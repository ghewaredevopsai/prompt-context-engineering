# Lab 2 &mdash; Make it validate

**Tier 2 &middot; Output contracts** &nbsp;|&nbsp; ~14 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## The situation

The duty supervisor wants a morning summary of the exceptions list. Today somebody
pastes the report into chat and reads whatever comes back. You are going to find out
what it would take to stop a human being in that loop &mdash; and what it costs.

## Before you start

```bash
cd meridian-freight
python3 -m meridian exceptions > /tmp/exceptions.txt
cat /tmp/exceptions.txt
```

That output is the input for every run below. Use the same text every time.

## Do

You will ask for the same summary **three ways**, and run each answer through the
same checker.

### Getting an answer into a file

`check_contract.py` reads a file. It cannot see your chat window, so each time a run
comes back you have to save the reply first. In a terminal:

```bash
cat > answer.json
```

Paste the reply, press <kbd>Enter</kbd>, then <kbd>Ctrl</kbd>+<kbd>D</kbd> to finish.
Saving it from your editor works just as well.

**Paste it exactly as it came back** &mdash; including a ``` fence if there is one,
and any "Here is the summary:" line before it. Whether that material is there is part
of what you are measuring; tidying it up by hand throws away the result.

Then check it:

```bash
python3 tools/check_contract.py answer.json
```

Use `answer.txt` for run 1, which is prose rather than JSON.

1. **Run 1 &mdash; free prose.** New chat.

   ```text
   Here is this morning's exceptions report. Summarise it for the duty supervisor.
   ```

   Paste the report underneath. Save what comes back. Run the checker on it. It will
   fail at the first line, and **that is the finding**: there is nothing to check.

2. **Run 2 &mdash; delimited.** New chat.

   ```text
   Summarise this exceptions report for the duty supervisor.
   One line per consignment: id|codes|action, pipe separated, no header, no prose.
   ```

   Save it. The checker will still reject it &mdash; it wants JSON. Score this run by
   hand instead: can you name a field that is missing, or would a dropped field just
   shift the columns silently?

3. **Run 3 &mdash; a schema you supply.** New chat.

   ```text
   Summarise this exceptions report for the duty supervisor.

   Return ONLY JSON, no fence, no preamble, in exactly this shape:
   {"generated_for": "YYYY-MM-DD",
    "exceptions": [{"consignment": "MF-0000", "codes": ["MF-01"], "action": "<= 120 chars"}],
    "total": <number of entries in exceptions>}

   The codes are a closed set of six, defined in meridian/validate.py. Use no others.
   ```

   Run the checker. If it fails, **change the request, not the answer**, and run
   again. Note what you changed.

4. **Run each of the three twice more**, so you have three attempts at each shape.
   Same text, new chat each time.

5. **Measure the length.**

   ```bash
   python3 tools/ctxmeter.py count --absolute answer.json
   ```

   Do the same for your run-1 prose answer.

## Record

One paste creates the sheet:

```bash
cat > lab-2-record.md <<'EOF'
# Lab 2

                     contract passes   est. output tokens   what broke
free prose           _ / 3             ______               ______________
delimited            _ / 3             ______               ______________
supplied schema      _ / 3             ______               ______________

What I changed in the request to make run 3 pass: ____________________

Shorter or longer than the prose? ______   By how much? ______
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-2-record.md && git commit -m "lab 2: three shapes of answer"
```

## Notice

- **The JSON is usually shorter than the prose.** Almost nobody predicts this. A
  contract does not cost you tokens; it stops the model narrating, and narration is
  most of what you were paying for.

- **`check_contract.py` judges shape, not quality.** Read its docstring. It cannot
  tell you whether those are the right consignments, whether the actions make sense,
  or whether it understood the question. It tells you whether the next system can run
  without a person. That is a lower bar than "good" &mdash; and it is the bar that
  decides whether this can be a cron job.

- **Watch for an invented code.** `MF-07` and `MF-99` both turn up. They are the
  cheapest possible demonstration of a fabricated fact: specific, plausible,
  formatted correctly, and it would reject the whole batch downstream.

- **"Return ONLY JSON, no fence" earns its place.** Drop that clause and a third of
  runs come back inside a Markdown fence, which is a right answer in the wrong shape
  &mdash; the cheapest quadrant to fix, and still a broken pipeline.

## Stretch

Add one line to the run-3 request: `If a consignment's action is unclear from the
codes alone, set action to "review" rather than guessing.` Run it three more times.
Did the contract pass rate change? Did the *content* get more honest? Only one of
those two is something `check_contract.py` can see, and noticing which is the
point of Tier 5.
