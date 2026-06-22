#!/usr/bin/env python3
# Test different max_tokens settings - Week 2 Day 2

import ollama

question = "Explain what artificial intelligence is in detail."

print("=== Max Tokens Comparison ===\n")

# Very short response
print("1. max_tokens = 20 (Very short):")
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}],
    options={'max_tokens': 20}
)
print(f"   {response['message']['content']}\n")

# Medium response
print("2. max_tokens = 100 (Medium):")
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}],
    options={'max_tokens': 100}
)
print(f"   {response['message']['content']}\n")

# No limit (default)
print("3. No max_tokens (Full response):")
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}]
)
full_response = response['message']['content']
print(f"   {full_response[:200]}...")  # Show first 200 characters
print(f"   Total length: {len(full_response)} characters\n")

print("=== Max tokens controls response length! ===")
