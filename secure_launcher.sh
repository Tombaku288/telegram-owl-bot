#!/bin/bash
# Only runs scripts with safe permissions

SCRIPT="$1"

if [ ! -f "$SCRIPT" ]; then
    echo "Error: $SCRIPT not found"
    exit 1
fi

PERMS=$(stat -c "%a" "$SCRIPT")

if [ "$PERMS" = "755" ] || [ "$PERMS" = "700" ]; then
    echo " Safe permissions ($PERMS). Running $SCRIPT..."
    ./"$SCRIPT"
else
    echo " Unsafe permissions: $PERMS"
    echo "Expected 700 or 755"
    echo "Fix with: chmod 755 $SCRIPT"
fi
