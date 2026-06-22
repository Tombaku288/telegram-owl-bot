#!/bin/bash
# Safe copy script using absolute paths

BASE_DIR="$HOME/projects/week1"
SOURCE_DIR="$BASE_DIR/practice_files"
BACKUP_DIR="$BASE_DIR/backups"

# Create backup directory if missing
mkdir -p "$BACKUP_DIR"

# Check if source has files
if [ -z "$(ls -A $SOURCE_DIR/*.txt 2>/dev/null)" ]; then
    echo "No .txt files found in $SOURCE_DIR"
    exit 1
fi

# Copy files with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp -v $SOURCE_DIR/*.txt "$BACKUP_DIR/backup_${TIMESTAMP}/" 2>/dev/null || \
    echo "No .txt files to copy"

echo "Backup complete. Contents:"
ls -la "$BACKUP_DIR"
