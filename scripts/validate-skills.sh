#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0

for skill_md in "$repo_dir"/skills/*/SKILL.md; do
  [ -f "$skill_md" ] || continue
  skill_dir="$(basename "$(dirname "$skill_md")")"
  if ! grep -q '^---$' "$skill_md"; then
    echo "missing frontmatter fence: $skill_md"
    status=1
  fi
  if ! grep -q "^name: $skill_dir$" "$skill_md"; then
    echo "name does not match directory: $skill_md"
    status=1
  fi
  if ! grep -q '^description: ' "$skill_md"; then
    echo "missing description: $skill_md"
    status=1
  fi
done

exit "$status"
