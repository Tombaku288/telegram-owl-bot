#!/usr/bin/env python3
# Enhanced Telegram Bot with Hermes - Week 3 Day 3

import os
import json
import logging
import platform
from datetime import datetime
import ollama
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Load token
with open('telegram_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# User sessions
user_sessions = {}

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
    return user_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.effective_user.id}: /start")
    await update.message.reply_text(
        " Hello! I am Hermes, your AI assistant.\n"
        "Send me a message and I'll respond!\n"
        "Type /help for commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.effective_user.id}: /help")
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/clear - Clear conversation memory\n"
        "/status - Show bot status\n"
        "/about - About this bot\n\n"
        "Just send me a message and I'll reply with Hermes!"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show bot status."""
    logger.info(f"User {update.effective_user.id}: /status")
    
    # Check Ollama status
    try:
        response = ollama.chat(
            model=config['model'],
            messages=[{'role': 'user', 'content': 'Say "OK"'}],
            options={'max_tokens': 5}
        )
        ollama_status = " Connected"
    except Exception as e:
        ollama_status = f" Error: {str(e)[:50]}"
    
    # Check Python version
    python_version = platform.python_version()
    
    status_message = (
        " **Bot Status**\n\n"
        f"**Model:** {config['model']}\n"
        f"**Temperature:** {config['temperature']}\n"
        f"**Ollama:** {ollama_status}\n"
        f"**Python:** {python_version}\n"
        f"**Sessions:** {len(user_sessions)}\n"
        f"**Uptime:** Running"
    )
    
    await update.message.reply_text(status_message)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show about information."""
    logger.info(f"User {update.effective_user.id}: /about")
    about_message = (
        " **About Hermes**\n\n"
        "I am Hermes 3:3b, an AI model from Nous Research.\n"
        "I run locally on a machine via Ollama.\n\n"
        "Built with:\n"
        " Python-telegram-bot\n"
        " Ollama Python library\n"
        " Linux (WSL2)\n\n"
        "Created by EliteAgent for learning and practice."
    )
    await update.message.reply_text(about_message)

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"User {user_id}: /clear")
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
    logger.info(f"User {user_id}: {user_message}")
    
    session = get_session(user_id)
    session.append({'role': 'user', 'content': user_message})
    
    try:
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
        
    except ollama.ResponseError as e:
        logger.error(f"Ollama error: {e}")
        await update.message.reply_text(" Model error. Please try again.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(" An unexpected error occurred.")

print("\n" + "="*50)
print("     TELEGRAM BOT (ENHANCED)")
print("="*50)
print(f"Model: {config['model']}")
print(f"Temperature: {config['temperature']}")
print("="*50 + "\n")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status_command))
app.add_handler(CommandHandler("about", about_command))
app.add_handler(CommandHandler("clear", clear_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_hermes))

print("Bot is running... Press Ctrl+C to stop.\n")
app.run_polling()
