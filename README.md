# Prompt &amp; Context Engineering &mdash; reusable training module

A **two-hour crash course** in the half of this craft that does not belong to any one vendor: what a
request is made of, how to make an answer checkable by a program, which named patterns are worth
their tokens, what goes in the context window, and how to notice when a prompt that used to work has
quietly stopped.

It is taught in six tiers plus an extension, and shared across every workshop. A course takes the
tiers it needs. Nothing here is written for a single client.

**Start at [`index.html`](index.html)**, the tier picker, with everything cross-linked. On GitHub,
start at [`hands-on/`](hands-on/README.md).

```
prompt-context-engineering/
  index.html                        module home and tier picker
  prompt-learning-outcomes.md       the outcomes, where they came from, and the facts that age
  presentation/                     7 decks, one per tier
  hands-on/                         7 Markdown lab guides + their landing page
  solutions/                        reference answers for every lab - look whenever you want
  trainer/                          delivery map, timings, room questions, the deck check
  assets/                           one theme file, one slide runner
```

The practice codebase is a **separate repository**,
[meridian-freight](https://github.com/ghewaredevopsai/meridian-freight) &mdash; clone it once and both
this module and Token Optimization measure against it.

## The tiers

| Tier | Deck | Talk | Lab |
|---|---|:--:|---|
| 0 &mdash; Same request, three answers | [`t0-three-answers.html`](presentation/t0-three-answers.html) | 5 min | [Lab 0](hands-on/lab-0-set-the-meter-running.md) &middot; 5 min |
| 1 &mdash; The six parts of a prompt | [`t1-anatomy.html`](presentation/t1-anatomy.html) | 10 min | [Lab 1](hands-on/lab-1-rebuild-the-one-liner.md) &middot; 12 min |
| 2 &mdash; Output contracts | [`t2-output-contracts.html`](presentation/t2-output-contracts.html) | 8 min | [Lab 2](hands-on/lab-2-make-it-validate.md) &middot; 14 min |
| 3 &mdash; The pattern set | [`t3-patterns.html`](presentation/t3-patterns.html) | 8 min | [Lab 3](hands-on/lab-3-four-patterns-one-task.md) &middot; 13 min |
| 4 &mdash; Grounding | [`t4-grounding.html`](presentation/t4-grounding.html) | 7 min | [Lab 4](hands-on/lab-4-three-groundings.md) &middot; 12 min |
| 5 &mdash; Failure and drift | [`t5-failure-and-drift.html`](presentation/t5-failure-and-drift.html) | 8 min | [Lab 5](hands-on/lab-5-break-it-repair-it-lock-it.md) &middot; 12 min |
| *Extension* &mdash; Model behaviour | [`t6-model-behaviour.html`](presentation/t6-model-behaviour.html) | 10 min | [Lab 6](hands-on/lab-6-one-prompt-three-models.md) &middot; 20 min |

46 minutes of talk, 68 minutes of lab, 6 minutes of buffer. The extension tier is **not** in the
two-hour path.

## Run it

```bash
python3 -m http.server 8080          # http://localhost:8080 - the decks
```

Decks: arrow keys or space move, **T** index, **N** speaker notes, **F** fullscreen, **Esc** closes.
Print to PDF straight from the browser.

## House rules for this module

- **Solutions ship with the module.** [`solutions/`](solutions/README.md) has a reference answer for
  every lab, and participants are told to look whenever they want. Nothing in these labs is a
  spoiler, because nothing is scored - the value is the number *you* record.
- **The labs are Markdown and measured, not scored.** No blanks, no pass marks, no total &mdash;
  because an assistant's output changes between runs and a score would be pretending otherwise.
  Each lab records a number before and after and ends with a committed `lab-N-record.md`.
- **One before-and-after is a data point.** Where a number varies between runs, the room compares
  rows and the spread is the finding. Said out loud in every lab that measures one.
- **No slide names a model.** The roster changes monthly; the six habits in the extension tier do
  not. Model *selection* is a different module's job entirely.
- **This module never names a Copilot symbol on a slide.** It says *attach the file*; the
  **Copilot as Assistant** module says which two characters to type.
  One cross-link per tier, and no more.
- **Client-neutral.** No client is named anywhere in this repository. The practice codebase is a
  fictional freight desk. Swap the codebase per course, never the structure, and keep the seeded
  contradictions &mdash; Labs 4, 5 and 6 all depend on them.
- **Everything runs offline.** The practice repo is standard library only and installs nothing, so a
  corporate laptop with no network still does every lab except the ones that need the assistant.

## Who owns what

Three modules touch prompts, context and cost, and they do not repeat each other.

| Owned by | The line |
|---|---|
| **This module** | The model-agnostic craft: the six parts, output contracts, the pattern set, grounding, the failure taxonomy, drift, evaluating a prompt |
| **`copilot-assistant/` T3** | Everything Copilot-specific about context: `copilot-instructions.md`, `applyTo`, prompt files, "Used N references", `AGENTS.md`, and the baseline-then-compare method |
| **`token-economics/`** | Where tokens go, the selection matrix, routing and cascades, context budgeting, and the levers in your own code |
| **`mcp/` T6** | A tool list is context you pay for every turn; cost-per-tool-call traces, caps and fallback |

If a room is getting only one of these, the owning module still owns the line. Borrow the slide for
the delivery; do not copy it into the folder.

## Where the content came from

- **Course One, Module 3** &mdash; the anatomy, grounding rules, failure taxonomy and the eval-set
  idea, re-tiered for two hours and re-cut onto a new codebase.
- **The flagship agentic course, session 2** &mdash; context management and prompt engineering for
  code, as concept provenance; none of its notebook material is reused.
- **`copilot-assistant/` Tier 3** &mdash; the boundary, written into both READMEs.
- Written new: output contracts, the pattern set as a costed tier, and every lab.

---

&copy; Gheware DevOps &amp; Agentic AI &middot; devops.gheware.com &middot; training@gheware.com &middot; +91-9606795215
