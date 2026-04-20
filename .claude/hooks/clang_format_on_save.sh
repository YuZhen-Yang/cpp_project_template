#!/usr/bin/env bash
# PostToolUse hook: run clang-format on C++ files after Write/Edit.
# Reads Claude Code hook JSON from stdin.

if ! command -v jq &>/dev/null; then
  echo "Warning: jq not found. Please install jq to enable clang-format hook." >&2
  exit 0
fi

if ! command -v clang-format &>/dev/null; then
  echo "Warning: clang-format not found. Please install clang-format." >&2
  exit 0
fi

input=$(cat)

f=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.filePath // empty' 2>/dev/null)

case "$f" in
  *.cpp|*.h|*.hpp|*.cc|*.cxx)
    clang-format -i "$f"
    ;;
esac