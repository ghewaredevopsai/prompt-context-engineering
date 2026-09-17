# Lab 0 &mdash; Set the meter running

**Tier 0 &middot; Same request, three answers** &nbsp;|&nbsp; ~5 minutes &nbsp;|&nbsp;
No assistant needed &nbsp;|&nbsp; measured, not scored

## The situation

You have just been handed the freight desk codebase. Before you ask an assistant
anything about it, you are going to find out what "just attach the repository" would
cost you &mdash; because for the rest of this module, every number you record is
compared against the one you write down now.

## Do

1. **Clone it and prove it runs.**

   ```bash
   git clone https://github.com/ghewaredevopsai/meridian-freight
   cd meridian-freight
   python3 -m unittest discover -s tests -t .
   ```

   You should see **27 tests** and **exactly one failure**, in `test_manifest.py`.
   More or fewer than one means something has drifted &mdash; say so now, not in
   Lab 4, which depends on that failure being there.

2. **Look at what failed, and do not fix it.**

   ```
   AssertionError: 113987 != 114655
   ```

   The manifest says the depot should collect ₹1,139.87. The quote says ₹1,146.55.
   Six rupees and change, on every consignment that carries a surcharge. Write down
   what you think is going on in one line. You will find out in Lab 4 whether you
   were right.

3. **Meter the repository.**

   ```bash
   python3 tools/ctxmeter.py repo --absolute
   ```

   Read the itemised list, not just the total. One file is over a fifth of the whole
   repository on its own.

4. **Read the footer.** All six lines of it. That footer is the reason the numbers
   in this module can be trusted for what they are used for, and the reason they
   cannot be used for anything else.

## Record

Create `lab-0-record.md` in the repository root and fill it in:

```markdown
# Lab 0

Tests: __ passed, __ failed
Whole repository: __________ est. tokens
Largest single file: ______________ at ______ est. tokens (__% of the repo)
My guess at the failing test: ____________________________________

The one line from the ctxmeter footer I would quote to my team:
____________________________________________________________
```

```bash
git add lab-0-record.md && git commit -m "lab 0: baseline"
```

## Notice

- **`ctxmeter` made you pass `--absolute`.** It refuses to print a single total
  without being asked twice, because a number from an estimator is exactly the kind
  of thing that ends up in someone's slide deck as a fact. Everything else in this
  module uses `diff`, which is the honest verb.

- **Two data files are nearly half the repository.** Neither of them has anything to
  do with how the desk prices freight &mdash; they are the freight. Every time
  somebody says "just give it the whole repo", that is mostly what they are sending.

- **You have not asked the model anything yet**, and you already know the most
  important number in the module.

## Stretch

Run `python3 tools/ctxmeter.py turns tools/bundles/naive.txt --turns 10` and look at
the cumulative column. Then answer, out loud, to whoever is next to you: *why is the
tenth turn of a conversation more expensive than the first, when you typed less?*
