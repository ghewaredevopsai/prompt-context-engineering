# Solutions

Reference answers for all seven labs. **Look at them whenever you want** &mdash; before, during or
after. Nothing here is a spoiler, because none of these labs is scored.

What that means in practice: the value of a lab in this module is the number *you* record, not
whether you arrived at the same one as this folder. Two people can both do Lab 4 correctly and get
different answers from their assistant, and comparing those two results is the actual lesson.

## What each file gives you

| File | What is in it |
|---|---|
| [`lab-1-saturday-surcharge.md`](lab-1-saturday-surcharge.md) | A reference implementation of the Saturday surcharge, the eight-row checklist with the right answers, and what a typical one-liner run gets wrong |
| [`lab-2-contract.md`](lab-2-contract.md) | A request that passes `check_contract.py` first time, a passing answer, and the three ways runs usually fail |
| [`lab-3-manifest-defects.md`](lab-3-manifest-defects.md) | All three money defects in `manifest.py`, with the runbook rule each one breaks |
| [`lab-4-groundings.md`](lab-4-groundings.md) | The three token counts, the answer each grounding tends to give, and why the largest bundle often loses |
| [`lab-5-prompt-check.md`](lab-5-prompt-check.md) | A worked `prompt-check.md`, including the rows that cannot be written and what to do about them |
| [`lab-6-model-habits.md`](lab-6-model-habits.md) | What the three response classes look like in full, and the direction each one moves the code |
| [`record-sheets/`](record-sheets/) | A filled-in example of every lab's record sheet |

## The numbers you can check yourself

These are deterministic for a given state of the practice repo &mdash; but the repo grows, so the
absolute totals drift. **Re-derive them rather than trusting this table**:

```bash
python3 tools/grounding_report.py     # the three groundings, live
python3 tools/audit_report.py         # the four cuts, live
```

At the time of writing:

| Measurement | Value |
|---|---|
| Practice repo, everything attached | ~52,000 est. tokens |
| `naive.txt` bundle | ~38,400 |
| `minimal.txt` &mdash; `rating.py` + `manifest.py` | ~2,200 |
| Six runbook lines + the failing test output | ~300 |
| Test suite | 27 tests, exactly 1 failure |
| The failing assertion | `113987 != 114655` |

## Using these well

- **Try the lab first.** Not for discipline's sake &mdash; the lab measures your starting point, and
  reading the answer first destroys the only measurement that was ever yours.
- **Disagree with them.** These are one trainer's answers on one codebase. Lab 3 says "at least
  three defects" because a fourth is defensible and people find it.
- **The record sheets are the format, not the target.** Your numbers will differ. The columns are
  what transfers to work.
