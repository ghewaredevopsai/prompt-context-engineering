# Prompt &amp; Context Engineering &mdash; delivery map

**Trainer-facing, and it ships with the module.** There are no lab spoilers here: the labs are
measured rather than scored, and the reference answers are published in `../solutions/`. Two hours, six tiers, six labs.
Written 18 September 2026.

## 1. Timing

| Tier | Talk | Lab | Running |
|---|:--:|:--:|:--:|
| 0 &mdash; Same request, three answers | 5 | 5 | 0:10 |
| 1 &mdash; The six parts of a prompt | 10 | 12 | 0:32 |
| 2 &mdash; Output contracts | 8 | 14 | 0:54 |
| 3 &mdash; The pattern set | 8 | 15 | 1:17 |
| 4 &mdash; Grounding | 7 | 12 | 1:34 |
| 5 &mdash; Failure and drift | 8 | 12 | 1:54 |
| Buffer / questions | | 6 | **2:00** |
| *Extension &mdash; Model behaviour* | *10* | *20* | *2:30* |

**46 min talk / 68 min lab / 6 min buffer &mdash; 40.4% theory on teaching time.**

The buffer is a row in this table on purpose. 48/72 sums to exactly 120 and leaves nothing for a
question, a laptop that will not clone, or the two minutes it takes twelve people to put rows on a
board. It will be used every time.

**Slide pace is ~1.9 min/slide** across 24 slides. If you find yourself at 3 min/slide you are
teaching the lab from the front; stop and let them run it.

## 2. Audience to tier

| Audience | Tiers |
|---|---|
| Engineers using an assistant daily (the common case) | T0&ndash;T5, full |
| A room that only writes chat prompts, no pipeline | T0&ndash;T3, stop after the pattern set |
| A team building something that consumes model output | T0, T2, T4, T5 &mdash; contracts and drift are the whole job |
| Architects and leads, no hands-on | T0, T4, T5 talks only; show Lab 4's table rather than running it |
| A room that has just done Copilot as Assistant T3 | Skip nothing, but say in T1 slide 4 that the files are theirs already |

**T4 is the tier people wrongly cut**, because "attach less" sounds like an optimisation rather than a
correctness argument. It is the only tier that produces a number the room will repeat to a colleague.

## 3. The 90-minute Course Three path

Day 1 is 09:00&ndash;19:00 with a fixed 4-hour block 1.3. Three 2-hour blocks leave no lunch. For
that delivery, run **90 minutes**:

1. Drop the extension tier entirely (it is already out of the 2h path).
2. Run **Lab 3 as a demo from the front** &mdash; you run two patterns, the room watches and fills in
   the sheet. Saves 13 minutes and loses least, because Lab 3's finding is a ratio they can read.
3. Trim T1 to 7 minutes by cutting slide 4 (*Two of the six should never be typed twice*) **if and
   only if** Copilot as Assistant T3 is being delivered in the same day &mdash; that slide is the
   cross-link, and without T3 in the room it has to stay.

That lands at 90 minutes with Labs 0, 1, 2, 4 and 5 intact. **Do not buy time from Lab 4.**

## 4. What the labs actually produce

Deterministic, identical in every room, safe to quote from the front:

| Measurement | Value |
|---|---|
| Practice repo, everything attached | ~52,000 est. tokens |
| `naive.txt` bundle | ~38,400 |
| `minimal.txt` (rating.py + manifest.py) | ~2,200 |
| Six runbook lines + the failing test output | ~300 |
| Test suite | 27 tests, exactly 1 failure |
| The failing assertion | `113987 != 114655` |
| Lab 2 answer sizes, run 1 | prose 125 / delimited 169 / **JSON 707** &mdash; ratio 5.7x |
| Lab 2 answer sizes, run 2 | prose 450 / delimited 226 / **JSON 846** &mdash; ratio 1.9x |

**Not deterministic, and the labs say so:** turns to green, house rules broken, contract pass rate,
whether a given run names the drift. Put these on a board and read the spread. If you quote a single
participant's number as a result you have taught the opposite of Tier 5.

### The three defects in `manifest.py`

Lab 3 says "at least three". They are: fuel applied to the base alone rather than base plus
surcharges; `OVERSIZE` omitted entirely; `INSURANCE` omitted entirely. The band lookup is also
duplicated, including the 1 kg short-circuit, which is a fourth answer and a good one.

### Lab 2: the contract is LONGER, and that is the lesson

⚠️ An earlier version of Tier 2 and Lab 2 claimed the JSON was the *shortest* of the
three shapes. It is not: on this report it is about **five and a half times** the
prose. Prose groups and discards per-consignment detail; JSON enumerates sixteen rows
and repeats the keys on each. If anyone saw the old wording, correct it out loud.

⚠️ **And do not replace it with "5x" either.** Two measured runs gave 5.7x and 1.9x,
and the prose-versus-delimited order swapped between them. **Only one thing is stable:
the JSON is the largest**, for the structural reason that it enumerates every row and
repeats the keys.

Say "between about two and six times, depending on how much it narrates", then **ask
the room for their ratios and put them on a board.** The spread is the lesson, and it
is the same lesson as Tier 5's about n=1. Output tokens bill at roughly 6x input, so
the difference is a real invoice line on anything run at volume.

### Why `ctxmeter diff` refuses a percentage on the flagship cut

`naive.txt` is 64% data by tokens; `minimal.txt` is 100% code. The estimator's error does not cancel
across that, so it declines to print a headline percentage without `--allow-mixed`. **This is a
feature and a teaching beat** &mdash; when it fires in Lab 4's stretch, stop and read the message
aloud. It is the tool refusing to let someone screenshot a number.

## 5. Room questions to expect

*"Isn't this just writing a good ticket?"* &mdash; Yes, largely, and say so. The difference is that a
colleague fills gaps from shared context and asks when stuck; a model fills them from a million other
codebases and does not. That is the whole argument for the `# context` block.

*"Our prompts are in a wiki, is that not the same as a prompt file?"* &mdash; A wiki page is not
reviewed when the code changes and cannot be invoked by name. The mechanism belongs to the Copilot as
Assistant module; here, just note that a prompt nobody can review is a prompt nobody owns.

*"Which model should we use?"* &mdash; Not this module. Hand it to Token Optimization, and resist
answering even though you know. Answering here is how the boundary erodes.

*"Won't the model just get better and make this unnecessary?"* &mdash; The four hidden inputs from T0
do not go away with model quality, and neither does a stale document in the bundle. Better models
raise the floor on the bottom-left quadrant of T5 and do very little for the top-right one.

*"We are told not to paste our code into a model at all."* &mdash; A real constraint, and the honest
answer is that Tier 4 becomes more important, not less: pasting six lines of a runbook is a very
different governance conversation from attaching a repository.

## 6. Facts that age, and slide notes

- **T3 calls explicit chain of thought mostly obsolete.** True against current reasoning models.
  If the room is on a small or older model, say it is still live for them.
- **No slide names a model.** Keep it that way when asked directly &mdash; the six habits in the
  extension tier are stable, the rankings are not.
- **`ctxmeter` calibration is dated 18 Sep 2026** in the practice repo's `tools/calibration.md`.
  Re-run it after any large change to that repo and update the date. A calibration nobody re-ran is
  a claim.
- **The `data/model-runs.json` file in the practice repo is SYNTHETIC** and labelled so in the file.
  It is used by the Token Optimization module, not this one, but if anyone opens it here, say so
  immediately. Replace it with recorded runs before anyone quotes a row.

**Re-measure these before a delivery**, and after any change to the practice repo or to
`ctxmeter`'s constants:

```bash
cd ../meridian-freight
python3 tools/ctxmeter.py repo --absolute | grep TOTAL
for b in everything naive minimal; do
  python3 tools/ctxmeter.py count --absolute $(grep -v '^#' tools/bundles/$b.txt) | grep TOTAL
done
```

⚠️ These figures moved once already: they were first written against the uncalibrated
estimator, and recalibrating it changed every one of them by 10-50%. A number quoted on
a slide and never re-derived is the exact failure this module teaches people to avoid.

## 7. Before a delivery

- [ ] `python3 check-decks.py` &rarr; **0 problems** on all seven decks
- [ ] Clone the practice repo fresh and confirm **27 tests, 1 failure**
- [ ] `python3 tools/ctxmeter.py repo --absolute` still gives ~52,000 &mdash; if it has moved, update
      section 4 and Lab 4's slide numbers in T4 slide 4
- [ ] Run Labs 1 and 4 with live Copilot and time them. **The lab minutes above are estimates and
      have not been rehearsed against a live assistant.**
- [ ] Leak scan (below) prints nothing
- [ ] Confirm the room has an assistant; Labs 1&ndash;5 do not work without one

## 8. Before you push

Run the leak scan from the trainer's local notes (`../../trainer-private/leak-scan.sh`). Its pattern
list names clients and internal systems, so the list itself does not ship with this repository.

Check authorship too: `git log --format='%an %ae'`.
