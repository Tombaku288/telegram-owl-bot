#!/bin/bash
# Safe delete  previews before deleting

if [ -z "$1" ]; then
    echo "Usage: $0 <file_pattern>"
    echo "Example: $0 *.log"
    exit 1
fi

echo "Files matching '$1':"
ls -la $1 2>/dev/null

if [ $? -ne 0 ]; then
    echo "No files match '$1'"
    exit 1
fi

echo ""
read -p "Delete these files? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    rm -v $1
    echo "Deleted."
else
    echo "Cancelled."
fi
