# skills

Revido's shared skills for coding agents. One repo, one source of truth, works in Claude Code, Codex, Cursor, Gemini CLI and OpenCode.

Skills use the open [Agent Skills](https://agentskills.io) format: `skills/<name>/SKILL.md` with `name` and `description`, plus optional `references/`, `assets/` and `scripts/`.

## Skills

| Skill | Use it when |
|---|---|
| [`recommend-monitors`](skills/recommend-monitors/SKILL.md) | An app is going live or under a support plan and you need the monitors, priorities and dev tasks, as a plan to approve and a JSON block the Revido portal can read |

## Install

Clone the repo, then:

```bash
./install.sh                 # link every skill into ~/.agents/skills and ~/.claude/skills
./install.sh --project DIR   # copy them into an app's .agents/skills and .claude/skills (commit them)
./install.sh --dry-run       # show what would happen
./install.sh --uninstall     # remove the links
```

| Agent | Reads | Covered by |
|---|---|---|
| Codex, Cursor, Gemini CLI, OpenCode | `.agents/skills` | the `~/.agents/skills` link |
| Claude Code | `.claude/skills` | the `~/.claude/skills` link (symlinks are followed) |
| Cursor, OpenCode | also `.claude/skills` | either link |

Claude Code users can instead install it as a plugin (auto-updates):

```bash
claude plugin marketplace add Revido-LLC/skills
claude plugin install revido-skills@revido
```

Updating a linked install is `git pull`. Restart the agent after adding a new skill folder.

Working inside this repo needs nothing: `.agents/skills` and `.claude/skills` link to `skills/`.

## Check

```bash
python3 scripts/validate.py
```

Checks frontmatter against the portable format, name and folder match, description rules, size limits, links and JSON. CI runs it on every push.

## Contribute

Read [AGENTS.md](AGENTS.md). In short: write the eval scenario first, watch an agent fail without the skill, then write the smallest skill that fixes it.
