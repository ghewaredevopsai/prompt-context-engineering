# Lab 5 — reference answer

## What the three breaks do

| break | rules broken | what it looks like |
|---|:--:|---|
| baseline (working prompt) | 0–1 of 8 | occasionally misses rule 5, export exclusion |
| 1 — delete `# constraints` | 3–5 | obviously worse: new dependencies, `manifest.py` edited, sometimes a float |
| 2 — point at the wrong document | 2–4 | **confident, well-formatted, wrong.** Fuel after the surcharge, because the stale notes say so |
| 3 — loosen `# format` | 2–3 | starts explaining; while explaining, starts editing neighbouring files |
| repaired | 0–1 | back to baseline |

**Break 2 is the one to dwell on.** Break 1 produces visibly worse code. Break 2 produces code that
cites a source — and the source is real, it is just stale. Nothing in the output looks wrong. This
is the top-right quadrant of the taxonomy, and it is the break that would survive review.

**Break 3 costs more than people expect.** Loosening the format loosens everything: format is not
only about parsing, it is the last constraint in the request and it holds the others in place.

## A worked `prompt-check.md`

```markdown
| case | what must be true of the output | how I check it |
|---|---|---|
| a Saturday domestic booking | a SAT charge of exactly 32000 appears | assert in test |
| a weekday booking | no SAT charge at all | assert in test |
| a Saturday export booking | no SAT charge at all | assert in test |
| any consignment with a surcharge | the fuel line is larger than fuel on the base alone | assert in test |
| any change | manifest.py is unmodified | `git diff --name-only` |
```

Five rows, all five writable. That is better than most first attempts, and it is because the rules
are unusually concrete. Now the two that usually defeat people:

```markdown
| any request | the code is idiomatic for this codebase | ??? |
| any request | the summary is useful to the supervisor | ??? |
```

## What to do with the rows you cannot write

**Decompose, or name an owner. Never leave it blank.**

"Idiomatic" almost always decomposes. On this codebase it becomes three checkable rules: money is an
integer, public functions return a `Quote`, and nothing calls `datetime.now()`. That is a check.

"Useful to the supervisor" does not decompose, and should not be forced to. The honest entry is:

```markdown
| any request | the summary is useful | the duty supervisor reads it each morning; no automated check |
```

Writing down *which human owns that judgement* is a real answer. Pretending a regex covers it is not.

## The sixth row worth adding

A check that asserts on something **not** happening — the Saturday export case above. Checks like
that are what catch a model update, because a model that starts being "helpful" about edge cases
breaks them first. Almost nobody writes them.

## What a fresh run scores

Against the repaired prompt, a fresh run typically passes 4 or 5 of the five writable rows. If it
passes all five twice running, your prompt is in good shape. If it passes three, you have found
drift on the day it happened, which is the only day it is cheap to fix.
