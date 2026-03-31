#!/bin/bash
# Morning research trigger — runs at 6:00 AM ET Mon-Fri
# Triggers OpenClaw to conduct penny stock research and publish daily picks

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "$(date): Starting morning research..."
echo "Project dir: $PROJECT_DIR"

# The actual research is handled by OpenClaw cron job (agentTurn)
# This script exists for manual runs / debugging
echo "Morning research is triggered via OpenClaw cron. Run manually with:"
echo "  openclaw cron run --job penny-stock-morning"
