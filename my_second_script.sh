#!/bin/bash
# Script with conditional logic - Day 6 Step 2

echo "=== System Information ==="
echo "User: $USER"
echo "Date: $(date)"
echo ""

echo "=== Checking Ollama ==="
if pgrep -x "ollama" > /dev/null; then
    echo " Ollama is RUNNING"
    echo ""
    echo "=== Your Models ==="
    ollama list
else
    echo " Ollama is NOT running"
    echo "Start it with: ollama serve &"
fi

echo ""
echo "=== Bot Ready Status ==="
if [ "$BOT_READY" = "true" ]; then
    echo " Bot is ready to deploy"
else
    echo "  Bot not ready. Run: export BOT_READY=true"
fi
