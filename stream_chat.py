#!/usr/bin/env python3
# Streaming responses from Hermes - Week 2 Day 2

import ollama

print("=== Streaming Chat with Hermes ===\n")

# Simple question
stream = ollama.chat(
    model='hermes3:3b',
    messages=[{'role': 'user', 'content': 'Write a short haiku about programming'}],
    stream=True  #  THIS enables streaming
)

print("Hermes (streaming): ", end="", flush=True)
for chunk in stream:
    print(chunk['message']['content'], end="", flush=True)
print("\n")
