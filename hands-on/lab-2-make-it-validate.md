# Lab 2 &mdash; Make it validate

**Tier 2 &middot; Output contracts** &nbsp;|&nbsp; ~14 minutes &nbsp;|&nbsp;
Assistant: chat &nbsp;|&nbsp; measured, not scored

## Objective

Find out what it takes to get an answer a **program** can act on, instead of one a
person has to read &mdash; and what that costs.

By the end of this lab you should be able to:

- ask for an answer in a shape a script can verify, and say what each clause of that
  request is doing;
- state precisely what a shape validator can and cannot tell you;
- put a number on what a contract costs, and say what it buys.

## The situation

The duty supervisor wants a morning summary of the exceptions list. Today somebody
pastes the report into chat and reads whatever comes back. You are going to find out
what it would take to take the human out of that loop.

## What you will do

**Three requests, three attempts each. Nine runs.**

| | the request | what you are testing |
|---|---|---|
| **A** | ask for a summary | free prose &mdash; nothing to check |
| **B** | ask for pipe-separated lines | delimited &mdash; looks checkable, is not |
| **C** | ask for JSON in a shape you supply | a contract a program can verify |

## What to watch for

Four things. Note each one as it happens &mdash; they are what you discuss afterwards.

1. **Does the reply parse at all?** Run A will not. That is the finding, not a failure.
2. **Does anything wrap the answer?** A ``` fence, or a "Here is the summary:" line.
   That is a right answer in a wrong shape, and it breaks a pipeline just as
   thoroughly as a wrong one.
3. **Does an exception code appear that is not one of the six?** `MF-07` and `MF-99`
   both turn up. Specific, plausible, correctly formatted, and invented.
4. **How the three lengths compare.** Write the numbers down before you form an
   opinion about which shape is "efficient".

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

Compare the two totals. **The JSON will be several times larger** &mdash; write down
the ratio, because the Notice section below is about what that buys you.

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

JSON vs prose: ______ times larger.   What does that buy? ______________
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-2-record.md && git commit -m "lab 2: three shapes of answer"
```

---

## Key takeaways

1. **Shape is not quality, and shape is what you can automate.** `check_contract.py`
   cannot tell you whether those are the right consignments or whether the actions
   make sense. It tells you whether the next step can run without a person &mdash; a
   lower bar than "good", and the one that decides whether this can be a cron job.

2. **A contract costs about five times the prose.** On this report &mdash; 16
   exceptions &mdash; prose meters around 125 est. tokens, delimited 169, and the JSON
   about 707. **Machine readability is bought, not free.**

3. **Those are two different answers, not two renderings of one.** Prose is short
   because it *groups*: "eight are MF-03". JSON enumerates all sixteen and repeats the
   keys on every row. That is why it costs more, and why it is the only one the next
   system can act on per consignment. Since output tokens bill at roughly six times
   input, a contract you run thousands of times a day is a real invoice line.

4. **The delimited format is the trap.** It looks structured and it is the one teams
   reach for first. A missing field shifts every column silently and nothing raises.
   It fails quietly, which is the worst property a format can have.

5. **Repair the request, never the answer.** Hand-editing an answer to make the
   checker pass proves nothing about what the next run will do.

6. **"Return ONLY JSON, no fence" earns its place.** Drop that clause and a third of
   runs come back fenced. One clause, one whole class of failure removed.

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
