# Lab 1 &mdash; Rebuild the one-liner

**Tier 1 &middot; The six parts** &nbsp;|&nbsp; ~12 minutes &nbsp;|&nbsp;
Assistant: chat or agent mode &nbsp;|&nbsp; measured, not scored

## The situation

The desk has started collecting on Saturdays and the surcharge was never built. You
are going to ask for it twice: once the way everybody asks, and once with all six
parts of a prompt present. Same model, same codebase, same afternoon.

The point of the lab is not that the second one is better. It is **how much better,
and which specific things changed** &mdash; because that is the only version of this
claim you can take to a colleague who disagrees with you.

## Before you start

```bash
cd meridian-freight
git switch -c lab-1-one-liner          # or copy the folder, see hands-on/README.md
```

**Do not read `docs/ops-runbook.md` yet.** Read it after run A. Half the value of
this lab is noticing what you personally assumed.

## Do

1. **Run A &mdash; the one-liner.** Open a **new chat**. Send exactly this and nothing
   else:

   ```text
   add a saturday collection surcharge
   ```

   Let it work. Accept what it produces. Run the tests. If it is red, say "fix it"
   and let it try again &mdash; up to three times, then stop and record where you got to.

   **Count your own messages**, not its steps. Three "fix it"s is four turns.

2. **Score run A against the checklist.** Now open `docs/ops-runbook.md` and find the
   Saturday collections section. Mark each row broken or kept:

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

3. **Reset.**

   ```bash
   git restore . && git clean -fd
   ```

4. **Run B &mdash; the same request, assembled.** Open a **new chat** again (this
   matters: a fresh context, not a follow-up). Send:

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

   Run the tests. Count turns the same way.

5. **Score run B** against the same eight rows.

## Record

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

## Notice

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
