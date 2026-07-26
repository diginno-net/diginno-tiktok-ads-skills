#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_dir="${OPENCODE_SKILLS_DIR:-$HOME/.config/opencode/skills/marketing-content/paid-ads}"
codex_skills_dir="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
sync_script="$HOME/.config/opencode/scripts/skills-audit/link-skills.sh"

mkdir -p "$target_dir"

for skill_dir in "$repo_dir"/skills/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  rm -rf "$target_dir/$skill_name"
  cp -R "$skill_dir" "$target_dir/$skill_name"
  echo "installed $skill_name -> $target_dir/$skill_name"
done

if [ -x "$sync_script" ]; then
  "$sync_script" "$codex_skills_dir"
else
  echo "sync script not found or not executable: $sync_script"
  echo "manual Codex sync may be required"
fi
