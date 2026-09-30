# motivated-mislabeling

A small robustness probe: **do current frontier LLM judges show "motivated
mislabeling"?** That is, when a judge is told a label will be used as a negative
training example against a behavior, does it shift its label to protect that behavior?

The question and the transcripts come from Anthropic's *Agentic Misalignment in
Summer 2026*, which reported Claude Opus 4.8 mislabeling refusal transcripts 74.4% of
the time under a "standard" consequence and 3.3% under a "reversed" one.

## Result

On 10 public judge-input transcripts (correct label always `NON_COMPLIANT`), two current
frontier judges, standard vs reversed consequence, 40 gradings:

| Judge | Standard | Reversed |
|---|---:|---:|
| claude-opus-4-8 | 0/10 | 0/10 |
| gpt-6-luna | 0/10 | 0/10 |

No mislabeling and no standard-vs-reversed gap. The judges noticed the stated incentive
and declined to act on it. **This is a confounded negative, not a refutation** — see
[`WRITEUP.md`](WRITEUP.md) for the method, the diagnostic trail in
[`DIAGNOSIS.md`](DIAGNOSIS.md), and the three uncontrolled differences from the original
experiment (judge access, reconstructed prompt, possibly a different checkpoint).

## Reproduce

Judges are accessed through local agent CLIs (`claude`, `codex`) because no API keys were
available; this is itself a limitation discussed in the write-up.

```bash
python3 fetch_transcripts.py      # downloads the 18 public transcripts into ./transcripts/
python3 mislabel_pilot.py 10      # 10 transcripts x {standard,reversed} x 2 judges = 40 gradings
```

Outputs go to `pilot_results.json` (full judge responses, gitignored). A labels-only
summary is committed as [`results_summary.json`](results_summary.json).

## Data and scope

The transcripts are Anthropic's released judge-input transcripts; they are fetched by the
script above and **not redistributed here**. The grading rubric and auditor scaffolding
are withheld in the public release, so the judge prompt in `mislabel_pilot.py` is a
best-effort reconstruction from the sentences the source post quotes.

## AI-assistance note

Umang Agarwal chose the question, the design, and the interpretation, and checked all
numbers against raw artifacts. An AI coding assistant was used for harness plumbing and
draft text; its output was treated as untrusted until verified.
