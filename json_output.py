#!/usr/bin/env python3
# Get structured JSON output - Week 2 Day 2

import ollama
import json

print("=== Structured JSON Output ===\n")

# Ask for JSON format
response = ollama.chat(
    model='hermes3:3b',
    messages=[{
        'role': 'user',
        'content': '''You are a helpful assistant. Respond in valid JSON format only.

User question: What are the 3 most popular programming languages?

Respond with this exact JSON structure:
{"languages": ["language1", "language2", "language3"]}'''
    }],
    options={'temperature': 0.1}  # Low temperature for consistency
)

# Parse and display JSON
try:
    data = json.loads(response['message']['content'])
    print("Parsed JSON response:")
    print(json.dumps(data, indent=2))
    print(f"\nFirst language: {data['languages'][0]}")
except:
    print("Raw response (not valid JSON):")
    print(response['message']['content'])
