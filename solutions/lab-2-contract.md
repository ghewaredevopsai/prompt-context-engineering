# Lab 2 — reference answer

## A request that passes first time

```text
Summarise this exceptions report for the duty supervisor.

Return ONLY JSON, no fence, no preamble, in exactly this shape:
{"generated_for": "YYYY-MM-DD",
 "exceptions": [{"consignment": "MF-0000", "codes": ["MF-01"], "action": "<= 120 chars"}],
 "total": <number of entries in exceptions>}

The codes are a closed set of six, defined in meridian/validate.py. Use no others.
If a consignment's action is unclear from the codes alone, set action to "review".
```

## An answer that satisfies the contract

```json
{"generated_for": "2026-03-04",
 "exceptions": [
   {"consignment": "MF-1034", "codes": ["MF-03", "MF-04"], "action": "hold - chase the DG declaration, then route"},
   {"consignment": "MF-1003", "codes": ["MF-06"], "action": "reprice against the 2025 tariff"},
   {"consignment": "MF-1024", "codes": ["MF-01"], "action": "call the depot for dimensions"}],
 "total": 3}
```

```
$ python3 tools/check_contract.py answer.json
check_contract: answer.json satisfies the contract
  shape only - it says nothing about whether the answer is right
$ echo $?
0
```

## The three ways runs actually fail

Verified output from the checker on a typical bad answer:

```
check_contract: bad.json breaks the contract in 3 place(s)
  - exceptions[0].consignment '1034' is not in the form MF-0000
  - exceptions[0].codes has 'MF-07', which is not one of the six: MF-01, MF-02, MF-03, MF-04, MF-05, MF-06
  - 'total' says 2 but there are 1 rows
```

1. **A fence.** `` ```json `` before the object. This is the single most common failure and the
   cheapest to fix — it is the "right answer, wrong shape" quadrant. `Return ONLY JSON, no fence`
   earns its place in the request.
2. **An invented code.** `MF-07` and `MF-99` both turn up. Specific, plausible, correctly formatted,
   and it would reject the whole batch downstream. This is a fabricated fact with a number attached.
3. **`total` disagreeing with the list.** Usually because the model counted the consignments it
   *described in prose first* rather than the rows it emitted.

## The result that surprises people

| shape | est. output tokens |
|---|---|
| free prose | ~210 |
| delimited | ~90 |
| supplied schema | ~140 |

The JSON is **shorter than the prose**, not longer. A contract does not cost you tokens — it stops
the model narrating, and the narration was most of what you were paying for. The delimited version
is shortest of all and is still the worst option, because a dropped field shifts every column
silently and nothing raises.

(Your numbers will differ; the ordering is the stable part.)

## Why the checker is deliberately weak

`check_contract.py` judges **shape, not quality**. It cannot tell you whether those are the right
three consignments, whether "reprice" is sensible, or whether the model understood the question.

That is not a limitation to fix. It is the line: shape is what decides whether the next step can run
without a human, which is a much lower bar than "good" and a much more useful one to be able to test.
