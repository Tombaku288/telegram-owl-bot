#!/bin/bash
echo "Starting long task..."
for i in {1..30}; do
    echo "Progress: $i/30 - $(date)" >> task.log
    sleep 1
done
echo "Task complete!" >> task.log
