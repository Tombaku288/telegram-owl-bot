#!/usr/bin/env python3
# Test error handling - Week 2 Day 3

import ollama

print("=== Testing Error Handling ===\n")

try:
    # Try to use a model that doesn't exist
    response = ollama.chat(
        model='fake_model_that_does_not_exist',
        messages=[{'role': 'user', 'content': 'Hello'}]
    )
    print(f"Success: {response}")
    
except ollama.ResponseError as e:
    print(f" Caught Ollama error!")
    print(f"   Error code: {e.status_code}")
    print(f"   Error message: {e.error}")
    
except Exception as e:
    print(f" Caught general error: {type(e).__name__}: {e}")
    
print("\n=== Error was handled, script didn't crash! ===")
