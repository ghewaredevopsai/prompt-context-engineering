# Lab 5 &mdash; Break it, repair it, lock it

**Tier 5 &middot; Failure and drift** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## The situation

You have a prompt that works &mdash; run B from Lab 1. In three months it will stop
working and nobody will notice on the day. This lab is about finding out which part
of it is load-bearing, and writing down the thing that would have caught it.

## Before you start

```bash
cd meridian-freight
git switch -c lab-5-drift
```

Have your Lab 1 run B prompt and its eight-row checklist in front of you.

## Do

1. **Re-establish the baseline.** Run your Lab 1 run B prompt once more in a new
   chat. Score it against the eight rows. This is your "before" column &mdash; do
   not reuse Lab 1's number, because the point of the exercise is that the same
   prompt does not always give the same answer.

   ```bash
   git restore . && git clean -fd
   ```

2. **Break it three ways.** Each time: start from the working prompt, make **one**
   prescribed change, run it in a new chat, score the eight rows, then reset.

   - **Break 1 &mdash; delete the `# constraints` block.**
   - **Break 2 &mdash; corrupt the context.** Change `docs/ops-runbook.md, section
     "Saturday collections"` to `docs/tariff-2026-notes.md`. The file exists. It is
     just the wrong one.
   - **Break 3 &mdash; loosen the format.** Replace the `# format` block with
     `Explain your approach and then implement it.`

3. **Repair.** Put the prompt back together and confirm it scores as it did in
   step 1. If it does not, that is a finding &mdash; write down what else changed.

4. **Lock it.** Create `prompt-check.md` in the repository root with **five rows**:

   ```markdown
   | case | what must be true of the output | how I check it |
   |---|---|---|
   | a Saturday domestic booking | a SAT charge of exactly 32000 appears | assert in test |
   |  |  |  |
   |  |  |  |
   |  |  |  |
   |  |  |  |
   ```

   Fill in four more. **Try to make every row checkable by something other than a
   person reading it.** You will not manage it for all five. That is the exercise,
   not a failure of it.

5. **Run your own checks.** Take a fresh run of the repaired prompt and see how many
   of your five rows it passes.

## Record

```markdown
# Lab 5

                          rules broken / 8
baseline (working)        ___
break 1: no constraints   ___    which rows: ____________
break 2: wrong document   ___    which rows: ____________
break 3: loose format     ___    which rows: ____________
repaired                  ___

Of my five checks, ___ are machine-checkable and ___ need a person.
The check I could not write, and what I would need to make it writable:
____________________________________________________________

A fresh run passed ___ of my 5 checks.
```

```bash
git add lab-5-record.md prompt-check.md && git commit -m "lab 5: break, repair, lock"
```

## Notice

- **Break 2 is the quiet one.** Deleting constraints produces obviously worse code.
  Pointing at the wrong document produces *confident, well-formatted, wrong* code
  that cites a source &mdash; and the source is real, it is just stale. This is the
  top-right quadrant, and it is the one that survives review.

- **Break 3 costs you more than you would guess.** Loosening the format usually
  loosens everything else with it: the model starts explaining, and while explaining
  it starts editing neighbouring files. Format is not only about parsing.

- **Three of your five checks will not be writable**, and they will be the
  interesting three &mdash; "the code is idiomatic", "the summary is useful". Those
  are the rows where you were quietly relying on a person. Either decompose them into
  something specific, or write down which human owns that judgement. Both are honest.
  Leaving the row blank is not.

- **A prompt with a check file is a different object** from a prompt in somebody's
  chat history. It can be reviewed, owned and re-run against a model you did not
  choose. That is the whole of Tier 5 in one sentence.

## Stretch

Add a sixth row to `prompt-check.md` for a case that does **not** exist yet: a
Saturday *export* booking, which must pick up no SAT charge at all. Run the prompt
fresh and check it. A check that asserts on something not happening is the kind
that catches a model update, and almost nobody writes them.
