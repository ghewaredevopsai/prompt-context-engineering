# Lab 6 — reference answer

## The ambiguity, precisely

`Fix the manifest total so it matches the quote.` is under-specified in exactly one way: two files
disagree and nothing in the request says which is right.

- `rating.py` charges fuel on base + surcharges — **correct**, per the runbook
- `manifest.py` charges fuel on base alone — wrong, per the runbook

Attaching both files and *not* the runbook is deliberate. With the runbook attached there is no
ambiguity left to observe.

## The three classes, in full

**Asks.** *"These two files disagree about whether fuel applies to surcharges. The runbook is not in
what you gave me. Which is authoritative?"* — the best outcome and the rarest.

**Picks, and says so.** *"I have assumed `rating.py` is correct, because `quote()` is documented as
the only place that decides a price. If that is wrong, the change is one line."* — fine. The
assumption is visible and cheap to reverse.

**Picks, silently.** Edits one file to match the other and reports success. **The expensive one**,
and it splits two ways:

- edits `manifest.py` → now correct, silently. *Dangerous*, because it teaches you to trust the silence.
- edits `rating.py` → now **both are consistently wrong**, the failing test passes, and the repository
  looks healthier than before.

That last case is worth sitting with: a green test suite, a smaller diff, and the bug has spread.

## What the added line does

```text
If the two files disagree about a rule, stop and ask me which is authoritative.
```

The spread across models narrows sharply. Most of what looks like *"this model is better at
ambiguity"* is *"this model happens to ask by default"*, and one sentence closes most of the gap.

**That is the portable finding.** A prompt that says what to do when unsure works on a model you did
not choose. A prompt that relies on being asked is a prompt that relies on a habit.

## Classifying honestly

Record **class** and **direction** separately. They are independent, and the dangerous combination —
silent and correct — looks like the best result if you only record one column.

## The single-model stretch

Five runs of the ambiguous prompt on one model, in five new chats, frequently produce two different
classes. If one model gives you two answers across five runs, then *"which model asks?"* was never
the right question. The right question is what your prompt does when nobody asks — which is Tier 5's
answer, arrived at from the other end.

## A note on shelf life

Everything here has a shelf life of about one model release. The six habits are stable; which model
shows which is not. Date your record sheet.
