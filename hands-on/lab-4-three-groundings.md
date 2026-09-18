# Lab 4 &mdash; Three groundings, one question

**Tier 4 &middot; Grounding** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## The situation

One failing test, one question, three ways of answering it. This is the lab that
settles the argument about whether attaching more context buys you a better answer.

**The question, identical in all three runs:**

> Why does the manifest total differ from the quote total?

## Do

1. **Measure the three bundles before you send anything.**

   ```bash
   python3 tools/ctxmeter.py count --absolute $(cat tools/bundles/everything.txt | grep -v '^#')
   python3 tools/ctxmeter.py count --absolute meridian/rating.py meridian/manifest.py
   ```

   And for the third: the six lines of `docs/ops-runbook.md` under **Charging order**
   that decide this. Put them in a file and meter that:

   ```bash
   sed -n '/^## Charging order/,/^## Clocks/p' docs/ops-runbook.md > six-lines.txt
   python3 tools/ctxmeter.py count --absolute six-lines.txt
   ```

   Write all three numbers down **now**, before you know which answer is best.

2. **Run A &mdash; attach everything.** New chat. Attach the whole repository (in
   VS Code: `#codebase`, or drag the folder in). Ask the question.

3. **Run B &mdash; attach two files.** New chat. Attach `meridian/rating.py` and
   `meridian/manifest.py`. Nothing else. Ask the question.

4. **Run C &mdash; paste the rule.** New chat. Attach **nothing**. Paste the six
   runbook lines and the failing test output:

   ```bash
   python3 -m unittest tests.test_manifest -v 2>&1 | tail -12
   ```

   Ask the question.

5. **Score each answer on one thing only:** did it name the fuel-surcharge drift
   &mdash; that `manifest.py` applies fuel to the base alone while `rating.py`
   applies it to base plus surcharges? Yes or no. Not "did it sound insightful".

## Record

One paste creates the sheet:

```bash
cat > lab-4-record.md <<'EOF'
# Lab 4

                       est. tokens sent   named the drift?   also found the two
                                                             missing surcharges?
A: everything          ______             ___                ___
B: two files           ______             ___                ___
C: six pasted lines    ______             ___                ___

Ratio of A to C: ______ times the context.
Which gave the most useful answer? ______

If A lost, what did it spend its attention on instead? ____________________
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-4-record.md && git commit -m "lab 4: three groundings"
```

**Put the three yes/no columns on the board.** The token numbers are deterministic
and everyone's will match. The yes/no columns are not, and the spread across the room
is the real result &mdash; if a third of the room got a "yes" from run A, that is
worth more discussion than any slide.

## Notice

- **Run A is over a hundred times the context of run C.** If it also gave the worse
  answer, then you have just watched context work against you, not for you. The model
  had everything it needed in run A &mdash; it also had two large data files, forty
  sample consignments and a stale notes document.

- **Run C had the least and knew the most**, because you did the thinking: you chose
  which six lines mattered. That is the trade the whole tier is about. Column three
  is cheapest and requires you to know your codebase; column one is most convenient
  and requires nothing.

- **The stale document is in run A.** `docs/tariff-2026-notes.md` says fuel applies to
  the base alone &mdash; which is exactly what `manifest.py` does. If run A told you
  `manifest.py` was correct, it was not hallucinating. It was reading a document you
  gave it, that happens to be wrong. **That is what "attach everything" means.**

- **Neither B nor C can tell you which one is right.** Both files are internally
  consistent. Only the runbook settles it, and only if you attach the runbook and not
  the notes. Deciding *which* source is authoritative is your job and stays your job.

## Stretch

Run A again, but exclude the two `data/*.json` files and `docs/tariff-2026-notes.md`.
Meter it first. You have removed most of the tokens and the single wrong document.
Does it now match run B? That is the shape of a well-chosen `.gitignore` for context
&mdash; and the first thing to reach for when someone says "the tool is not good at
our codebase".
