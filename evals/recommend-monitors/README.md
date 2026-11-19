# Eval: recommend-monitors

A fixture app with known gaps and a checklist of what a good plan contains.

## Run it

Use a fresh agent session for each run, in any agent. Start both from `fixtures/orders-app`.

1. **Baseline (no skill):** make sure the skill is not installed, then paste the prompt from [scenario.md](scenario.md).
2. **With the skill:** install it (`./install.sh` from the repo root), restart the agent, paste the same prompt.
3. Score each answer against [expected.md](expected.md). Record the baseline failures verbatim; the skill must fix exactly those.
4. Repeat 3 times per condition. If the answers differ a lot between runs, the wording is not binding yet.

## What to look for

- Does the skill trigger from the prompt alone (it does not name the skill)?
- Does the plan follow the output order, include the JSON block, and agree with its own table?
- Did the agent create or change anything? It must not.

Add a scenario here for every failure you see in real use, then fix the skill.
