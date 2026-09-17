# Lab 1 &mdash; reference answer

## A correct implementation

Two changes to `meridian/rating.py`. Nothing else in the package is touched.

```python
def _is_saturday_collection(consignment: Consignment) -> bool:
    """Saturday collections carry a flat surcharge - domestic only.

    We do not collect export freight on Saturdays at all, so a Saturday export
    booking is a data error rather than a chargeable collection.

    The day comes from the consignment's own timestamp, never from today.
    """
    if consignment.scope is Scope.EXPORT:
        return False
    return consignment.booked_at.weekday() == 5
```

and, inside `_surcharges()`, **before** the return &mdash; so it lands in the subtotal that fuel is
charged on:

```python
    if _is_saturday_collection(consignment):
        sat = tariffs.surcharge(tariff, "SAT")
        out.append(Charge("SAT", sat["label"], sat["flat_minor"]))
```

Note what this does *not* do: it does not reach for `datetime.now()`, it does not hardcode 32000, it
does not return a float, and it adds nothing to `manifest.py`.

## A test that proves the parts that matter

```python
def test_a_saturday_domestic_booking_carries_the_flat_surcharge(self):
    q = rating.quote(consignment(booked_at=datetime(2026, 3, 7, 9, 0, 0)), self.tariff)
    self.assertEqual(q.charge("SAT").amount_minor, 32000)

def test_a_weekday_booking_does_not(self):
    q = rating.quote(consignment(booked_at=datetime(2026, 3, 4, 9, 0, 0)), self.tariff)
    self.assertIsNone(q.charge("SAT"))

def test_export_is_excluded_even_on_a_saturday(self):
    q = rating.quote(consignment(booked_at=datetime(2026, 3, 7, 9, 0, 0),
                                 scope=Scope.EXPORT), self.tariff)
    self.assertIsNone(q.charge("SAT"))

def test_fuel_is_charged_on_the_saturday_surcharge(self):
    sat = rating.quote(consignment(booked_at=datetime(2026, 3, 7, 9, 0, 0)), self.tariff)
    wed = rating.quote(consignment(booked_at=datetime(2026, 3, 4, 9, 0, 0)), self.tariff)
    self.assertGreater(sat.charge("FUEL").amount_minor, wed.charge("FUEL").amount_minor)
```

Verified against the reference implementation: SAT is 32000 on a Saturday domestic booking, absent on
a weekday, absent on a Saturday export booking, and the fuel line rises from **14,824 to 19,576**
minor units because the surcharge is inside the subtotal.

That last test is the one worth having. It is the only one that would catch the most expensive
mistake in this lab, and it does not mention the number 32000 at all.

## The eight rows, with the answers

| # | House rule | Where it is written | What a one-liner run typically does |
|---|---|---|---|
| 1 | Flat 32000 paise, not a percentage | runbook, *Saturday collections* | Often invents a percentage of declared value. Percentages feel more "flexible" |
| 2 | Charge code is `SAT` | runbook + `tariff.json` | Usually invents `SATURDAY` or `SAT_COLLECT`. Harmless-looking, breaks the billing feed |
| 3 | Money stays an integer | runbook, *Money* | Reaches for `float` or `Decimal` perhaps half the time |
| 4 | Applied **before** fuel | runbook, *Charging order* | **The expensive one.** Frequently appended after the fuel line, where no test fails |
| 5 | Export excluded | runbook, *Saturday collections* | Almost always missed &mdash; it is a negative rule, and nothing in the code hints at it |
| 6 | Returns a `Charge` | `models.py`, and every other surcharge | Usually right, because the surrounding code shows the pattern |
| 7 | `unittest`, no new dependency | runbook + `README` | Usually right; occasionally imports `pytest` or `dateutil` |
| 8 | `manifest.py` untouched | runbook, *routing*/duplication | Sometimes "helpfully" updates the manifest too, which looks like diligence |

## Why rule 4 is the one to dwell on

If the surcharge is added after the fuel line, every Saturday consignment under-bills by the fuel
percentage of &#8377;320 &mdash; about &#8377;47 at the current rate. Forever. Silently. **No test in
the repository fails**, because the repository has no test for a rule it has never implemented.

That is the top-right quadrant of Tier 5 arriving a tier early: readable code, plausible output, and
wrong in a way that only a rule written down somewhere else could have caught.

## What a good run B looks like against a typical run A

| | run A (one-liner) | run B (assembled) |
|---|---|---|
| turns to green | 3&ndash;4 | 1&ndash;2 |
| rules broken | 4&ndash;6 of 8 | 0&ndash;1 of 8 |
| usually broken | 1, 4, 5, and often 2 | occasionally 5 |

**Rule 5 survives longest into run B**, which is worth noticing: it is the one rule stated as a
negative. If your `# context` block quoted the runbook section rather than pointing at it, you
probably caught it.

Your own numbers will differ, and that is fine &mdash; the pattern that matters is *which* rules
break, not how many.
