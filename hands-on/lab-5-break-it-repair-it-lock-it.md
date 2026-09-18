# Lab 5 &mdash; Break it, repair it, lock it

**Tier 5 &middot; Failure and drift** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: **agent mode** &nbsp;|&nbsp; measured, not scored

## Objective

Find out which part of a working prompt is load-bearing, and write down the thing
that would catch it when it stops working.

By the end you should be able to:

- name three directions a working prompt rots from;
- say why a green test suite is not evidence when the model wrote both sides;
- write a check that is machine-checkable, and recognise honestly when you cannot.

## The situation

You have a prompt that works &mdash; run B from Lab 1. In three months it will stop
working and nobody will notice on the day. This lab is about finding out which part
of it is load-bearing, and writing down the thing that would have caught it.

You will run it once as it is, once with **one** of three prescribed breaks, and once
repaired &mdash; and the repaired run is also the one you test your own checks
against. **Use agent mode**, as in Lab 1: the prompt points the assistant at files it
has to open itself, and it edits code you then test and reset.

Work straight down this page.

## What to watch for

- **Break 2 is the quiet one.** Deleting constraints produces visibly worse code.
  Pointing at the wrong document produces confident, well-formatted, wrong code that
  cites a real source. Only one of those survives review.
- **Break 3 costs more than it looks.** Loosening the format tends to loosen
  everything: the model starts explaining, and while explaining it starts editing
  neighbours.
- **Some of your five checks will not be writable.** That is the exercise. Notice
  *which* ones &mdash; they are the ones you were quietly relying on a person for.

---

## Step 1 &mdash; Set up

```bash
cd ~/meridian-freight
git status
```

`git status` must report nothing to commit. If Lab 1's run B code is still there,
clear it first with `git restore . && git clean -fd` &mdash; otherwise the baseline
asks for a surcharge that already exists. Then:

```bash
git switch -c lab-5-drift
```

Have **your Lab 1 run B prompt** and its **eight-row checklist** in front of you. You
score against those same eight rows three times in this lab.

**Take a break number.** Count off round the room &mdash; 1, 2, 3, 1, 2, 3 &mdash; and
run only that break in Step 3. Every break still gets several runs across the room,
which tells you more than one person running all three would.

---

## Step 2 &mdash; Re-establish the baseline

**2.1** Send your Lab 1 run B prompt again, in a **new chat**, unchanged.

**2.2** Score it against the eight rows. This is your "before" column.

**Do not reuse Lab 1's number.** The point of the exercise is that the same prompt
does not always give the same answer, and you need today's figure to compare against.

**2.3** Reset:

```bash
git restore . && git clean -fd
```

---

## Step 3 &mdash; Run your break

Take the working prompt, apply **your** break below and change nothing else. New
chat, send it, score the eight rows, then reset with `git restore . && git clean -fd`.

**Break 1 &mdash; delete the constraints.** Delete the whole `# constraints` block.

**Break 2 &mdash; point at the wrong document.** In the `# context` block, change

`docs/ops-runbook.md, section "Saturday collections"` &rarr; `docs/tariff-2026-notes.md`

That file exists. It is simply the wrong one. It says nothing about Saturdays at all;
what it does say is that surcharges are *not* fuelled &mdash; watch where that lands.

**Break 3 &mdash; loosen the format.** Replace the whole `# format` block with:

```text
Explain your approach and then implement it.
```

---

## Step 4 &mdash; Lock it

Create `prompt-check.md` with **five rows**. One paste starts it:

```bash
cat > prompt-check.md <<'EOF'
| case | what must be true of the output | how I check it |
|---|---|---|
| a Saturday domestic booking | a SAT charge of exactly 32000 appears | assert in test |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
EOF
```

Fill in the other four. **Try to make every row checkable by something other than a
person reading it.**

You will not manage it for all five. That is the exercise, not a failure of it
&mdash; see the takeaways once you have tried.

---

## Step 5 &mdash; Repair, and run your checks

**5.1** Put the prompt back exactly as it was in Step 2. New chat, send it, score the
eight rows.

If it does not score as it did in Step 2, that is a finding, not a mistake &mdash;
write down what else changed.

**5.2** **Do not reset yet.** Check this run's code against your five rows:

- an **assert in test** row &mdash; add the test to `tests/test_rating.py` and run
  `python3 -m unittest discover -s tests -t .`
- a "file untouched" row &mdash; `git diff --name-only`
- a row only a person can check &mdash; check it by reading, and say so on the sheet

Count how many of the five this run passes.

---

## Step 6 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-5-record.md <<'EOF'
# Lab 5

                          rules broken / 8
baseline (working)        ___
my break: number ___      ___    which rows: ____________
repaired                  ___

From the board, the other two breaks:
break ___                 ___    which rows: ____________
break ___                 ___    which rows: ____________

Of my five checks, ___ are machine-checkable and ___ need a person.
The check I could not write, and what I would need to make it writable:
____________________________________________________________

The repaired run passed ___ of my 5 checks.
EOF
```

Fill in the blanks in any editor, then commit the sheet and the check file &mdash; only
those. The repaired run's code is thrown away straight after:

```bash
git add lab-5-record.md prompt-check.md && git commit -m "lab 5: break, repair, lock"
git restore . && git clean -fd
```

## Key takeaways

- **Break 2 is the quiet one.** Deleting constraints produces obviously worse code.
  Pointing at the wrong document produces *confident, well-formatted, wrong* code
  that cites a source &mdash; and the source is real, it is just stale. This is the
  top-right quadrant, and it is the one that survives review.

- **Break 3 costs you more than you would guess.** Loosening the format usually
  loosens everything else with it: the model starts explaining, and while explaining
  it starts editing neighbouring files. Format is not only about parsing.

- **Some of your five checks will not be writable**, and they will be the
  interesting ones &mdash; "the code is idiomatic", "the summary is useful". Those
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
