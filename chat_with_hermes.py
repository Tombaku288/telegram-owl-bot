#!/usr/bin/env python3
# First Python script that calls Hermes - Week 2 Day 1

import ollama

print("=== Testing Ollama from Python ===\n")

# Simple test prompt
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': 'Say "Python is connected to Hermes!"'}]
)

print("Response from Hermes:")
print(response['message']['content'])
print("\n Python can now talk to your local LLM!")
