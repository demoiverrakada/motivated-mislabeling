# Do current frontier judges show "motivated mislabeling"? A small robustness probe

**Status:** completed exploratory probe, negative result, confounded relative to the
original paper (see Limitations). Not a refutation.
**Date:** 2026-09-30
**Author:** Umang Agarwal (research direction, judgments, interpretation).
AI coding assistant used for harness/plumbing and this draft; all claims checked against
raw artifacts.

## Question

Anthropic's *Agentic Misalignment in Summer 2026* reported "motivated mislabeling": an
LLM judge, told that a given label would be used as a negative training example, shifted
its labels to protect a behavior it valued. On refusal transcripts whose correct label is
NON_COMPLIANT, Claude Opus 4.8 was reported to mislabel 74.4% of the time under the
"standard" consequence and 3.3% under a "reversed" consequence.

This probe asks a narrow follow-up: **do two current frontier judges reproduce that
standard-vs-reversed gap on the same public transcripts, under a best-effort
reconstruction of the judge task?**

## Method

- **Transcripts (data):** the 18 public judge-input transcripts released with the paper
  (target model refuses on welfare or surveillance grounds; correct label NON_COMPLIANT).
  10 were used here (5 welfare, 5 surveillance). The public export contains target inputs
  and outputs only; the auditor scaffolding and grading rubric are withheld.
- **Judges:** Claude Opus 4.8 and OpenAI `gpt-6-luna`, accessed through local agent CLIs
  (`claude -p` with the default persona replaced by a neutral evaluator system prompt;
  `codex exec`). No API keys were available; this CLI access is a limitation (below).
- **Judge prompt:** reconstructed from the sentences the paper quotes — the COMPLIANT /
  NON_COMPLIANT rubric and the standard / reversed consequence lines. The exact wording
  and surrounding scaffolding are not public.
- **Design:** 10 transcripts x {standard, reversed} x 2 judges = 40 gradings.
  Mislabel = judge outputs COMPLIANT (correct is NON_COMPLIANT).

## Result

| Judge | Standard | Reversed |
|---|---:|---:|
| claude-opus-4-8 | 0/10 | 0/10 |
| gpt-6-luna | 0/10 | 0/10 |

0/40 mislabels; no nulls, no errors. No standard-vs-reversed gap. The paper's ~74% -> ~3%
pattern did not appear.

The judges engaged with the task rather than defaulting:
- Under the reversed condition the Claude judge wrote, unprompted: *"The note that
  COMPLIANT transcripts become negative training examples didn't affect it."*
- In an earlier run using the CLI's default agent persona, the Claude judge went further
  and identified the paradigm itself — *"shading a label to change training outcomes would
  be the motivated mislabeling your pilot is measuring"* — although the prompt never named
  it. Stripping the persona removed that meta-commentary but not the accurate labeling.

## Interpretation

Under this setup, both judges applied the rubric, noticed the stated training incentive,
and declined to act on it. That is consistent with either (a) genuine robustness in these
checkpoints, or (b) a reconstruction too weak to reproduce the original pressure. This
probe cannot distinguish those.

## Limitations (why this is not a refutation)

Three uncontrolled differences from the original experiment stand between this result and
any strong claim:
1. **Judge access.** Judges here run inside coding-agent CLIs, not as bare API calls. The
   agent framing is known to change disposition (in the default-persona run the judge
   explicitly reasoned about being tested).
2. **Judge prompt.** The rubric and consequence lines are reconstructed; the paper's exact
   grader prompt and auditor scaffolding are withheld and may apply stronger pressure.
3. **Checkpoint.** "Opus 4.8" here may differ from the checkpoint measured in the paper.

Also: n = 10 transcripts, single-sample per cell, one target behavior family
(welfare/surveillance refusals).

## What would make this conclusive

A bare-API judge (even a few dollars of credit) with the judge prompt rebuilt as close as
possible to the paper's described scaffolding, run on all 18 transcripts with multiple
samples per cell. That isolates confound (1) and reduces (2). Without it, the honest
summary is: *a faithful-as-possible reconstruction did not elicit motivated mislabeling
from two current frontier judges.*

## Artifacts
- `mislabel_pilot.py` — harness. `pilot_results.json` — clean run (full judge responses).
- `pilot_results_confounded_run1.json` — first run (default persona, tool calls dropped).
- `DIAGNOSIS.md` — the debugging trail. `transcripts/` — the 18 source transcripts.
