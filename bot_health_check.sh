#!/bin/bash
# Bot Health Check Script - Day 6 Step 6
# This script checks if everything is ready for your Telegram/Discord bot

# Colors for output (optional, makes it prettier)
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function: Print colored status
print_status() {
    if [ "$2" = "good" ]; then
        echo -e "${GREEN} $1${NC}"
    elif [ "$2" = "bad" ]; then
        echo -e "${RED} $1${NC}"
    else
        echo -e "${YELLOW}  $1${NC}"
    fi
}

# Function: Check if Ollama is running
check_ollama() {
    if pgrep -x "ollama" > /dev/null; then
        print_status "Ollama is running" "good"
        return 0
    else
        print_status "Ollama is NOT running (run: ollama serve &)" "bad"
        return 1
    fi
}

# Function: Check if Hermes model exists
check_hermes_model() {
    if ollama list | grep -q "hermes3:3b"; then
        print_status "Hermes 3:3b model is available" "good"
        return 0
    else
        print_status "Hermes 3:3b model NOT found (run: ollama pull hermes3:3b)" "bad"
        return 1
    fi
}

# Function: Check if .env file exists and is secure
check_env_file() {
    if [ -f ".env" ]; then
        PERMS=$(stat -c "%a" .env 2>/dev/null)
        if [ "$PERMS" = "600" ]; then
            print_status ".env file exists with correct permissions (600)" "good"
        else
            print_status ".env file exists but permissions are $PERMS (should be 600)" "bad"
        fi
    else
        print_status ".env file NOT found (create one with your bot tokens)" "bad"
    fi
}

# Function: Check exported bot variables
check_bot_vars() {
    if [ -n "$BOT_READY" ] && [ "$BOT_READY" = "true" ]; then
        print_status "BOT_READY = true" "good"
    else
        print_status "BOT_READY not set to true (run: export BOT_READY=true)" "bad"
    fi
}

# Main script starts here
echo ""
echo "========================================"
echo "     BOT HEALTH CHECK - DAY 6"
echo "========================================"
echo ""

# Run all checks
check_ollama
check_hermes_model
check_env_file
check_bot_vars

echo ""
echo "========================================"
echo "            SUMMARY"
echo "========================================"
echo ""

# Count how many passed (simple version)
PASS_COUNT=0
check_ollama > /dev/null 2>&1 && PASS_COUNT=$((PASS_COUNT + 1))
check_hermes_model > /dev/null 2>&1 && PASS_COUNT=$((PASS_COUNT + 1))
check_env_file > /dev/null 2>&1 && PASS_COUNT=$((PASS_COUNT + 1))
check_bot_vars > /dev/null 2>&1 && PASS_COUNT=$((PASS_COUNT + 1))

echo "Passed: $PASS_COUNT / 4 checks"
echo ""

if [ $PASS_COUNT -eq 4 ]; then
    echo -e "${GREEN} All checks passed! Ready to deploy your bot.${NC}"
    exit 0
else
    echo -e "${YELLOW}  Some checks failed. Fix the issues above before deploying.${NC}"
    exit 1
fi
