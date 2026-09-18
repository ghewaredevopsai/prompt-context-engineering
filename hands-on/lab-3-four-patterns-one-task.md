# Lab 3 &mdash; Four patterns, one task

**Tier 3 &middot; The pattern set** &nbsp;|&nbsp; ~13 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored &nbsp;|&nbsp; **in pairs**

## Objective

Find out what each named prompting pattern actually buys you, and what it costs
&mdash; on one real task, measured rather than argued about.

By the end you should be able to:

- describe few-shot, decomposition, chain of thought and self-critique in terms of
  what each does mechanically;
- say what each costs, and name a task where that cost is worth paying;
- choose one to take back to work, and say what for.

## The situation

Four named moves, one task, and a question nobody usually asks: what does each one
actually cost, and is it worth it *for this task*?

**Work in pairs.** Each of you runs two patterns, then you swap sheets and compare.
Four patterns each would take half an hour and you would stop reading the output
carefully by the third one.

## What to watch for

- **How many of the three money defects each pattern surfaces.** That is the column
  the script cannot fill in for you, and the one that decides everything.
- **Whether the pattern made it quote the rule** before judging. Most apparent
  reasoning failure is the model never having looked the rule up.
- **The ratio**, not the winner. "Self-critique found the most" is not a finding;
  "self-critique found one more and cost 2.2x" is.

## Step 1 &mdash; Split the work

**Work in pairs.** Four patterns each would take half an hour and you would stop
reading the output carefully by the third.

- **Partner A:** bare, then few-shot
- **Partner B:** decomposition, then self-critique

---

## Step 2 &mdash; Agree the task, and do not change it

Every run uses this task, word for word:

> Review `meridian/manifest.py` against `docs/ops-runbook.md` and find everything it
> gets wrong about money.

There are at least three defects to find.

**Every run starts in a new chat with the same two files attached** &mdash;
`meridian/manifest.py` and `docs/ops-runbook.md`, nothing else. That way the pattern
is the only thing that varies.

---

## Step 3 &mdash; Run your first pattern

**Partner A &mdash; bare.** New chat. The task exactly as above, nothing added.
Save what you sent as **`prompt-bare.txt`**.

**Partner B &mdash; decomposition.** New chat. Three requests, one at a time, waiting
for each answer:

```text
1. List every arithmetic operation in manifest.py that touches money. Do not judge them yet.
2. For each one, quote the rule in ops-runbook.md that governs it.
3. Now tell me which of them disagree with their rule.
```

Save all three, together, as **`prompt-decomp.txt`**.

Both: note how many of the three defects it found, and how many turns you sent.

---

## Step 4 &mdash; Run your second pattern

**Partner A &mdash; few-shot.** New chat. The task, preceded by two worked examples of
the *kind* of finding you want. Save as **`prompt-fewshot.txt`**:

```text
Here are two examples of the kind of finding I want:

FINDING: rating.py charges fuel on (base + surcharges).
RULE: ops-runbook, "Charging order" - fuel applies to the sum.
VERDICT: correct.

FINDING: rating.py uses integer minor units throughout, no float.
RULE: ops-runbook, "Money".
VERDICT: correct.

Now do the same for meridian/manifest.py. Same three lines per finding.
```

**Partner B &mdash; self-critique.** New chat. Send the bare task, wait for the
answer, then send:

```text
Now find three ways your own review was incomplete. Check the charging order
specifically.
```

Save both messages together as **`prompt-critique.txt`**.

---

## Step 5 &mdash; Let the script do the arithmetic

```bash
python3 tools/lab3_report.py
```

```
pattern         file                 est. tokens   vs bare
--------------------------------------------------------------
bare            prompt-bare.txt              24   baseline
few-shot        prompt-fewshot.txt          101   4.2x
decomposition   prompt-decomp.txt             -   not saved yet
self-critique   prompt-critique.txt           -   not saved yet
```

The attachments are identical across runs, so the **difference between these numbers
is the cost of the pattern itself**. Your partner's two rows stay blank until you
swap.

---

## Step 6 &mdash; Swap with your partner

Copy their two prompt files into your folder, or sit together and run the script once
on all four. Now you have the whole table.

---

## Step 7 &mdash; Record

```bash
python3 tools/lab3_report.py --record
```

That writes `lab-3-record.md` with the token columns already filled in. **You fill in
the defects each pattern found, the turns, and the two questions at the foot** &mdash;
those are the judgements, and they are the point of the lab.

```bash
git add lab-3-record.md && git commit -m "lab 3: four patterns"
```

## Key takeaways

- **The finding is the ratio, not the winner.** Self-critique usually finds the most
  and usually costs about twice as much. That is not an argument for or against it
  &mdash; it is the number you need in order to decide, per task, whether doubling
  the bill is worth it. On money code it obviously is. On a docstring it obviously
  is not.

- **Decomposition wins more often than people expect**, because step 2 forces the
  model to quote the rule before judging it. Most of what looks like reasoning
  failure is the model never having looked the rule up.

- **Few-shot is doing something different from the other three.** It is not making
  the model think harder; it is showing it a format and a standard of evidence. Use
  it when the rule is easier to show than to say.

- **Nobody should be running chain of thought here.** If you tried "think step by
  step" on a reasoning model, compare its output length with the bare run. You paid
  for the same reasoning twice.

## Stretch

Run the bare task once more, but first add one line: `Quote the runbook line you are
judging against for every finding.` One line, no pattern, no extra turns. Compare it
with your decomposition column. A large part of what patterns buy you can sometimes
be bought with a sentence &mdash; and a sentence is cheaper to maintain than a
four-step procedure.
