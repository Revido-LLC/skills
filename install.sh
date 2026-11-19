#!/usr/bin/env bash
# Install every skill in this repo for all coding agents.
#
#   Codex, Cursor, OpenCode, Gemini CLI read  ~/.agents/skills   (project: .agents/skills)
#   Claude Code reads                         ~/.claude/skills   (project: .claude/skills)
#   Cursor and OpenCode also read ~/.claude/skills, and Claude Code follows symlinks,
#   so installing into both folders covers every agent.
#
# Usage:
#   ./install.sh                       link all skills into your user-level folders
#   ./install.sh --project DIR         copy all skills into DIR/.agents/skills and DIR/.claude/skills
#   ./install.sh --project DIR --link  symlink instead of copy (don't commit these)
#   ./install.sh --uninstall           remove symlinks this script made (add --project DIR for a project)
#   ./install.sh --dry-run             print what would happen
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$REPO/skills"
PROJECT=""
MODE=""
UNINSTALL=0
DRY=0
TAG=""

while [ $# -gt 0 ]; do
  case "$1" in
    --project) PROJECT="${2:?--project needs a directory}"; shift 2 ;;
    --link) MODE=link; shift ;;
    --copy) MODE=copy; shift ;;
    --uninstall) UNINSTALL=1; shift ;;
    --dry-run) DRY=1; TAG="(dry run) "; shift ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

if [ -n "$PROJECT" ]; then
  PROJECT="$(cd "$PROJECT" && pwd)"
  DESTS=("$PROJECT/.agents/skills" "$PROJECT/.claude/skills")
  : "${MODE:=copy}"   # project folders get committed, so copy by default
else
  DESTS=("$HOME/.agents/skills" "$HOME/.claude/skills")
  : "${MODE:=link}"
fi

run() { if [ "$DRY" -eq 1 ]; then echo "  ${TAG}would: $*"; else "$@"; fi; }

for dest in "${DESTS[@]}"; do
  echo "== $dest"
  [ "$UNINSTALL" -eq 1 ] || run mkdir -p "$dest"
  for skill in "$SRC"/*/; do
    name="$(basename "$skill")"
    target="$dest/$name"
    if [ "$UNINSTALL" -eq 1 ]; then
      if [ -L "$target" ] && [ "$(readlink "$target")" = "${skill%/}" ]; then
        run rm "$target"; echo "  ${TAG}removed $name"
      elif [ -e "$target" ]; then
        echo "  ${TAG}skipped $name (not a link made by this script; remove it by hand)"
      fi
      continue
    fi
    if [ -L "$target" ] && [ "$(readlink "$target")" = "${skill%/}" ]; then
      echo "  ${TAG}ok      $name (already linked)"
    elif [ -e "$target" ] || [ -L "$target" ]; then
      if [ "$MODE" = copy ] && [ ! -L "$target" ]; then
        run rm -rf "$target"; run cp -R "${skill%/}" "$target"; echo "  ${TAG}updated $name"
      else
        echo "  ${TAG}skipped $name (already exists and is not ours; remove it to replace)"
      fi
    elif [ "$MODE" = link ]; then
      run ln -s "${skill%/}" "$target"; echo "  ${TAG}linked  $name"
    else
      run cp -R "${skill%/}" "$target"; echo "  ${TAG}copied  $name"
    fi
  done
done
