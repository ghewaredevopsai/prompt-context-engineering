# Lab 0 &mdash; Set the meter running

**Tier 0 &middot; Same request, three answers** &nbsp;|&nbsp; ~5 minutes &nbsp;|&nbsp;
No assistant needed &nbsp;|&nbsp; measured, not scored

## Objective

Establish the numbers every later lab is compared against, and meet the instrument
you will be quoting all day.

By the end you should be able to:

- say what "just attach the repository" costs, with a figure;
- name the single largest file in it, and whether it has anything to do with the
  logic you care about;
- state what the estimator cannot see, without looking it up.

## The situation

You have just been handed the freight desk codebase. Before you ask an assistant
anything about it, you are going to find out what "just attach the repository" would
cost you &mdash; because for the rest of this module, every number you record is
compared against the one you write down now.

**You will clone the codebase, run its tests, and measure what "just attach the
repository" costs.** Work straight down this page.

## What to watch for

- **One file is about a fifth of the repository.** Note which, and ask yourself
  whether a question about pricing logic needs it.
- **The tool made you type `--absolute`.** That is deliberate. Ask why before you
  read the footer.
- **The test that fails.** You are not fixing it today. Write down what you think it
  is; Lab 4 tells you whether you were right.

---

## Step 1 &mdash; Clone it

```bash
cd ~
git clone https://github.com/ghewaredevopsai/meridian-freight
cd meridian-freight
```

---

## Step 2 &mdash; Run the tests

```bash
python3 -m unittest discover -s tests -t .
```

You should see **28 tests** and **exactly one failure**, in `test_manifest.py`.

More or fewer than one failure means something has drifted &mdash; say so now, not in
Lab 4, which depends on that failure being there.

---

## Step 3 &mdash; Look at what failed, and do not fix it

Scroll up in that output to the assertion:

```
AssertionError: 113987 != 114655
```

The manifest says the depot should collect &#8377;1,139.87. The quote says
&#8377;1,146.55. Six rupees and change, on every consignment that carries a surcharge.

**Write down in one line what you think is going on.** You will find out in Lab 4
whether you were right.

---

## Step 4 &mdash; Meter the repository

```bash
python3 tools/ctxmeter.py repo --absolute
```

Read the **itemised list**, not just the total at the bottom. Note which single file
is the largest, and what share of the repository it is on its own.

---

## Step 5 &mdash; Read the footer

All six lines of it, printed under every `ctxmeter` run.

That footer is the reason the numbers in this module can be trusted for what they are
used for &mdash; and the reason they cannot be used for anything else. Pick the one
line you would quote to your own team; you will write it down in the next step.

---

## Step 6 &mdash; Record

One paste creates the sheet:

```bash
cat > lab-0-record.md <<'EOF'
# Lab 0

Tests: __ passed, __ failed
Whole repository: __________ est. tokens
Largest single file: ______________ at ______ est. tokens (__% of the repo)
My guess at the failing test: ____________________________________

The one line from the ctxmeter footer I would quote to my team:
____________________________________________________________
EOF
```

Fill in the blanks in any editor, then commit it &mdash; the sheet is the
deliverable, not your memory of the run:

```bash
git add lab-0-record.md && git commit -m "lab 0: baseline"
```

## Key takeaways

- **`ctxmeter` made you pass `--absolute`.** It refuses to print a single total
  without being asked twice, because a number from an estimator is exactly the kind
  of thing that ends up in someone's slide deck as a fact. Everything else in this
  module uses `diff`, which is the honest verb.

- **Three data files are nearly half the repository.** None of them is pricing
  *logic*: two are the tariff and forty sample consignments, and the third is run
  history kept for another module. A question about how the desk prices freight needs
  a few lines of the tariff at most. Every time somebody says "just give it the whole
  repo", that is mostly what they are sending.

- **You have not asked the model anything yet**, and you already know the most
  important number in the module.

## Stretch

Run `python3 tools/ctxmeter.py turns tools/bundles/naive.txt --turns 10` and look at
the cumulative column. Then answer, out loud, to whoever is next to you: *why is the
tenth turn of a conversation more expensive than the first, when you typed less?*
