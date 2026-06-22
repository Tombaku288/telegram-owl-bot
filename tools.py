#!/usr/bin/env python3
# Tool definitions for Hermes - Month 5 Week 2 (Part 1)

import datetime

# ===== TOOL DEFINITIONS =====
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to calculate (e.g., '2 + 2')"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# ===== TOOL IMPLEMENTATIONS =====
def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%d-%m-%Y %H:%M:%S")

def calculate(expression):
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {e}"

# ===== WEB SEARCH TOOL =====
def web_search(query):
    """Search the web using DuckDuckGo."""
    try:
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=3):
                results.append(f" {r['title']}: {r['body'][:200]}...")
            if results:
                return "\n".join(results)
            else:
                return "No results found."
    except Exception as e:
        return f"Search error: {e}"

# Update tools list with web search
tools.append({
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search the web for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
})

# ===== TOOL REGISTRY =====
def execute_tool(tool_name, parameters):
    if tool_name == "get_current_time":
        return get_current_time()
    elif tool_name == "calculate":
        return calculate(parameters.get("expression", ""))
    elif tool_name == "web_search":
        return web_search(parameters.get("query", ""))
    else:
        return f"Unknown tool: {tool_name}"

# ===== WEATHER TOOL (No API Key Required) =====
import requests

def get_weather(city):
    """Get current weather for a city using wttr.in (free, no API key)."""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"
        else:
            return f"Weather error: Could not fetch data for {city}"
    except Exception as e:
        return f"Weather error: {e}"

# Update tools list with weather
tools.append({
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name (e.g., 'Tokyo', 'London')"
                }
            },
            "required": ["city"]
        }
    }
})

# ===== UPDATED TOOL REGISTRY =====
def execute_tool(tool_name, parameters):
    if tool_name == "get_current_time":
        return get_current_time()
    elif tool_name == "calculate":
        return calculate(parameters.get("expression", ""))
    elif tool_name == "web_search":
        return web_search(parameters.get("query", ""))
    elif tool_name == "get_weather":
        return get_weather(parameters.get("city", ""))
    else:
        return f"Unknown tool: {tool_name}"

# ===== CLEANER WEATHER TOOL =====
def get_weather(city):
    """Get current weather for a city in km/h."""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w+km/h"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"
        else:
            return f"Weather error: Could not fetch data for {city}"
    except Exception as e:
        return f"Weather error: {e}"

# ===== FIXED WEATHER TOOL (No duplicate units) =====
def get_weather(city):
    """Get current weather for a city."""
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"Weather in {city}: {response.text.strip()}"
        else:
            return f"Weather error: Could not fetch data for {city}"
    except Exception as e:
        return f"Weather error: {e}"
