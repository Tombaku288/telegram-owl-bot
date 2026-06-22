#!/usr/bin/env python3
# Chat with conversation memory - Week 2 Day 1

import ollama

print("=== Chat with Memory ===")
print("Hermes will remember the conversation")
print("Type 'quit' to exit\n")

# List to store conversation history
messages = []

while True:
    # Get user input
    user_input = input("You: ")
    
    # Check if user wants to quit
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    # Add user message to history
    messages.append({'role': 'user', 'content': user_input})
    
    # Get response from Hermes with full history
    response = ollama.chat(
        model='hermes3:3b',
        messages=messages
    )
    
    # Get Hermes response
    hermes_response = response['message']['content']
    
    # Add Hermes response to history
    messages.append({'role': 'assistant', 'content': hermes_response})
    
    # Print Hermes response
    print(f"Hermes: {hermes_response}\n")
    
    # Show how many messages are in memory
    print(f"[Memory: {len(messages)} messages stored]\n")
