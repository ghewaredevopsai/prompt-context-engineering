# Learning Outcomes &mdash; Prompt &amp; Context Engineering

*A two-hour crash course &middot; 6 tiers &middot; 6 labs &middot; one extension*

Tick a box (`- [x]`) when you can do the thing **without looking it up**.

This module assumes you write code for a living and have used an assistant in an editor. It does not
re-teach what an LLM is, and it does not teach any vendor's syntax &mdash; see *Boundary* at the foot.

## Progress

| Tier | Outcomes | Lab | Done |
|---|:--:|---|:--:|
| 0 &mdash; Same request, three answers | 3 | Lab 0 | &#9744; |
| 1 &mdash; The six parts of a prompt | 5 | Lab 1 | &#9744; |
| 2 &mdash; Output contracts | 4 | Lab 2 | &#9744; |
| 3 &mdash; The pattern set | 5 | Lab 3 | &#9744; |
| 4 &mdash; Grounding | 5 | Lab 4 | &#9744; |
| 5 &mdash; Failure and drift | 5 | Lab 5 | &#9744; |
| *Extension* &mdash; Model behaviour | 3 | Lab 6 | &#9744; |

## Tier 0 &middot; Same request, three answers

- [ ] Name the four inputs that reach the model on every request, and say which one is not yours.
- [ ] Explain why the same request twice gives different answers, without using the word "random".
- [ ] Rank the three things you control &mdash; what you type, what you attach, what stands &mdash;
      by how much of the request each one is, and say which most teams work on first.

**Lab evidence**
- [ ] Lab 0 &mdash; you have a measured baseline for the practice repository and you read the
      estimator's footer before quoting its number.

## Tier 1 &middot; The six parts of a prompt

- [ ] Name all six parts and the specific failure each one prevents.
- [ ] Given a bad answer, name which part was missing rather than rewording the whole request.
- [ ] Write a constraint that a reviewer could check against a diff, and say why
      "be careful with money" is not one.
- [ ] Decide which parts of a request should stop being typed and become a file.
- [ ] Explain why "you are an expert Python developer" and "think step by step" are not in the
      assembled version.

**Lab evidence**
- [ ] Lab 1 &mdash; the same task run bare and assembled, with turns and house-rule violations for
      both, and you can name the rule that no amount of code-reading would have caught.

## Tier 2 &middot; Output contracts

- [ ] Ask for an answer in a shape a program can check, and say what "only JSON, no fence" is for.
- [ ] Explain why a delimited format fails more dangerously than prose.
- [ ] State precisely what a shape validator can and cannot tell you about an answer.
- [ ] Repair a failed contract by changing the request rather than the output, and say why the
      other way proves nothing.

**Lab evidence**
- [ ] Lab 2 &mdash; three shapes of answer measured side by side, and you can say what the
      contract costs and what it buys.

## Tier 3 &middot; The pattern set

- [ ] Describe few-shot, decomposition, chain of thought and self-critique in terms of what each
      one does mechanically.
- [ ] Say what each costs, in tokens or in turns, and give a task where that cost is worth paying.
- [ ] Explain why explicit chain of thought is mostly obsolete against a reasoning model.
- [ ] Say why none of the four should be permanently on in a prompt file.
- [ ] Ask for the test first, and say why that beats every pattern above for catching wrong code.

**Lab evidence**
- [ ] Lab 3 &mdash; defects found against tokens spent for four patterns, and a stated choice of which
      one you will use at work and for what.

## Tier 4 &middot; Grounding

- [ ] Draw the context window as a budget and name what is in it before you have typed anything.
- [ ] Choose between pasting the lines, pointing at files, and letting it search &mdash; and justify
      the choice in terms of both precision and cost.
- [ ] Explain why the cheapest bundle often gives the best answer, with a number rather than an opinion.
- [ ] Recognise that a stale document in the bundle is worse than no document.
- [ ] Say which of these decisions stays a human's job and cannot be delegated.

**Lab evidence**
- [ ] Lab 4 &mdash; one question grounded three ways, with tokens sent and whether the real defect was
      found, and you can say what the largest bundle spent its attention on instead.

## Tier 5 &middot; Failure and drift

- [ ] Name four classes of failure and the different tell each one has.
- [ ] Say which class survives code review, and why "read more carefully" is not the counter for it.
- [ ] Name three directions a working prompt rots from, including the one nobody diffs.
- [ ] Explain why a green test suite is not evidence when the model wrote both the code and the test.
- [ ] Write a check row that is machine-checkable, and recognise when you cannot &mdash; and say
      which human owns that judgement instead.

**Lab evidence**
- [ ] Lab 5 &mdash; a working prompt broken three prescribed ways and repaired, plus a
      `prompt-check.md` whose unwritable rows you can account for.

## Extension &middot; Model behaviour

- [ ] Name six habits that differ between models, and the one line of prompt that pins each.
- [ ] Classify a response to an ambiguous request as asks / says-so / silent, and say why silent
      and correct is the dangerous combination.
- [ ] Say what belongs in a behaviour write-up and what belongs in a model-selection decision.

**Lab evidence**
- [ ] Lab 6 &mdash; one prompt against three models, classified, then re-run with one line added, and
      you can name the habit you were relying on without realising.

## Where these outcomes came from

| Source | What it contributed |
|---|---|
| Course One, Module 3 (*Prompt &amp; Context Engineering*, 35 slides) | The anatomy as "six parts, and the failure each prevents", the grounding rules, the four-failure taxonomy, and the eval-set idea behind Tier 5. Re-tiered from a two-day course into two hours and re-cut onto a new codebase. |
| Course One, Module 1 | Session hygiene and the argument that a long conversation costs more and signals less. Tier 4's budget picture. |
| Flagship agentic course, session 2 | *Context Management* and *Prompt Engineering for Code* as concept provenance. None of its notebook material is reused &mdash; it is stdlib simulation, not assistant work. |
| Three-day Copilot course, block 1.1 | The four labs the client was promised: teardown and rewrite, a schema-valid JSON contract, the instructions file, break and repair. The instructions-file one is delegated, not rebuilt. |
| `copilot-assistant/` Tier 3 | The boundary. Everything about *which file* and *what syntax* stays there; this module cross-links rather than repeating, and both READMEs say so. |
| `token-economics/` | The habit of deriving a number from a run rather than asserting it, and the disclaimer discipline that `ctxmeter` inherits. |
| Written new, September 2026 | Output contracts as a tier, the pattern set costed rather than listed, the portability argument in the extension tier, and all seven labs. |

## Facts that age

Checked 18 September 2026. Re-read this list before a delivery.

- **Chain of thought.** Tier 3 calls explicit CoT mostly obsolete against a reasoning model. That is
  true of current reasoning models and was not true two years ago. If the room is on an older or
  smaller model, it is still worth teaching as a live technique.
- **`ctxmeter`'s calibration** was measured on 18 September 2026 against two BPE tokenizers. The
  measured error is in the practice repo's `tools/calibration.md`. Re-run it after any large change
  to that repository, and update the date.
- **The estimator is not a tokenizer**, and no vendor's true tokenizer is available to a participant
  on a corporate laptop. Every number in these labs is a floor and a comparison, never a bill.
- **Model habits** in the extension tier have a shelf life of roughly one model release. The six
  habits are stable; which model shows which is not, and no slide names one.

## Boundary

This module owns the model-agnostic craft. **How to write the files** &mdash;
`.github/copilot-instructions.md`, `*.instructions.md` and `applyTo`, prompt files, confirming an
instruction file was used &mdash; is **Copilot as Assistant**
Tier 3. **Which model, and what it costs** is **Token Optimization**.
**What a tool list costs you per turn** is **MCP** Tier 6.
