# Lab 5 &mdash; Break it, repair it, lock it

**Tier 5 &middot; Failure and drift** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## The situation

You have a prompt that works &mdash; run B from Lab 1. In three months it will stop
working and nobody will notice on the day. This lab is about finding out which part
of it is load-bearing, and writing down the thing that would have caught it.

**You have a prompt that works** &mdash; run B from Lab 1. You are going to break it
three prescribed ways, repair it, and write down the checks that would have caught
the damage. Work straight down this page.

---

## Step 1 &mdash; Set up

```bash
cd ~/meridian-freight
git switch -c lab-5-drift
```

Have **your Lab 1 run B prompt** and its **eight-row checklist** in front of you. You
score against those same eight rows five times in this lab.

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

## Step 3 &mdash; Break 1: delete the constraints

**3.1** Take the working prompt and **delete the whole `# constraints` block**. Change
nothing else.

**3.2** New chat, send it, score the eight rows.

**3.3** Reset: `git restore . && git clean -fd`

---

## Step 4 &mdash; Break 2: point at the wrong document

**4.1** Take the working prompt again. In the `# context` block, change

`docs/ops-runbook.md, section "Saturday collections"` &rarr; `docs/tariff-2026-notes.md`

That file exists. It is simply the wrong one.

**4.2** New chat, send it, score the eight rows.

**4.3** Reset.

---

## Step 5 &mdash; Break 3: loosen the format

**5.1** Take the working prompt again. Replace the whole `# format` block with:

```text
Explain your approach and then implement it.
```

**5.2** New chat, send it, score the eight rows.

**5.3** Reset.

---

## Step 6 &mdash; Repair

Put the prompt back together as it was in Step 2. Run it once more and confirm it
scores as it did then.

If it does not, that is a finding, not a mistake &mdash; write down what else changed.

---

## Step 7 &mdash; Lock it

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
&mdash; see the Notice section once you have tried.

---

## Step 8 &mdash; Run your own checks

Take one fresh run of the repaired prompt and see how many of your five rows it
passes.

---

## Step 9 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-5-record.md <<'EOF'
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
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

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
