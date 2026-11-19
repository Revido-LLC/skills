#!/usr/bin/env python3
"""Validate every skill under skills/ against the portable Agent Skills format
plus this repo's conventions (see AGENTS.md). Standard library only.

Usage: python3 scripts/validate.py [path/to/skills]
Exit code is 1 if any error is found.
"""
import json
import re
import sys
from pathlib import Path

# Fields every agent understands. Anything else (e.g. Claude Code's
# `context: fork` or `when_to_use`) is not portable and would be ignored,
# or rejected, elsewhere.
PORTABLE_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
WARN_DESCRIPTION = 500
MAX_BODY_LINES = 500
RESERVED_NAMES = {"synced"}  # Claude Code reserves this folder name


def parse_frontmatter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.S)
    if not m:
        return None, text
    fm, key = {}, None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0] in " \t":  # nested map or folded continuation
            if key is not None and isinstance(fm[key], str):
                fm[key] = (fm[key] + " " + line.strip()).strip()
            continue
        k, _, v = line.partition(":")
        key, v = k.strip(), v.strip()
        if v in (">", "|", ">-", "|-"):
            v = ""
        if len(v) > 1 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        fm[key] = v
    return fm, m.group(2)


def check_skill(skill_dir, errors, warnings):
    name_on_disk = skill_dir.name
    skill_md = skill_dir / "SKILL.md"
    where = f"{skill_dir.name}/SKILL.md"
    if not skill_md.is_file():
        errors.append(f"{skill_dir.name}: missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        errors.append(f"{where}: missing YAML frontmatter")
        return

    unknown = sorted(set(fm) - PORTABLE_KEYS)
    if unknown:
        errors.append(f"{where}: non-portable frontmatter keys {unknown} (allowed: {sorted(PORTABLE_KEYS)})")

    name = fm.get("name", "")
    if not name:
        errors.append(f"{where}: missing name")
    else:
        if not NAME_RE.match(name):
            errors.append(f"{where}: name '{name}' must be lowercase letters, digits and single hyphens")
        if len(name) > MAX_NAME:
            errors.append(f"{where}: name longer than {MAX_NAME} characters")
        if name != name_on_disk:
            errors.append(f"{where}: name '{name}' must match folder '{name_on_disk}'")
        if name in RESERVED_NAMES:
            errors.append(f"{where}: '{name}' is a reserved name")

    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{where}: missing description")
    else:
        if len(desc) > MAX_DESCRIPTION:
            errors.append(f"{where}: description is {len(desc)} chars (max {MAX_DESCRIPTION})")
        elif len(desc) > WARN_DESCRIPTION:
            warnings.append(f"{where}: description is {len(desc)} chars; aim for under {WARN_DESCRIPTION}")
        if not desc.startswith("Use when"):
            errors.append(f"{where}: description must start with 'Use when' (triggers only, no workflow summary)")

    lines = text.count("\n") + 1
    if lines > MAX_BODY_LINES:
        errors.append(f"{where}: {lines} lines (max {MAX_BODY_LINES}); move detail into references/")

    # Relative markdown links must resolve.
    for md in skill_dir.rglob("*.md"):
        for target in re.findall(r"\]\(([^)\s]+)\)", md.read_text(encoding="utf-8")):
            if re.match(r"^(https?:|mailto:|#)", target):
                continue
            path = target.split("#", 1)[0]
            if path and not (md.parent / path).exists():
                errors.append(f"{md.relative_to(skill_dir.parent)}: broken link '{target}'")

    # JSON assets must parse.
    for js in skill_dir.rglob("*.json"):
        try:
            json.loads(js.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{js.relative_to(skill_dir.parent)}: invalid JSON ({e})")


def check_plugin(root, errors):
    plugin = root / ".claude-plugin" / "plugin.json"
    market = root / ".claude-plugin" / "marketplace.json"
    names = {}
    for label, p in (("plugin.json", plugin), ("marketplace.json", market)):
        if not p.is_file():
            continue
        try:
            names[label] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f".claude-plugin/{label}: invalid JSON ({e})")
    if "plugin.json" in names and "marketplace.json" in names:
        entries = {e.get("name") for e in names["marketplace.json"].get("plugins", [])}
        if names["plugin.json"].get("name") not in entries:
            errors.append("marketplace.json: no plugin entry matches the name in plugin.json")


def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "skills"
    errors, warnings = [], []
    dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir() and not p.name.startswith("."))
    if not dirs:
        errors.append(f"no skills found in {skills_dir}")
    for d in dirs:
        check_skill(d, errors, warnings)
    check_plugin(root, errors)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(dirs)} skill(s) checked, {len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
