#!/usr/bin/env python3
# Multi-Step Agent - Month 5 Week 4

import json
import re
import ollama
from tools import tools, execute_tool

print("="*50)
print("     MULTI-STEP AGENT")
print("="*50 + "\n")

def parse_tool_calls(text):
    calls = []
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
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

def multi_step_agent(user_query):
    print(f" User: {user_query}\n")
    
    # Step 1: Get Hermes to plan
    plan_response = ollama.chat(
        model='hermes3:3b',
        messages=[
            {'role': 'system', 'content': """You are a helpful assistant with access to tools.

TOOLS:
- get_current_time: Get current date and time
- calculate: Do math (expression)
- web_search: Search the web (query)
- get_weather: Get weather for a city (city)

When you need a tool, respond with ONLY JSON:
{"tool_name": "get_weather", "parameters": {"city": "Tokyo"}}

For multiple tools, respond with multiple JSON objects."""},
            {'role': 'user', 'content': user_query}
        ],
        options={'temperature': 0.1}
    )
    
    plan = plan_response['message']['content'].strip()
    print(f" Plan:\n{plan}\n")
    
    # Step 2: Execute tools
    calls = parse_tool_calls(plan)
    if not calls:
        print(f" Hermes: {plan}")
        return
    
    print(f" Executing {len(calls)} tool(s)...\n")
    tool_results = []
    for call in calls:
        tool_name = call.get('tool_name')
        params = call.get('parameters', {})
        if tool_name:
            result = execute_tool(tool_name, params)
            tool_results.append(f"{tool_name}: {result}")
            print(f"    {tool_name}  {result}")
    
    if not tool_results:
        return
    
    # Step 3: Generate final answer
    print("\n Generating final answer...")
    final_response = ollama.chat(
        model='hermes3:3b',
        messages=[
            {'role': 'system', 'content': "You are a helpful assistant. Use the tool results to answer the user's question."},
            {'role': 'user', 'content': f"Question: {user_query}\n\nTool results:\n" + "\n".join(tool_results)}
        ],
        options={'temperature': 0.3}
    )
    print(f"\n Hermes: {final_response['message']['content']}\n")

if __name__ == "__main__":
    multi_step_agent("What is the weather in Tokyo and what time is it there?")
