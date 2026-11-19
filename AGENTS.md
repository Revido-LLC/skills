# Skills repo: conventions for any coding agent

This repo holds every skill Revido's coding agents use. One source of truth: `skills/<name>/SKILL.md`.
It must work in Claude Code, Codex, Cursor, Gemini CLI and OpenCode.

## Rules for every skill

1. **Portable frontmatter only:** `name`, `description`, and optionally `license`, `compatibility`, `metadata`, `allowed-tools`. Claude-only fields (`context: fork`, `when_to_use`, `paths`, ...) are ignored or rejected elsewhere. `scripts/validate.py` enforces this.
2. **`name` equals the folder name:** lowercase letters, digits and single hyphens, at most 64 characters.
3. **`description` says only when to use it.** Start with "Use when", name the triggers and symptoms, never summarize the workflow (agents follow the summary and skip the body). Aim for under 500 characters; the hard limit is 1024.
4. **`SKILL.md` stays under 500 lines.** Put detail in `references/` (read on demand), templates in `assets/`, and code in `scripts/`. Link one level deep with relative paths.
5. **Say actions, not tools.** Write "read the file", "dispatch a subagent", not `Read` or `Agent`. Subagents are not available everywhere, so every skill must also work done in one thread.
6. **No secrets, ever.** Tokens come from environment variables.
7. **Recommend before acting.** A skill that can change production state asks for approval first.

## Adding or changing a skill

1. Write the scenario and expected result under `evals/<skill>/` first.
2. Run it without the skill and note what the agent gets wrong (the baseline).
3. Write the smallest skill that fixes those failures. Run again with it.
4. `python3 scripts/validate.py` must pass.

## Layout

```
skills/<name>/SKILL.md      the skill
skills/<name>/references/   detail loaded on demand
skills/<name>/assets/       templates and schemas
evals/<name>/               scenarios, fixtures, expected results
.claude-plugin/             Claude Code marketplace manifest
install.sh                  links skills into every agent's folder
```
