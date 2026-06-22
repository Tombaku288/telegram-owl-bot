#!/bin/bash
echo "=== Hermes Test ==="
echo "Current time: $(date)"
echo ""
echo "Asking Hermes about Linux..."
ollama run hermes3:3b "What is one essential Linux command for beginners? Answer in one short sentence."
