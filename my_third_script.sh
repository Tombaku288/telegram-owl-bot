#!/bin/bash
# Script with a loop - Day 6 Step 3

echo "=== Model Counter ==="
echo "Counting your Ollama models..."

Count=0
for model in $(ollama list | tail -n +2 | awk '{print $1}'); do
echo "$COUNT. $model"
done

echo ""
echo "=== 5-Second Countdown Demo ==="
for i in 5 4 3 2 1; do
echo "  $i..."
done
echo "  GO! [200~~"
