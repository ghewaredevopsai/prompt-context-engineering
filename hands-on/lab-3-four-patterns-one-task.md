# Lab 3 &mdash; Four patterns, one task

**Tier 3 &middot; The pattern set** &nbsp;|&nbsp; ~13 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored &nbsp;|&nbsp; **in pairs**

## The situation

Four named moves, one task, and a question nobody usually asks: what does each one
actually cost, and is it worth it *for this task*?

**Work in pairs.** Each of you runs two patterns, then you swap sheets and compare.
Four patterns each would take half an hour and you would stop reading the output
carefully by the third one.

## The task, identical for all four runs

> Review `meridian/manifest.py` against `docs/ops-runbook.md` and find everything it
> gets wrong about money.

There are at least three defects to find. You are measuring **how many each pattern
surfaces**, and what you paid for them.

## Before you start

Decide who runs which pair:

- **Partner A:** bare, then few-shot
- **Partner B:** decomposition, then self-critique

Each run starts in a **new chat**. Attach `meridian/manifest.py` and
`docs/ops-runbook.md` every time, and nothing else &mdash; so the only thing that
varies is the pattern.

## Do

1. **Bare.** Just the task, as written above. This is your baseline.

2. **Few-shot.** The task, preceded by two worked examples of the *kind* of finding
   you want &mdash; lift them from `meridian/rating.py`:

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

3. **Decomposition.** Three separate requests in the same chat, one at a time:

   ```text
   1. List every arithmetic operation in manifest.py that touches money. Do not judge them yet.
   2. For each one, quote the rule in ops-runbook.md that governs it.
   3. Now tell me which of them disagree with their rule.
   ```

4. **Self-critique.** The bare task, then when it answers:

   ```text
   Now find three ways your own review was incomplete. Check the charging order
   specifically.
   ```

5. **Count the tokens you sent.** Save each prompt as a file &mdash; `cat >
   prompt-bare.txt`, paste, <kbd>Ctrl</kbd>+<kbd>D</kbd> (see
   [hands-on/README](README.md#getting-text-out-of-the-chat-window-and-into-a-file))
   &mdash; then:

   ```bash
   python3 tools/ctxmeter.py count --absolute prompt-bare.txt
   ```

   The attachments are identical across runs, so the difference between these
   numbers is the cost of the pattern itself.

6. **Swap sheets with your partner** and fill in their two columns.

## Record

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
