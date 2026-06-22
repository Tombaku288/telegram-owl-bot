#!/usr/bin/env python3
# Compare 3B vs 8B model responses - Week 2 Day 2

import ollama
import time

question = "Explain what a Python dictionary is in one sentence."

print("=== Model Comparison ===\n")

# Test Hermes 3:3b
print("1. Hermes 3:3b (2.0 GB - Fast):")
start = time.time()
response = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': question}]
)
elapsed = time.time() - start
print(f"   Response: {response['message']['content']}")
print(f"   Time: {elapsed:.2f} seconds\n")

# Test Llama 3.1:8b
print("2. Llama 3.1:8b (4.9 GB - Slower but smarter):")
start = time.time()
response = ollama.chat(
    model='llama3.1:8b',
    messages=[{'role': 'user', 'content': question}]
)
elapsed = time.time() - start
print(f"   Response: {response['message']['content']}")
print(f"   Time: {elapsed:.2f} seconds\n")

print("=== Comparison Complete ===")
