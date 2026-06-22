#!/bin/bash
# Script demonstrating exit codes - Day 6 Step 5

echo "=== Exit Code Demo ==="

# Command that succeeds
echo "Running: ollama list"
ollama list > /dev/null 2>&1
echo "Exit code: $?" # $? shows the last command's exit code
echo ""

# Command that fails
echo "Running: ollama show nonexistent_model"
ollama show nonexistent_model > /dev/null 2>&1
echo "Exit code: $?"
echo ""

# Using exit codes in conditions
echo "=== Using Exit Codes ==="
if ollama list > /dev/null 2>&1; then
     echo "'ollama list' succeeded (exit code 0)"
else
     echo "'ollama list' failed"
fi

if ollama show fake_model > /dev/null 2>&1; then
     echo "'ollama show fake_model' succeeded"
else
     echo "'ollama show fake_model' failed (exit code non-zero)"
fi

echo ""
echo "=== Script Complete (exit code 0) ==="
exit 0
