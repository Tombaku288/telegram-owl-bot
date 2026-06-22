#!/usr/bin/env python3
# Production Telegram Bot with Hermes - Week 3 Day 2

import os
import json
import logging
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

# Setup logging to file
log_filename = f"telegram_bot_{datetime.now().strftime('%d%m%Y_%H%M%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
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
        logger.info(f"New session: {user_id}")
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
        "/clear - Clear conversation memory\n\n"
        "Just send me a message and I'll reply with Hermes!"
    )

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
        logger.error(f"Ollama error for user {user_id}: {e}")
        await update.message.reply_text(" Model error. Please try again.")
    except Exception as e:
        logger.error(f"Unexpected error for user {user_id}: {e}")
        await update.message.reply_text(" An unexpected error occurred. Please try again.")

print("\n" + "="*50)
print("     TELEGRAM BOT (PRODUCTION)")
print("="*50)
print(f"Model: {config['model']}")
print(f"Temperature: {config['temperature']}")
print(f"Log file: {log_filename}")
print("="*50)
print("Bot is running... Press Ctrl+C to stop.\n")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("clear", clear_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_hermes))

app.run_polling()
