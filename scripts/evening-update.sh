#!/bin/bash
# Evening performance update — runs at 5:00 PM ET Mon-Fri
# Triggers OpenClaw to pull closing prices and update performance

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "$(date): Starting evening performance update..."
echo "Project dir: $PROJECT_DIR"

echo "Evening update is triggered via OpenClaw cron. Run manually with:"
echo "  openclaw cron run --job penny-stock-evening"
