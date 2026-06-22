#!/usr/bin/env python3
# Test different temperature settings - Week 2 Day 2

import ollama

question = "Write a one-sentence greeting for a friendly chatbot."

print("=== Temperature Comparison ===\n")

# Low temperature (predictable)
print("1. Temperature = 0.1 (Very predictable):")
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}],
    options={'temperature': 0.1}
)
print(f"   {response['message']['content']}\n")

# Medium temperature (balanced)
print("2. Temperature = 0.7 (Balanced):")
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}],
    options={'temperature': 0.7}
)
print(f"   {response['message']['content']}\n")

# High temperature (creative)
print("3. Temperature = 1.2 (Creative/Unpredictable):")
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}],
    options={'temperature': 1.2}
)
print(f"   {response['message']['content']}\n")

print("=== Notice how the answers differ! ===")
