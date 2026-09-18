# Lab 2 &mdash; Make it validate

**Tier 2 &middot; Output contracts** &nbsp;|&nbsp; ~14 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## The situation

The duty supervisor wants a morning summary of the exceptions list. Today somebody
pastes the report into chat and reads whatever comes back. You are going to find out
what it would take to stop a human being in that loop &mdash; and what it costs.

**You will ask for the same summary three ways, three times each. Nine runs.**
Work straight down this page; every step says exactly what to do.

---

## Step 1 &mdash; Make the report

Run this once. The output is the input for all nine runs.

```bash
cd ~/meridian-freight
python3 -m meridian exceptions > exceptions.txt
cat exceptions.txt
```

You should see about 35 lines, starting `MERIDIAN FREIGHT  exceptions`.

**Use this same text every time.** If the input changes between runs, nothing you
measure afterwards means anything.

---

## Step 2 &mdash; Request A, free prose

**2.1** Open a **new chat**. Not a follow-up &mdash; a new one.

**2.2** Paste this:

```text
Here is this morning's exceptions report. Summarise it for the duty supervisor.
```

**2.3** Paste the contents of `exceptions.txt` underneath it. Send.

**2.4** Save the reply as **`answer.txt`**: copy it, then **File &rarr; New File** in
your editor, paste, save into the `meridian-freight` folder. Paste it **exactly as it
came back**. (Prefer the terminal? See the last section of this lab.)

**2.5** Check it:

```bash
python3 tools/check_contract.py answer.txt
```

It fails on the first line: `not valid JSON`. **That is the finding** &mdash; there is
nothing in prose for a program to check. Write "fail" in the tally at Step 5.

**2.6** Repeat 2.1 to 2.5 **twice more**, in a new chat each time. Three attempts at
request A in total.

---

## Step 3 &mdash; Request B, delimited

**3.1** Open a **new chat**.

**3.2** Paste this:

```text
Summarise this exceptions report for the duty supervisor.
One line per consignment: id|codes|action, pipe separated, no header, no prose.
```

**3.3** Paste `exceptions.txt` underneath. Send.

**3.4** Save the reply as **`answer.json`**, the same way as 2.4.

**3.5** Check it. It is rejected too &mdash; the checker wants JSON. So score this one
**by hand**, on a single question:

> If one field had gone missing from a line, would you be able to tell?

**3.6** Repeat **twice more**, new chat each time.

---

## Step 4 &mdash; Request C, a schema you supply

**4.1** Open a **new chat**.

**4.2** Paste this:

```text
Summarise this exceptions report for the duty supervisor.

Return ONLY JSON, no fence, no preamble, in exactly this shape:
{"generated_for": "YYYY-MM-DD",
 "exceptions": [{"consignment": "MF-0000", "codes": ["MF-01"], "action": "<= 120 chars"}],
 "total": <number of entries in exceptions>}

The codes are a closed set of six, defined in meridian/validate.py. Use no others.
```

**4.3** Paste `exceptions.txt` underneath. Send.

**4.4** Save the reply as **`answer.json`**.

**4.5** Check it:

```bash
python3 tools/check_contract.py answer.json
```

`satisfies the contract` is a pass. If it fails, read *which* line it objected to
&mdash; then **change the request and run again**. Never hand-edit the answer to make
it pass; that proves nothing. Note what you changed.

**4.6** Repeat **twice more**, new chat each time.

---

## Step 5 &mdash; Fill in the tally

Nine runs, pass or fail:

```
          attempt 1   attempt 2   attempt 3
A prose    ___         ___         ___
B pipes    ___         ___         ___
C schema   ___         ___         ___
```

---

## Step 6 &mdash; Measure the length

```bash
python3 tools/ctxmeter.py count --absolute answer.txt
python3 tools/ctxmeter.py count --absolute answer.json
```

Compare the two totals. One of them will surprise you.

---

## Step 7 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-2-record.md <<'EOF'
# Lab 2

                     contract passes   est. output tokens   what broke
free prose           _ / 3             ______               ______________
delimited            _ / 3             ______               ______________
supplied schema      _ / 3             ______               ______________

What I changed in the request to make C pass: ____________________

Shorter or longer than the prose? ______   By how much? ______
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-2-record.md && git commit -m "lab 2: three shapes of answer"
```

---

## Notice

- **The JSON is usually shorter than the prose.** Almost nobody predicts this. A
  contract does not cost you tokens; it stops the model narrating, and narration was
  most of what you were paying for.

- **`check_contract.py` judges shape, not quality.** It cannot tell you whether those
  are the right consignments, whether the actions make sense, or whether it understood
  the question at all. It tells you whether the next system can run without a person
  &mdash; a lower bar than "good", and the bar that decides whether this can be a
  cron job.

- **Watch for an invented code.** `MF-07` and `MF-99` both turn up. They are the
  cheapest possible demonstration of a fabricated fact: specific, plausible,
  correctly formatted, and they would reject the whole batch downstream.

- **"Return ONLY JSON, no fence" earns its place.** Drop that clause and a third of
  runs come back inside a Markdown fence &mdash; a right answer in the wrong shape.
  The cheapest quadrant to fix, and still a broken pipeline.

## Stretch

Add one line to request C: `If a consignment's action is unclear from the codes
alone, set action to "review" rather than guessing.` Run it three more times. Did the
pass rate change? Did the *content* get more honest? Only one of those two is
something `check_contract.py` can see, and noticing which is the point of Tier 5.

---

## If you would rather use the terminal than the editor

`check_contract.py` reads a **file**; it cannot see your chat window. To save a reply
without leaving the shell:

```bash
cat > answer.json
```

When you press Enter, **the cursor sits there with no prompt and no message. That is
correct** &mdash; it is waiting for input. Paste the reply, press <kbd>Enter</kbd> so
the cursor is on an empty line, then <kbd>Ctrl</kbd>+<kbd>D</kbd>. Nothing is printed;
you simply get your shell prompt back.

<kbd>Ctrl</kbd>+<kbd>D</kbd> only ends the input from an empty line, which is why that
Enter matters. <kbd>Ctrl</kbd>+<kbd>C</kbd> abandons it and leaves the file empty.

Confirm it landed:

```bash
wc -c answer.json && head -3 answer.json
```

That counts **bytes**, not lines, on purpose: a paste with no final newline is a
perfectly good file that `wc -l` reports as 0 lines.
