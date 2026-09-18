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

**Three requests, one run each.** Save each reply under its own name, then let a
script do the measuring.

| | the request | save it as | what you are testing |
|---|---|---|---|
| **A** | ask for a summary | `answer.txt` | free prose &mdash; nothing to check |
| **B** | ask for pipe-separated lines | `answer.delimited` | looks checkable, is not |
| **C** | ask for JSON in a shape you supply | `answer.json` | a contract a program can verify |

## What to watch for

Four things. Note each as it happens &mdash; they are what you discuss afterwards.

1. **Does the reply parse at all?** Run A will not. That is the finding, not a failure.
2. **Does anything wrap the answer?** A ``` fence, or a "Here is the summary:" line.
   A right answer in a wrong shape breaks a pipeline just as thoroughly as a wrong one.
3. **Does a code appear that is not one of the six?** `MF-07` and `MF-99` both turn up.
   Specific, plausible, correctly formatted, and invented.
4. **How the three lengths compare.** Write them down before forming an opinion about
   which shape is "efficient".

Work straight down this page; every step says exactly what to do.

---

## Step 1 &mdash; Make the report

Run this once. The output is the input for all three runs.

```bash
cd ~/meridian-freight
python3 -m meridian exceptions > exceptions.txt
cat exceptions.txt
```

You should see about 35 lines, starting `MERIDIAN FREIGHT  exceptions`.

**Use this same text in all three runs.** If the input changes, nothing you measure
afterwards means anything.

---

## Step 2 &mdash; Request A, free prose

**2.1** Open a **new chat**. Not a follow-up &mdash; a new one.

**2.2** Paste this:

```text
Here is this morning's exceptions report. Summarise it for the duty supervisor.
```

**2.3** Paste the contents of `exceptions.txt` underneath it. Send.

**2.4** Save the reply as **`answer.txt`** in the `meridian-freight` folder &mdash;
copy it, then **File &rarr; New File**, paste, save. Paste it **exactly as it came
back**. (Prefer the terminal? See the last section of this lab.)

---

## Step 3 &mdash; Request B, delimited

**3.1** Open a **new chat**.

**3.2** Paste this:

```text
Summarise this exceptions report for the duty supervisor.
One line per consignment: id|codes|action, pipe separated, no header, no prose.
```

**3.3** Paste `exceptions.txt` underneath. Send.

**3.4** Save the reply as **`answer.delimited`**.

**3.5** Look at it and answer one question, for the record sheet later:

> If one field had gone missing from a line, would you be able to tell?

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

If it fails, read *which* line it objected to, then **change the request and run
again** in a new chat. Never hand-edit the answer to make it pass &mdash; that proves
nothing about what the next run would do. Note what you changed.

---

## Step 5 &mdash; Build the comparison table

You have three files. One command measures all three and checks each against the
contract:

```bash
python3 tools/lab2_report.py
```

```
    shape       file              est. tokens   contract
------------------------------------------------------------------
A   prose       answer.txt                 62   fail (not valid JSON...)
B   delimited   answer.delimited          164   fail (not valid JSON...)
C   schema      answer.json               706   pass

  largest / smallest = 11.4x
```

Your numbers will differ &mdash; the shape of the table will not.

**Prefer to have the assistant do it?** Paste your three answers into a chat with:

```text
Here are three answers to the same request, in three formats. For each, tell me:
the format, roughly how long it is, whether a script could parse it without a
human, and what information the shorter ones dropped to get shorter.
```

Then compare its answer with the script's. Where they disagree, the script is
measuring and the model is estimating &mdash; which is itself worth a minute.

---

## Step 6 &mdash; Read the three lengths

From that table:

- **prose** is the shortest, by a lot
- **delimited** sits in the middle &mdash; one line per consignment, no repeated keys
- **JSON** is the largest, several times the prose

**Before you read the takeaways, answer this for yourself:** the prose is short
because it left something out. What?

---

## Step 7 &mdash; Record

One command writes the sheet, already filled in with your measurements:

```bash
python3 tools/lab2_report.py --record
```

That creates `lab-2-record.md` with the table and three questions left blank. Open
it, answer those three in your own words, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-2-record.md && git commit -m "lab 2: three shapes of answer"
```

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

**A. Does C stay passing?** Run request C twice more, in new chats, saving over
`answer.json` each time and re-running `python3 tools/lab2_report.py`. A contract that
passes once and fails on the third run is not a contract you can schedule &mdash; and
finding that out is worth more than the first pass was.

**B. Make it more honest.** Add one line to request C: `If a consignment's action is
unclear from the codes alone, set action to "review" rather than guessing.` Did the
pass rate change? Did the *content* get better? Only one of those two is something
`check_contract.py` can see, and noticing which is the point of Tier 5.

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
