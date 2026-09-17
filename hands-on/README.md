# Six labs, one freight desk

Every lab in this module is done against [Meridian Freight
Desk](https://github.com/ghewaredevopsai/meridian-freight) &mdash; a small, fictional
internal service with real house rules that were never written down anywhere a
program can read.

## How these labs work

- **Measured, not scored.** There is no `[PASS]`/`[FAIL]` and no total. Each lab asks
  you to write down a number before you change anything, and the same number after.
  The comparison is the result.
- **The record sheet is the deliverable.** Every lab ends with you committing a
  `lab-N-record.md`. Nobody grades your prompt; the sheet is what you take back to
  work, and it is what makes "it felt better" into something you can show someone.
- **n = 1.** One before-and-after is a data point, not a result. Where a lab measures
  something non-deterministic &mdash; turns, credits &mdash; the room puts its rows on
  the board at the end and the **spread across a dozen people** is the finding. Your
  own row on its own proves very little, and the labs say so where it matters.
- **You need Copilot** (or another assistant) in your editor for Labs 1&ndash;5. Lab 0
  and every `tools/` command run offline with Python 3 alone.
- **Nothing is installed.** The practice repo is standard library only, on purpose:
  a corporate laptop with no network still does every lab.

## No git? No problem

Several labs branch and reset. If `git` is unavailable or restricted on your machine,
copy the folder instead:

```bash
cp -r meridian-freight meridian-freight-lab1      # instead of: git switch -c lab-1
```

and work in the copy. Every instruction below that says "restore" means "delete the
copy and make a fresh one".

## The labs

| Lab | Tier | Time | What you do | What you record |
|---|---|:--:|---|---|
| [0](lab-0-set-the-meter-running.md) | 0 | 5 min | Clone, run the tests, meter the repository | Whole-repo estimate, tests passing |
| [1](lab-1-rebuild-the-one-liner.md) | 1 | 12 min | Send a one-liner, then the same request assembled | Turns to green, house rules broken |
| [2](lab-2-make-it-validate.md) | 2 | 14 min | Ask for a summary three ways, validate each | Contract pass rate, output length |
| [3](lab-3-four-patterns-one-task.md) | 3 | 13 min | Few-shot, decomposition, chain of thought, self-critique | Defects found, tokens per pattern |
| [4](lab-4-three-groundings.md) | 4 | 12 min | One question, three sizes of context | Estimated tokens, did it find the drift |
| [5](lab-5-break-it-repair-it-lock-it.md) | 5 | 12 min | Break a working prompt three ways, then write checks | Violations before/broken/repaired |
| [6](lab-6-one-prompt-three-models.md) | Ext | 20 min | The same prompt against three models | Which habits differed |

Lab 6 is the extension lab and is not part of the two-hour path.

**[`../solutions/`](../solutions/README.md) has a reference answer for every lab.** Look whenever you
want - before, during or after. None of these labs is scored, so there is nothing to spoil; the
value is the number you record, not whether it matches the folder.

## Getting started

```bash
git clone https://github.com/ghewaredevopsai/meridian-freight
cd meridian-freight
python3 -m unittest discover -s tests -t .
```

You need: **Python 3.11+**, an editor with an AI assistant, and about ninety minutes
of lab time. You do not need a network connection for the tools, and you do not need
to install anything.

**One test fails when you clone it.** That is not your machine. It is the lab.
