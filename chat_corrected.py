#!/usr/bin/env python3
# Chat with accurate system prompt - Week 2 Day 1

import ollama

# System prompt with CORRECT information
system_prompt = """You are Hermes 3:3b, an AI model created by Nous Research.
You are running locally on a user's computer via Ollama.
The user's name is EliteAgent.
You do NOT know your own origin beyond this information.
If asked about your origin, say: "I am Hermes 3:3b, an AI model from Nous Research, running locally on your machine via Ollama."
Keep answers concise (2-3 sentences)."""

print("=== Chat with Accurate Information ===")
print("Hermes will now give correct answers")
print("Type 'quit' to exit\n")

# Initialize conversation
messages = [{'role': 'system', 'content': system_prompt}]

while True:
    user_input = input("You: ")
    
    if user_input.lower() == 'quit':
        print("Goodbye!")
        break
    
    messages.append({'role': 'user', 'content': user_input})
    
    response = ollama.chat(
        model='hermes3:3b',
        messages=messages
    )
    
    hermes_response = response['message']['content']
    messages.append({'role': 'assistant', 'content': hermes_response})
    
    print(f"Hermes: {hermes_response}\n")
