#!/bin/bash
# My first real script - Day 6

echo "=== System Information ==="
echo "User: $USER"
echo "Home: $HOME"
echo "Shell: $SHELL"
echo ""
echo "=== Ollama Status ==="
ollama list
echo ""
echo "=== Bot Environment ==="
echo "BOT_READY: ${BOT_READY:-NOT SET}"
echo "TEST_VAR: ${TEST_VAR:-NOT SET}"
