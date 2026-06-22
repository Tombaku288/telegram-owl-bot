#!/usr/bin/env python3
# Telegram Bot with Hermes - Week 3 Day 1

import os
import json
import logging
import ollama
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Load token from file
with open('telegram_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# User sessions
user_sessions = {}

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
        logger.info(f"New session for user: {user_id}")
    return user_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        " Hello! I am Hermes, your AI assistant.\n"
        "Send me a message and I'll respond!\n"
        "Type /help for commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/clear - Clear conversation memory\n\n"
        "Just send me a message and I'll reply with Hermes!"
    )

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_sessions:
        user_sessions[user_id] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
        await update.message.reply_text(" Conversation memory cleared!")
    else:
        await update.message.reply_text("No session to clear.")

async def chat_with_hermes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Get user session
    session = get_session(user_id)
    
    # Add user message
    session.append({'role': 'user', 'content': user_message})
    
    try:
        # Get response from Hermes
        response = ollama.chat(
            model=config['model'],
            messages=session,
            options={
                'temperature': config['temperature'],
                'max_tokens': config['max_tokens']
            }
        )
        
        bot_response = response['message']['content']
        session.append({'role': 'assistant', 'content': bot_response})
        
        await update.message.reply_text(bot_response)
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(" Sorry, I encountered an error. Please try again.")

# Create the application
app = ApplicationBuilder().token(token).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("clear", clear_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_hermes))

print("Bot is running with Hermes... Press Ctrl+C to stop.")
app.run_polling()
