#!/usr/bin/env python3
# Simple Bot Framework - Week 2 Day 2
# This is the foundation for your Telegram/Discord bot

import ollama
import json
import time

class SimpleBot:
    def __init__(self, model='hermes3:3b', temperature=0.7, max_tokens=500):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = []
    
    def add_system_prompt(self, prompt):
        """Add a system prompt to guide the bot's behavior"""
        self.conversation_history.append({'role': 'system', 'content': prompt})
    
    def chat(self, user_message):
        """Send a message and get response"""
        # Add user message to history
        self.conversation_history.append({'role': 'user', 'content': user_message})
        
        # Get response from model
        response = ollama.chat(
            model=self.model,
            messages=self.conversation_history,
            options={
                'temperature': self.temperature,
                'max_tokens': self.max_tokens
            }
        )
        
        # Extract bot response
        bot_response = response['message']['content']
        
        # Add bot response to history
        self.conversation_history.append({'role': 'assistant', 'content': bot_response})
        
        return bot_response
    
    def chat_json(self, user_message, expected_format):
        """Get response in JSON format"""
        prompt = f"""You are a helpful assistant. Respond in valid JSON format only.

User question: {user_message}

Respond with this exact JSON structure:
{json.dumps(expected_format, indent=2)}"""
        
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1, 'max_tokens': 500}
        )
        
        try:
            return json.loads(response['message']['content'])
        except:
            return {"error": "Invalid JSON", "raw": response['message']['content']}
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("History cleared!")

# Demo
if __name__ == "__main__":
    print("=== Simple Bot Framework Demo ===\n")
    
    # Create bot instance
    bot = SimpleBot()
    
    # Add system prompt
    bot.add_system_prompt("You are a friendly, helpful assistant named Hermes. Keep answers concise.")
    
    # Simple chat
    print("1. Simple chat:")
    response = bot.chat("What is your name?")
    print(f"   Bot: {response}\n")
    
    # Memory test
    print("2. Memory test (remembers previous conversation):")
    response = bot.chat("What did I just ask you?")
    print(f"   Bot: {response}\n")
    
    # JSON output
    print("3. JSON output:")
    result = bot.chat_json("What are the 3 most popular programming languages?", 
                          {"languages": ["language1", "language2", "language3"]})
    print(f"   Parsed JSON: {result}\n")
    
    print("=== Bot Framework Ready for Telegram! ===")
