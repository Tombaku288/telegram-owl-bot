#!/bin/bash
# Script with functions - Day 6 Step 4

# Function: Check if Ollama is running
check_ollama() {
    if pgrep -x "ollama" > /dev/null; then
        echo " Ollama is running"
        return 0
    else
        echo " Ollama is NOT running"
        return 1
    fi
}

# Function: Show a model's details
show_model() {
    local model_name=$1
    echo "Model: $model_name"
    ollama list | grep "$model_name"
    echo ""
}

# Main script starts here
echo "=== Using Functions ==="
echo ""

# Call the first function
check_ollama
echo ""

# Call the second function for each model
echo "=== Model Details ==="
show_model "hermes3:3b"
show_model "llama3.2:3b"
show_model "llama3.1:8b"

echo "=== Script Complete ==="
