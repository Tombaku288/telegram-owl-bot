#!/usr/bin/env python3
# Interactive chat with Hermes - Week 2 Day 1

import ollama

print("=== Interactive Chat with Hermes ===")
print("Type 'quit' to exit\n")

while True:
    # Get user input
    user_input = input("You: ")
    
    # Check if user wants to quit
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    # Get response from Hermes
    response = ollama.chat(
        model='hermes3:3b',
        messages=[{'role': 'user', 'content': user_input}]
    )
    
    # Print Hermes response
    print(f"Hermes: {response['message']['content']}\n")
