#!/bin/bash
# Daily Facebook routine runner (invoked by launchd: com.adamboehrer.fb-daily).
# Launches Claude Code headless to run the /fb-daily skill on this machine,
# using the locally logged-in Playwright browser session.
#
# NOTE: This drives Adam's real Facebook account. If Facebook throws a
# login/checkpoint, the skill detects it, writes daily_status.md, and stops —
# Adam then logs in once and the next day's run resumes.

set -euo pipefail

REPO="/Users/adamboehrer/Desktop/Claude Code"
LOG_DIR="$HOME/Library/Logs"
STAMP="$(date '+%Y-%m-%d %H:%M:%S')"

cd "$REPO"

echo "[$STAMP] fb-daily run starting" >> "$LOG_DIR/fb-daily.log"

# Resolve the claude binary (login shells put it on PATH; fall back to common paths).
CLAUDE_BIN="$(command -v claude || true)"
[ -z "$CLAUDE_BIN" ] && [ -x "$HOME/.claude/local/claude" ] && CLAUDE_BIN="$HOME/.claude/local/claude"
[ -z "$CLAUDE_BIN" ] && [ -x "/opt/homebrew/bin/claude" ] && CLAUDE_BIN="/opt/homebrew/bin/claude"

if [ -z "$CLAUDE_BIN" ]; then
  echo "[$STAMP] ERROR: claude binary not found on PATH" >> "$LOG_DIR/fb-daily.log"
  exit 1
fi

# Run the skill headless. --dangerously-skip-permissions is required for an
# unattended run; the skill itself is conservative and read/act-limited.
"$CLAUDE_BIN" -p "/fb-daily" \
  --dangerously-skip-permissions \
  >> "$LOG_DIR/fb-daily.log" 2>&1 || echo "[$STAMP] run exited non-zero" >> "$LOG_DIR/fb-daily.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] fb-daily run finished" >> "$LOG_DIR/fb-daily.log"
