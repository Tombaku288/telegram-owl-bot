#!/usr/bin/env python3
# Hermes Tool Calling - Month 5 Week 1 (Final Parser)

import json
import re
import ollama
from tools import tools, execute_tool

print("="*50)
print("     HERMES TOOL CALLING (FINAL PARSER)")
print("="*50 + "\n")

user_query = "What is the current time and also calculate 15 * 30?"

print(f"User: {user_query}\n")

response = ollama.chat(
    model='hermes3:3b',
    messages=[
        {'role': 'system', 'content': """You are a helpful assistant with access to tools.

TOOLS:
- get_current_time: Get the current date and time (no parameters)
- calculate: Perform a math calculation (parameter: expression)

When you need to use a tool, respond with ONLY this exact JSON format:
{"tool_name": "get_current_time", "parameters": {}}

For multiple tools, respond with a JSON array:
[{"tool_name": "get_current_time", "parameters": {}}, {"tool_name": "calculate", "parameters": {"expression": "15 * 30"}}]

Respond ONLY with valid JSON. No other text."""},
        {'role': 'user', 'content': user_query}
    ],
    options={'temperature': 0.1}
)

hermes_response = response['message']['content'].strip()
print(f"Hermes raw response:\n{hermes_response}\n")

# ===== Parser: Extract all JSON objects =====
def extract_json_objects(text):
    """Extract all valid JSON objects/arrays from text."""
    objects = []
    
    # First, try to find JSON arrays
    array_pattern = r'\[[^\[\]]*\]'
    for match in re.findall(array_pattern, text):
        try:
            obj = json.loads(match)
            objects.append(obj)
        except:
            pass
    
    # Then find individual JSON objects
    object_pattern = r'\{[^{}]*\}'
    for match in re.findall(object_pattern, text):
        try:
            obj = json.loads(match)
            objects.append(obj)
        except:
            pass
    
    return objects

# Extract all JSON objects
json_objects = extract_json_objects(hermes_response)

if not json_objects:
    print("No valid JSON found in response.")
    print(f"Hermes: {hermes_response}")
else:
    print(f"Found {len(json_objects)} JSON object(s)")
    
    # Flatten any arrays
    all_calls = []
    for obj in json_objects:
        if isinstance(obj, list):
            all_calls.extend(obj)
        else:
            all_calls.append(obj)
    
    print("Tool calls:", all_calls)
    print("\nExecuting tools...\n")
    
    for call in all_calls:
        tool_name = call.get('tool_name')
        params = call.get('parameters', {})
        if tool_name:
            result = execute_tool(tool_name, params)
            print(f"Tool: {tool_name}")
            print(f"Result: {result}\n")
        else:
            print(f"Skipping: {call} (no tool_name)")
