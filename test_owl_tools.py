#!/usr/bin/env python3
# Test Owl Alpha with tool calling

import os
import json
from openai import OpenAI

# Load API key
with open('openrouter.env', 'r') as f:
    key = f.read().strip().split('=')[1]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=key,
)

# Define a simple tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name (e.g., Tokyo)"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# Ask about weather
response = client.chat.completions.create(
    model="openrouter/owl-alpha",
    messages=[
        {"role": "user", "content": "What is the weather in Tokyo?"}
    ],
    tools=tools,
    tool_choice="auto"
)

print("Response from Owl Alpha:")
print(response.choices[0].message)
