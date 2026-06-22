#!/usr/bin/env python3
# Load configuration from JSON file - Week 2 Day 5

import json

print("=== Loading Configuration ===\n")

# Load config.json
with open('config.json', 'r') as f:
      config = json.load(f)

print("Config loaded successfully!")
print(f"Model: {config['model']}")
print(f"Temperature: {config['temperature']}")
print(f"Max tokens: {config['max_tokens']}")
print(f"System prompt: {config['system_prompt']}")
