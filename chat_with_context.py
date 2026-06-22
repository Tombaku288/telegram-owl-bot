#!/usr/bin/env python3
import ollama
import subprocess

# Get actual installed models
result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
models_output = result.stdout

system_prompt = f"""You are Hermes 3:3b. Here are the ACTUAL models installed on this system:

{models_output}

If asked about what models are installed, list THESE models exactly.
Do not invent other models like GPT-3 or BERT."""

print("=== Chat with System Context ===")
print("Hermes now knows what models you have\n")

messages = [{'role': 'system', 'content': system_prompt}]

while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    messages.append({'role': 'user', 'content': user_input})
    response = ollama.chat(model='hermes3:3b', messages=messages)
    hermes_response = response['message']['content']
    messages.append({'role': 'assistant', 'content': hermes_response})
    print(f"Hermes: {hermes_response}\n")
