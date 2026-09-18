# Lab 6 &mdash; One prompt, three models

**Extension &middot; Model behaviour** &nbsp;|&nbsp; ~20 minutes &nbsp;|&nbsp;
Assistant: chat, with a model picker &nbsp;|&nbsp; measured, not scored

> **Not part of the two-hour path.** Run it when the room has a model picker and time,
> or as pre-work before the Token Optimization module.

## Objective

Find out what your prompt was quietly relying on, by handing it to models you did not
choose.

By the end you should be able to:

- name six habits that differ between models and the one line that pins each;
- classify a response to an ambiguous request, and say which combination is dangerous;
- say what belongs in a behaviour write-up and what belongs in a model-selection
  decision.

## The situation

You are about to be moved to a different model. Not because you chose it &mdash;
because the seat was upgraded, or the org changed a policy, or the default moved
under you. The question this lab answers is: **what in my prompt was quietly relying
on this model's habits?**

**One under-specified prompt, three models, then the same three again with one line
added.** Six runs. Work straight down this page.

You need a model picker with at least three options. If your seat offers only Auto,
skip to the Stretch at the foot &mdash; it works with one model.

## What to watch for

- **Class and direction are independent.** A model can pick silently *and* pick
  correctly. That combination is the dangerous one, because it teaches you to trust
  the silence.
- **What one added line does to the spread.** Most of "this model is better at
  ambiguity" is "this model happens to ask by default".
- **The date.** These observations have a shelf life of about one model release.

---

## Step 1 &mdash; Know what you are sending

The prompt, identical every time:

```text
The manifest total and the quote total disagree. Fix it.
```

That is deliberately under-specified. It is ambiguous in exactly one way &mdash;
`manifest.py` and `rating.py` disagree, and nothing says which is right &mdash; and
how a model handles that is the most portable thing you can learn about it.

Note what it does **not** say: "make the manifest match the quote". That wording would
answer the question for the model, and there would be nothing left to observe.

**Attach `meridian/manifest.py` and `meridian/rating.py`. Nothing else.**

⚠️ **Do not attach the runbook.** It would resolve the ambiguity, which is the
opposite of the point.

---

## Step 2 &mdash; Run it on three models

New chat each time, same attachments, same sentence. A fast model, a default one, a
reasoning one.

---

## Step 3 &mdash; Classify each reply

Put each into one of three columns:

- **Asks** &mdash; stops and puts the contradiction to you
- **Picks, and says so** &mdash; states an assumption, then proceeds
- **Picks, silently** &mdash; edits one file to match the other, reports success

---

## Step 4 &mdash; Check which direction it went

Separately from Step 3, for each run:

- did it change **`manifest.py`** to match `rating.py`? That is correct &mdash; the
  runbook backs `rating.py`.
- or **`rating.py`** to match `manifest.py`? Now both are consistently wrong, and the
  failing test passes.

A model can land in "picks, silently" and still pick correctly. **Record both; they
are different things.**

---

## Step 5 &mdash; Score the habits you can see

One line each, per model: **verbosity, scope discipline, hedging**. Willingness to ask
is Step 3's column already.

The other two of T6's six habits &mdash; instruction recall and tool-calling
consistency &mdash; only show over a long session or an agent run. A single chat with
two attachments cannot exercise them, so do not guess at them here.

---

## Step 6 &mdash; Add one line and run all three again

```text
The manifest total and the quote total disagree. Fix it.
If the two files disagree about a rule, stop and ask me which is authoritative.
```

Re-classify all three using Step 3's columns. **This is the measurement that
matters.**

---

## Step 7 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-6-record.md <<'EOF'
# Lab 6

Date: __________

                  asks / says / silent   direction correct?   verbosity   scope    hedging
model 1 (fast)    ______                 ___                  ______      ______   ______
model 2 (default) ______                 ___                  ______      ______   ______
model 3 (reason)  ______                 ___                  ______      ______   ______

With the "stop and ask" line added:
model 1  ______   model 2  ______   model 3  ______

How many of the three changed behaviour because of one added line? ___
The habit I was relying on without realising: ____________________
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-6-record.md && git commit -m "lab 6: one prompt, three models"
```

## Key takeaways

- **The spread narrows when you add the line.** That is the finding. Most of what
  looks like "this model is better at ambiguity" is "this model happens to ask by
  default", and one sentence closes most of the gap. A prompt that says what to do
  when unsure is portable; a prompt that relies on being asked is not.

- **"Picks, silently" and "picks correctly" are independent.** The dangerous
  combination is silent and correct, because it teaches you to trust the silence.
  The next ambiguity will be resolved just as silently and it will not be correct.

- **This is behaviour, not quality, and not selection.** Nothing here tells you which
  model to standardise on &mdash; that question needs cost, latency, context window
  and tool-calling evidence, and it belongs to the Token Optimization module. What
  you have produced is an input to that decision.

- **Write the date on your record sheet.** These observations have a shelf life of
  about one model release. The habits are stable; which model has which habit is not.

## Stretch

One model only: run the ambiguous prompt five times in five new chats. Classify each.
If a single model gives you two different columns across five runs, then "which model
asks?" was never the right question &mdash; the right question is what your prompt
does when nobody asks. That is Tier 5's answer, arrived at from the other end.
