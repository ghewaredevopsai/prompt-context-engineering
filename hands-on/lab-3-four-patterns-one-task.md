# Lab 3 &mdash; Four patterns, one task

**Tier 3 &middot; The pattern set** &nbsp;|&nbsp; ~13 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored &nbsp;|&nbsp; **in pairs**

## The situation

Four named moves, one task, and a question nobody usually asks: what does each one
actually cost, and is it worth it *for this task*?

**Work in pairs.** Each of you runs two patterns, then you swap sheets and compare.
Four patterns each would take half an hour and you would stop reading the output
carefully by the third one.

**Four named patterns, one task, run in pairs.** Each of you runs two patterns, then
you swap sheets. Four each would take half an hour and you would stop reading the
output carefully by the third.

---

## Step 1 &mdash; Split the work

- **Partner A:** bare, then few-shot
- **Partner B:** decomposition, then self-critique

---

## Step 2 &mdash; Agree the task, and do not change it

Every run uses this task, word for word:

> Review `meridian/manifest.py` against `docs/ops-runbook.md` and find everything it
> gets wrong about money.

There are at least three defects to find.

**Every run also starts in a new chat with the same two files attached** &mdash;
`meridian/manifest.py` and `docs/ops-runbook.md`, nothing else. That way the pattern
is the only thing that varies.

---

## Step 3 &mdash; Your first pattern

**Partner A &mdash; bare.** New chat, the task exactly as above, nothing added. This
is the baseline.

**Partner B &mdash; decomposition.** New chat. Three requests, one at a time, waiting
for each answer:

```text
1. List every arithmetic operation in manifest.py that touches money. Do not judge them yet.
```

```text
2. For each one, quote the rule in ops-runbook.md that governs it.
```

```text
3. Now tell me which of them disagree with their rule.
```

Both: count the defects it found, and how many turns you sent.

---

## Step 4 &mdash; Your second pattern

**Partner A &mdash; few-shot.** New chat. The task, preceded by two worked examples of
the *kind* of finding you want:

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

---

## Step 5 &mdash; Count what each pattern cost you

Save each prompt you sent as its own file &mdash; in your editor, or with
`cat > prompt-bare.txt` in a terminal
([how](README.md#getting-text-out-of-the-chat-window-and-into-a-file)) &mdash; then:

```bash
python3 tools/ctxmeter.py count --absolute prompt-bare.txt
```

The attachments are identical across runs, so the **difference** between these
numbers is the cost of the pattern itself.

---

## Step 6 &mdash; Swap sheets

Fill in your partner's two rows from their numbers. You now have all four patterns on
one sheet.

---

## Step 7 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-3-record.md <<'EOF'
# Lab 3

                  defects found   est. prompt tokens   turns   would I use it here?
bare              ___ / 3         ______               ___     ______
few-shot          ___ / 3         ______               ___     ______
decomposition     ___ / 3         ______               ___     ______
self-critique     ___ / 3         ______               ___     ______

The three defects in manifest.py: ____________________________________

Cheapest pattern that found all three: ______________
The pattern I will actually use at work, and for what: ______________
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-3-record.md && git commit -m "lab 3: four patterns"
```

## Notice

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
