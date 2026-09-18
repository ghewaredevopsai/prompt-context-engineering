# Lab 4 — reference answer

## The three numbers

Deterministic — everyone in the room gets these:

| grounding | est. tokens | ratio |
|---|--:|--:|
| A: attach everything | ~45,700 | 155x |
| B: `rating.py` + `manifest.py` | ~2,200 | 7.5x |
| C: six runbook lines + the failing test output | ~300 | 1x |

## The right answer

> `manifest.py` applies the fuel percentage to the base rate alone, while `rating.py` applies it to
> the base **plus** the surcharges. The runbook's *Charging order* section says fuel applies to the
> sum, so `rating.py` is correct and `manifest.py` under-collects on every consignment carrying a
> surcharge. `manifest.py` also omits the `OVERSIZE` and `INSURANCE` surcharges entirely.

## What each grounding tends to say

**C (six lines) — names it, and cites the rule.** You supplied the rule, so it can. Usually the
best answer in the room, from the smallest context.

**B (two files) — names the discrepancy, hedges on which side is wrong.** Both files are internally
consistent; nothing in either says which is authoritative. A good answer here says *"these two
disagree, and I cannot tell you which is right from these files"* — which is correct, and is the
answer a careful colleague would give.

**A (everything) — the interesting one.** Often does *not* name the drift, and sometimes reports
that `manifest.py` is **correct**.

## Why the biggest bundle loses

It is not that the model got confused by volume, although 45,700 tokens of mostly-tariff-data does
not help.

**It is that `docs/tariff-2026-notes.md` is in bundle A**, and that document says fuel applies to
the base alone — which is exactly what `manifest.py` does. The model was not hallucinating. It read
a document you gave it, that happens to be wrong, and agreed with it.

**A stale document in the bundle is worse than no document.** That is the whole tier, and this is
the measurement that proves it: a hundred and fifty times the context, and a worse answer, because one of the
extra files was lying.

## The stretch, and what it shows

Re-run A without `data/*.json` and without `tariff-2026-notes.md`. Tokens fall to roughly B's range
and the answer usually becomes B's answer. You have just written the context equivalent of a
`.gitignore` — and it is the first thing to reach for when somebody says "the tool is not good at
our codebase".

## What stays your job

Neither B nor C can tell you which file is *right*. Both are internally consistent, and the runbook
only wins because a human decided the runbook wins. Choosing the authoritative source is not a thing
you can delegate to the model, and no amount of context changes that.
