#!/usr/bin/env python3
# Full Agent Loop with Weather - Month 5 Week 3

import json
import re
import ollama
from tools import tools, execute_tool

print("="*50)
print("     HERMES AGENT WITH WEATHER")
print("="*50 + "\n")

def parse_tool_calls(text):
    calls = []
    # Remove code blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    # Find JSON objects (multi-line)
    stack = []
    start_idx = -1
    for i, char in enumerate(text):
        if char == '{':
            if not stack:
                start_idx = i
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack:
                    try:
                        obj = json.loads(text[start_idx:i+1])
                        if 'tool_name' in obj:
                            calls.append(obj)
                    except:
                        pass
    return calls

def agent_chat(user_query):
    print(f"User: {user_query}\n")
    
    response = ollama.chat(
        model='hermes3:3b',
        messages=[
            {'role': 'system', 'content': """You are a helpful assistant with access to these tools:

TOOLS:
- get_current_time: Get current date and time (no parameters)
- calculate: Do math (parameter: expression)
- web_search: Search the web (parameter: query)
- get_weather: Get weather for a city (parameter: city)

When you need a tool, respond with ONLY JSON:
{"tool_name": "get_weather", "parameters": {"city": "Tokyo"}}

No other text. Just the JSON."""},
            {'role': 'user', 'content': user_query}
        ],
        options={'temperature': 0.1}
    )
    
    hermes_response = response['message']['content'].strip()
    print(f"Hermes raw response:\n{hermes_response}\n")
    
    calls = parse_tool_calls(hermes_response)
    if not calls:
        print(f"Hermes: {hermes_response}")
        return
    
    print(f"Detected tools: {calls}\n")
    
    tool_results = []
    for call in calls:
        tool_name = call.get('tool_name')
        params = call.get('parameters', {})
        if tool_name:
            result = execute_tool(tool_name, params)
            tool_results.append(f"{tool_name}: {result}")
            print(f" {tool_name}  {result}")
    
    if not tool_results:
        return
    
    print("\nGenerating final answer...")
    final_response = ollama.chat(
        model='hermes3:3b',
        messages=[
            {'role': 'system', 'content': "You are a helpful assistant. Use the tool results to answer the user's question."},
            {'role': 'user', 'content': f"Question: {user_query}\n\nTool results:\n" + "\n".join(tool_results)}
        ],
        options={'temperature': 0.3}
    )
    print(f"\nHermes: {final_response['message']['content']}\n")

if __name__ == "__main__":
    agent_chat("What is the weather in Tokyo right now?")
