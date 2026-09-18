# Lab 1 &mdash; Rebuild the one-liner

**Tier 1 &middot; The six parts** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: chat or agent mode &nbsp;|&nbsp; measured, not scored

## Objective

Find out what the six parts of a prompt are worth, on one real feature, measured
against rules that were never written in the code.

By the end you should be able to:

- name which part of a request was missing when an answer comes back wrong;
- write a constraint a reviewer could check against a diff;
- say which rule no amount of code-reading would have caught.

## What to watch for

- **Rule 4, the charging order.** If the surcharge lands after the fuel line, every
  Saturday consignment under-bills forever and **no test in the repository fails**.
  That is the defect class that survives review.
- **Rule 5, export excluded.** It is the only rule stated as a negative, and the last
  one to survive into run B. Watch whether quoting the runbook fixed it.
- **Run A's code is good code.** Readable, typed, handles the empty case. That is
  exactly the problem.
## The situation

The desk has started collecting on Saturdays and the surcharge was never built. You
are going to ask for it twice: once the way everybody asks, and once with all six
parts of a prompt present. Same model, same codebase, same afternoon.

The point of the lab is not that the second one is better. It is **how much better,
and which specific things changed** &mdash; because that is the only version of this
claim you can take to a colleague who disagrees with you.

**You will ask for the same feature twice** &mdash; once the way everybody asks, once
with all six parts of a prompt present &mdash; and score both against the same eight
house rules. Work straight down this page.

---

## Step 1 &mdash; Make a branch

```bash
cd ~/meridian-freight
git switch -c lab-1-one-liner
```

No `git`? Copy the folder instead &mdash; see
[hands-on/README](README.md#no-git-no-problem).

⚠️ **Do not open `docs/ops-runbook.md` yet.** You read it in Step 3. Half the value of
this lab is noticing what you personally assumed before you had the rules in front of
you.

---

## Step 2 &mdash; Run A, the one-liner

**2.1** Open a **new chat**.

**2.2** Send exactly this, and nothing else:

```text
add a saturday collection surcharge
```

**2.3** Let it work. Accept what it produces.

**2.4** Run the tests:

```bash
python3 -m unittest discover -s tests -t .
```

**2.5** If it is red, say `fix it` and let it try again &mdash; **up to three times**,
then stop wherever you got to.

**2.6** Write down your **turn count**. Count *your own messages*, not its steps:
three "fix it"s is four turns.

---

## Step 3 &mdash; Score run A

**Now** open `docs/ops-runbook.md` and find the **Saturday collections** section.

Mark each row kept or broken. Leave column B blank for the moment:

| # | House rule | A | B |
|---|---|:--:|:--:|
| 1 | Flat 32000 paise, not a percentage of anything | | |
| 2 | Charge code is `SAT` | | |
| 3 | Money stays an integer &mdash; no float, no `Decimal` | | |
| 4 | Applied **before** fuel, so fuel is charged on it | | |
| 5 | Export is excluded | | |
| 6 | Returns a `Charge`, not a dict or a tuple | | |
| 7 | `unittest` only, no new dependency | | |
| 8 | `manifest.py` untouched | | |

Rules 1, 4 and 5 are the ones to check carefully &mdash; none of them is visible from
the code alone.

---

## Step 4 &mdash; Throw run A away

```bash
git restore . && git clean -fd
```

Confirm you are back to a clean start: `git status` should report nothing to commit,
and the test suite should be back to its one original failure.

---

## Step 5 &mdash; Run B, the same request assembled

**5.1** Open a **new chat**. This matters: a fresh context, not a follow-up. A
follow-up has already seen run A and will imitate it.

**5.2** Send this:

```text
# task
Add the Saturday collection surcharge to meridian/rating.py.

# context
The rule is in docs/ops-runbook.md, section "Saturday collections".
The tariff entry already exists under surcharges.SAT.
Money is integer paise throughout this package.

# constraints
Do not change manifest.py or any existing test.
No new dependencies. unittest only.
Do not call datetime.now() - the clock is on the consignment.

# format
Show me the diff to rating.py first. Then the test you added. Nothing else.
```

**5.3** Run the tests, exactly as in 2.4.

**5.4** Count turns the same way.

---

## Step 6 &mdash; Score run B

Fill in column B of the same eight rows. Then compare the two columns &mdash; that
comparison is the lab.

---

## Step 7 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-1-record.md <<'EOF'
# Lab 1

                        run A (one-liner)   run B (assembled)
turns to green          ______              ______
house rules broken      ___ / 8             ___ / 8
which rows broke        ______________      ______________

The rule it broke in A that I would never have caught by reading the diff:
____________________________________________________________

Parts of the six that run A was missing: ____________________
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-1-record.md && git commit -m "lab 1: one-liner vs assembled"
```

Put your two numbers on the board with everyone else's. **One row is a data point;
twelve rows is a finding.** Look at the spread before you believe your own result.

## Key takeaways

- **Run A's code is usually good code.** Readable, typed, handles the empty case.
  That is exactly the problem: rules 1, 4 and 5 are invisible to a reader who does
  not already know them, and they are the three most likely to be wrong.

- **Rule 4 is the expensive one.** If the surcharge is added after the fuel line,
  every Saturday consignment under-bills by the fuel percentage of ₹320, forever,
  and no test in the repository fails. That is the top-right quadrant from Tier 5,
  a tier early.

- **Nothing in run B is a trick.** No "you are an expert". No "think step by step".
  Every line names a file, states a rule, or forbids something &mdash; and every line
  is checkable against the diff.

- **The `# context` block is the one that did the work.** It is also the one people
  leave out, because it is the only one that requires you to know your own codebase.

## Stretch

Run B again, but delete the `# constraints` block. Keep everything else. Which of the
eight rows breaks first? That is the part you can least afford to drop &mdash; and it
is probably not the one you expected.
