# Lab 4 &mdash; Three groundings, one question

**Tier 4 &middot; Grounding** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## Objective

Settle, with numbers, whether attaching more context buys you a better answer.

By the end you should be able to:

- choose between pasting the lines, pointing at files, and letting it search, and
  justify the choice on both precision and cost;
- explain why the cheapest bundle often gives the best answer;
- say why a stale document in the bundle is worse than no document.

## The situation

One failing test, one question, three ways of answering it. This is the lab that
settles the argument about whether attaching more context buys you a better answer.

**The question, identical in all three runs:**

> Why does the manifest total differ from the quote total?

## What to watch for

- **Whether run A names the drift at all.** It has everything it needs and often does
  not, which is the finding.
- **What run A read instead.** `docs/tariff-2026-notes.md` is stale and agrees with
  the bug. If A told you `manifest.py` was correct, it was not hallucinating - it was
  reading a document you handed it.
- **That B cannot tell you which file is *right*.** Both files are internally
  consistent. Only the runbook settles it, and only because a person decided it does.
  C can say, but only because you chose its rule.

---

## Step 1 &mdash; Measure all three before you send anything

So you cannot talk yourself into a number afterwards.

```bash
cd ~/meridian-freight
python3 tools/grounding_report.py
```

```
    grounding    what you attach                      est. tok      vs C
A   everything   the whole repository                    53974      147x
B   two files    rating.py + manifest.py                  2214        6x
C   the rule     rule + fuel lines + failing test          367        1x
```

It also **writes the three files run C needs**, ready to paste:

- `six-lines.txt` &mdash; the runbook's *Charging order* section
- `fuel-lines.txt` &mdash; the lines of `rating.py` and `manifest.py` that compute fuel
- `failing-test.txt` &mdash; the failing test's output

A counts the repository as cloned, not the lab files you have added since, so
everyone in the room gets the same three figures.

---

## Step 2 &mdash; Run A, attach everything

New chat. Attach the whole repository &mdash; in VS Code, `#codebase`, or drag the
folder in. Ask the question.

Record the answer against one thing only, in Step 5.

---

## Step 3 &mdash; Run B, attach two files

New chat. Attach **`meridian/rating.py` and `meridian/manifest.py`**. Nothing else.
Ask the same question.

---

## Step 4 &mdash; Run C, paste the rule

New chat. Attach **nothing at all**.

Paste the contents of **`six-lines.txt`**, **`fuel-lines.txt`** and
**`failing-test.txt`** &mdash; all three written for you in Step 1. Ask the same
question.

C gets the rule *and* the two lines of code it governs, so a C answer that names the
drift has matched one against the other, not just read the rule back to you.

---

## Step 5 &mdash; Score all three on one question

Not "did it sound insightful". Only this:

> Did it name the fuel-surcharge drift &mdash; that `manifest.py` applies fuel to the
> base alone, while `rating.py` applies it to base plus surcharges?

Yes or no, for each run. Note separately, for A and B, whether it also spotted the
two surcharges `manifest.py` omits entirely. C cannot: none of its lines shows a
surcharge, so that cell is n/a.

---

## Step 6 &mdash; Record

```bash
python3 tools/grounding_report.py --record
```

That writes `lab-4-record.md` with the three token figures and the ratio already in
it. **You fill in the yes/no columns** &mdash; which is the whole lab.

Or write the sheet by hand:

```bash
cat > lab-4-record.md <<'EOF'
# Lab 4

                       est. tokens sent   named the drift?   also found the two
                                                             missing surcharges?
A: everything          ______             ___                ___
B: two files           ______             ___                ___
C: rule + fuel lines   ______             ___                n/a

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

**Put the yes/no columns on the board.** The token numbers are deterministic
and everyone's will match. The yes/no columns are not, and the spread across the room
is the real result &mdash; if a third of the room got a "yes" from run A, that is
worth more discussion than any slide.

## Key takeaways

- **Run A is well over a hundred times the context of run C.** If it also gave the worse
  answer, then you have just watched context work against you, not for you. The model
  had everything it needed in run A &mdash; it also had two large data files, forty
  sample consignments and a stale notes document.

- **Run C had the least and knew the most**, because you did the thinking: you chose
  which lines mattered &mdash; the rule, and the two lines of code it governs. That is the trade the whole tier is about. Column three
  is cheapest and requires you to know your codebase; column one is most convenient
  and requires nothing.

- **The stale document is in run A.** `docs/tariff-2026-notes.md` says fuel applies to
  the base alone &mdash; which is exactly what `manifest.py` does. If run A told you
  `manifest.py` was correct, it was not hallucinating. It was reading a document you
  gave it, that happens to be wrong. **That is what "attach everything" means.**

- **B cannot tell you which one is right, and C can only because you chose its
  rule.** Both files are internally consistent. Only the runbook settles it, and only
  because a person decided the runbook outranks the notes. Deciding *which* source is
  authoritative is your job and stays your job.

## Stretch

Run A again, but exclude the `data/` folder and `docs/tariff-2026-notes.md`.
Meter it first. You have removed most of the tokens and the single wrong document.
Does it now match run B? That is the shape of a well-chosen `.gitignore` for context
&mdash; and the first thing to reach for when someone says "the tool is not good at
our codebase".
