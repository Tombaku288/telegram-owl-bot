#!/usr/bin/env python3
# Simple Bot Framework WITH Error Handling - Week 2 Day 3

import ollama
import json

class SimpleBotSafe:
    def __init__(self, model='hermes3:3b', temperature=0.7, max_tokens=500):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history = []
    
    def add_system_prompt(self, prompt):
        """Add a system prompt to guide the bot's behavior"""
        self.conversation_history.append({'role': 'system', 'content': prompt})
    
    def chat(self, user_message):
        """Send a message and get response with error handling"""
        # Add user message to history
        self.conversation_history.append({'role': 'user', 'content': user_message})
        
        try:
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
            
        except ollama.ResponseError as e:
            error_msg = f" Model error: {e.error}"
            return error_msg
        except Exception as e:
            error_msg = f" Unexpected error: {type(e).__name__}"
            return error_msg
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        print("History cleared!")

# Demo
if __name__ == "__main__":
    print("=== SimpleBotSafe with Error Handling ===\n")
    
    bot = SimpleBotSafe()
    bot.add_system_prompt("You are a helpful assistant. Keep answers concise.")
    
    # Normal chat
    print("1. Normal chat:")
    response = bot.chat("Say 'Hello World'")
    print(f"   Bot: {response}\n")
    
    # This would crash before - now it's handled
    print("2. Testing error handling (fake model):")
    bot.model = "fake_model"
    response = bot.chat("Hello")
    print(f"   Bot: {response}\n")
    
    # Reset to real model
    bot.model = "hermes3:3b"
    print("3. Back to normal:")
    response = bot.chat("Say 'I am back'")
    print(f"   Bot: {response}\n")
    
    print("=== Error handling complete! Bot never crashed. ===")
