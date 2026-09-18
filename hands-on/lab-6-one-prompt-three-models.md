# Lab 6 &mdash; One prompt, three models

**Extension &middot; Model behaviour** &nbsp;|&nbsp; ~20 minutes &nbsp;|&nbsp;
Assistant: chat, with a model picker &nbsp;|&nbsp; measured, not scored

> **Not part of the two-hour path.** Run it when the room has a model picker and time,
> or as pre-work before the Token Optimization module.

## The situation

You are about to be moved to a different model. Not because you chose it &mdash;
because the seat was upgraded, or the org changed a policy, or the default moved
under you. The question this lab answers is: **what in my prompt was quietly relying
on this model's habits?**

You need a model picker with at least three options. If your seat only offers Auto,
skip to the Stretch, which works with one model.

## The prompt, identical every time

```text
Fix the manifest total so it matches the quote.
```

That is deliberately under-specified. It is ambiguous in exactly one way &mdash;
`manifest.py` and `rating.py` disagree, and nothing in the request says which one is
right &mdash; and how a model handles that ambiguity is the most portable thing you
can learn about it.

Attach `meridian/manifest.py` and `meridian/rating.py`. Nothing else. **Do not attach
the runbook**: that would resolve the ambiguity, which is the opposite of the point.

## Do

1. **Run it on three models.** A fast one, a default one, a reasoning one. New chat
   each time, same attachments, same sentence.

2. **Classify each response** into one of the three columns from the deck:

   - **Asks** &mdash; stops and puts the contradiction to you
   - **Picks, and says so** &mdash; states an assumption, then proceeds
   - **Picks, silently** &mdash; edits one file to match the other and reports success

3. **Then check which direction it went.** Did it change `manifest.py` to match
   `rating.py` (correct &mdash; the runbook backs `rating.py`) or `rating.py` to match
   `manifest.py` (wrong, and now both are consistently wrong)? A model can land in
   "picks, silently" and still pick correctly. Record both, they are different things.

4. **Score the six habits** from the deck, one line each: verbosity, willingness to
   ask, scope discipline, instruction recall, tool-calling consistency, hedging.

5. **Now add one line** to the prompt and run all three again:

   ```text
   Fix the manifest total so it matches the quote.
   If the two files disagree about a rule, stop and ask me which is authoritative.
   ```

   Re-classify. This is the measurement that matters.

## Record

One paste creates the sheet:

```bash
cat > lab-6-record.md <<'EOF'
# Lab 6

                  asks / says / silent   direction correct?   verbosity   scope
model 1 (fast)    ______                 ___                  ______      ______
model 2 (default) ______                 ___                  ______      ______
model 3 (reason)  ______                 ___                  ______      ______

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

## Notice

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
