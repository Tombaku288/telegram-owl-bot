#!/usr/bin/env python3
# Chat with system prompt - Week 2 Day 1

import ollama

# System prompt defines Hermes's behaviour
system_prompt = """You are a helpul, concise AI assistant named Hermes.
Keep your answers short and to the point (2-3 sentences maximum).
Be friendly but efficient. Focus on practical, actionable information."""

print("=== Chat with System Prompt ===")
print("Hermes will now answer concisely")
print("Type 'quit' to exit\n")

# Initialize conversation with system prompt
messages = [{'role': 'system', 'content': system_prompt}]

while True:
     # Get user input
     user_input = input("You: ")

     # Check if user wants to quit
     if user_input.lower() == 'quit':
           print("Goodbye!")
           break
    
     # Add user message to history
     messages.append({'role': 'user', 'content': user_input})

     # Get response from Hermes
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
