# Lab 3 — reference answer

## The three money defects in `manifest.py`

All three are real, all three are checkable against `docs/ops-runbook.md`, and the first one is the
cause of the failing test in the repository.

### 1. Fuel is charged on the base alone

```python
pct = tariffs.fuel_pct(tariff, consignment.booked_at)
fuel = (base * int(pct * 100)) // 10_000       # <- base, not base + extras
```

**Rule broken:** runbook, *Charging order* — "Base rate, then surcharges, then fuel **on the sum of
the two**."

**Why it exists, which is the interesting part:** `docs/tariff-2026-notes.md` says *"Fuel is applied
to the base rate. Surcharges are added afterwards and are not themselves fuelled."* That document is
stale and the runbook says so. Whoever wrote `manifest.py` read the wrong file. **This is a
grounding failure preserved in code**, not a coding mistake — which is why Lab 4 can find it with
six pasted lines and cannot find it with the whole repository.

This is the defect behind `AssertionError: 113987 != 114655`.

### 2. `OVERSIZE` is missing entirely

`rating.py` charges 78000 for any piece over 120 cm on a side or 250,000 cm³. `manifest.py` never
looks. A consignment with an oversize piece is under-collected by ₹780 plus its fuel.

### 3. `INSURANCE` is missing entirely

`rating.py` charges 1.15% of declared value with a 9000 floor. `manifest.py` has no insurance line
at all.

### The fourth answer, which is also right

The band lookup is **duplicated** from `rating.py`, including the 1 kg short-circuit. Two copies of
the same pricing table walk, and only one of them will be fixed when the tariff changes. The runbook
says it plainly: *"Never re-implement rating in `manifest.py`; call `rating.quote()`."*

People who find this one usually find it *instead* of #2 and #3, because they stop reading once they
see the duplication. Both readings are defensible.

## What each pattern typically surfaces

| pattern | defects found | prompt tokens | notes |
|---|:--:|:--:|---|
| bare | 1 of 3 | baseline | finds the fuel drift, stops |
| few-shot | 2 of 3 | +40% | the worked examples set a standard of evidence, so it keeps going |
| decomposition | 3 of 3 | +20%, over 3 turns | step 2 forces it to quote the rule before judging |
| self-critique | 3 of 3 | ~2.2x | finds the most, including the duplication; costs the most |

**The finding is the ratio, not the winner.** Decomposition tends to win on value here because the
middle step — "quote the rule that governs each one" — does the work. Most of what looks like
reasoning failure is the model never having looked the rule up.

## The one-line version

Adding `Quote the runbook line you are judging against for every finding.` to the bare request gets
most of decomposition's benefit for one sentence and no extra turns. Worth trying before adopting a
four-step procedure that somebody has to maintain.
