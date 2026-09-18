# Lab 3 &mdash; Four patterns, one task

**Tier 3 &middot; The pattern set** &nbsp;|&nbsp; ~15 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored &nbsp;|&nbsp; **in pairs**

## Objective

Find out what each named prompting pattern actually buys you, and what it costs
&mdash; on one real task, measured rather than argued about.

By the end you should be able to:

- describe few-shot, decomposition and self-critique in terms of what each does
  mechanically;
- say what each costs against an unpatterned baseline, and name a task where that
  cost is worth paying;
- say why chain of thought is **not** one of the three you ran;
- choose one to take back to work, and say what for.

## The situation

One task, run four ways: **a bare baseline and three named patterns**. The question
nobody usually asks is what each pattern costs against that baseline, and whether it
is worth it *for this task*.

Chain of thought is deliberately not among them &mdash; the last takeaway says why.

## What to watch for

- **How many of the three money defects each pattern surfaces.** That is the column
  the script cannot fill in for you, and the one that decides everything.
- **Whether a run was handed a clue.** Each pattern here is written to add *structure*
  and no information &mdash; see Step 2. If you reword one and accidentally name a
  defect, its score stops meaning anything.
- **Whether the pattern made it quote the rule** before judging. Most apparent
  reasoning failure is the model never having looked the rule up.
- **The ratio**, not the winner. "Self-critique found the most" is not a finding;
  "self-critique found one more and cost 2x" is.
- **In Step 5, whether the extra words bought anything.** That one run is the whole
  argument about chain of thought, and it takes a minute.

## Step 1 &mdash; Split the work

**Work in pairs.** Four runs each would take half an hour, and you would stop reading
the output carefully by the third.

- **Partner A:** the bare baseline, then few-shot
- **Partner B:** decomposition, then self-critique

**Working alone?** Run all four yourself and allow about twenty minutes.

---

## Step 2 &mdash; Agree the task, and do not change it

Every run uses this task, word for word:

> Review `meridian/manifest.py` against `docs/ops-runbook.md` and find everything it
> gets wrong about money.

**There are three money defects to find.** A fourth answer &mdash; that the band
lookup is duplicated from `rating.py` &mdash; is also defensible, and people who find
it often find it *instead* of one of the three.

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

FINDING: chargeable_weight_g() in rating.py divides volume by the divisor for the
consignment's scope - 5000 domestic, 6000 export - and charges the larger weight.
RULE: ops-runbook, "Weight".
VERDICT: correct.

FINDING: scripts/nightly_sync.py stamps its feed with datetime.now() instead of
taking the date it is syncing as an argument.
RULE: ops-runbook, "Clocks".
VERDICT: wrong.

Now: Review meridian/manifest.py against docs/ops-runbook.md and find everything it
gets wrong about money. Same three lines per finding.
```

The examples are about other files and other rules, one **correct** and one
**wrong**, and neither touches anything `manifest.py` gets wrong. That is deliberate:
few-shot is meant to demonstrate a *format and a standard of evidence* &mdash; name
the rule, then judge &mdash; not to hand over an answer. Both verdicts are true of the
code; an example that is itself wrong teaches the model your standard is low. The last
line is the task, word for word.

**Partner B &mdash; self-critique.** New chat. Send the bare task, wait for the
answer, then send:

```text
Now find three ways your own review was incomplete.
```

Save both messages together as **`prompt-critique.txt`**.

⚠️ **Do not add "check the charging order" or any other pointer.** An earlier version
of this lab did, and it made self-critique look better than it is: a run that is told
where to look is not being compared with runs that are not.

---

## Step 5 &mdash; The one you should not run, run once

Sixty seconds, whoever finishes their second pattern first.

New chat, the bare task, with one line added:

```text
Review meridian/manifest.py against docs/ops-runbook.md and find everything it
gets wrong about money.

Think step by step.
```

Compare what comes back with the plain bare run:

- **Is it more correct?** Usually not &mdash; the same defects, found the same way.
- **Is it longer?** Usually yes, sometimes much.

If your assistant is on a reasoning model, it was already reasoning before you asked.
`Think step by step` does not switch that on; it asks the model to *narrate* it as
well. **You pay for the reasoning twice and read it once.**

Do not save this one as a prompt file &mdash; it is not one of the three, and it is
not in the table. It is here so that when somebody asks why chain of thought is not in
this lab, you have seen the answer rather than been told it.

---

## Step 6 &mdash; Let the script do the arithmetic

```bash
python3 tools/lab3_report.py
```

```
pattern         file                   typed  turns   est. sent   vs bare
----------------------------------------------------------------------------
bare            prompt-bare.txt           29      1        2469   baseline
few-shot        prompt-fewshot.txt       149      1        2589   1.0x
decomposition   prompt-decomp.txt          -      3           -   not saved yet
self-critique   prompt-critique.txt        -      2           -   not saved yet
```

*(An example, not a target &mdash; yours will differ with how you word things.)*

Two columns matter. **typed** is what you wrote. **est. sent** is what the pattern
actually sent: the two attachments go again with *every turn*, so a three-turn pattern
pays for them three times. That is why few-shot, with the most words, costs barely
more than bare, and decomposition, with three short questions, costs the most.

**est. sent is a floor.** From the second turn on, the model's own earlier replies are
re-sent too, and no file can see them.

Your partner's two rows stay blank until you swap.

---

## Step 7 &mdash; Swap with your partner

Copy their two prompt files into your folder, or sit together and run the script once
on all four. Now you have the whole table.

---

## Step 8 &mdash; Record

```bash
python3 tools/lab3_report.py --record
```

That writes `lab-3-record.md` with the token and turn columns already filled in.
**You fill in the defects each pattern found and the questions at the foot** &mdash;
those are the judgements, and they are the point of the lab.

The chain-of-thought run from Step 5 is deliberately not a row: it is a demonstration,
not a contender.

```bash
git add lab-3-record.md && git commit -m "lab 3: four patterns"
```

## Key takeaways

- **The finding is the ratio, not the winner.** "Self-critique found the most" is not
  a finding. "Self-critique found one more and cost 2x" is &mdash; it is the number
  you need to decide, per task, whether doubling the bill is worth it. On money code
  it obviously is. On a docstring it obviously is not.

- **Two expectations to test, not to accept.** The trainer's experience is that
  self-critique surfaces the most and costs roughly double, and that decomposition
  does better than people expect because its second request forces the model to quote
  the rule before judging. **Neither is measured.** Your table is the evidence; if it
  disagrees, your table wins and the room should hear it.

- **Few-shot is doing something different from the other three.** It is not making
  the model think harder; it is showing it a format and a standard of evidence. Use
  it when the rule is easier to show than to say.

- **Chain of thought is not in the table, and Step 5 is why.** Against a reasoning
  model, `think step by step` does not make it reason &mdash; it makes it narrate the
  reasoning it was doing anyway, in output tokens, which bill at several times the
  input rate. It remains worth asking for when you need the reasoning **visible** for a
  human to audit. That is a different reason from "it makes the answer better".

## Stretch

Run the bare task once more, but first add one line: `Quote the runbook line you are
judging against for every finding.` One line, no pattern, no extra turns. Compare it
with the decomposition column once you have swapped sheets. A large part of what patterns buy you can sometimes
be bought with a sentence &mdash; and a sentence is cheaper to maintain than a
four-step procedure.
