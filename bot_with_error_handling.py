#!/usr/bin/env python3
# Bot with error handling - Week 2 Day 3

import ollama
import sys

print("=== Bot with Error Handling ===\n")

try:
    # Try to chat with Hermes
    response = ollama.chat(
        model='hermes3:3b',
        messages=[{'role': 'user', 'content': 'Say "Hello!"'}]
    )
    print(f"Success: {response['message']['content']}\n")
    
except ollama.ResponseError as e:
    print(f" Ollama error: {e}")
    print("   Try: ollama serve &")
    
except Exception as e:
    print(f" Unexpected error: {e}")
    
finally:
    print("=== Error handling complete ===")
