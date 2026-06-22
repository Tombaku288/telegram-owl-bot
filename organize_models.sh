#!/bin/bash
# Organize model outputs by date

BASE_DIR="$HOME/projects/week1/model_outputs"
DATE=$(date +%Y%m%d)
TIME=$(date +%H%M%S)

# Create dated directory
mkdir -p "$BASE_DIR/$DATE"

# Save current model list
ollama list > "$BASE_DIR/$DATE/models_$TIME.txt"

# Create a symlink to "latest"
ln -sf "$BASE_DIR/$DATE" "$BASE_DIR/latest"

# Show what was created
echo "Model output saved to: $BASE_DIR/$DATE/"
ls -la "$BASE_DIR/$DATE/"
echo ""
echo "Latest symlink points to:"
ls -la "$BASE_DIR/latest"
