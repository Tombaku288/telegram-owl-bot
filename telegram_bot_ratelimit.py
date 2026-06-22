#!/usr/bin/env python3
# Telegram Bot with Rate Limiting - Week 3 Day 4

import os
import json
import logging
import time
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

# Rate limiting: track last message time per user
user_last_message = {}

def is_rate_limited(user_id, cooldown_seconds=3):
    current_time = time.time()
    if user_id in user_last_message:
        if current_time - user_last_message[user_id] < cooldown_seconds:
            return True
    user_last_message[user_id] = current_time
    return False

# User sessions
user_sessions = {}

def get_session(user_id):
    if user_id not in user_sessions:
        user_sessions[user_id] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
    return user_sessions[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" Hello! I am Hermes. Send /help for commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start\n"
        "/help - This help\n"
        "/clear - Clear memory\n"
        "/status - Bot status\n"
        "/about - About me\n"
        "/ping - Check latency"
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        ollama.chat(model=config['model'], messages=[{'role': 'user', 'content': 'OK'}], options={'max_tokens': 2})
        ollama_status = " Connected"
    except:
        ollama_status = " Error"
    
    await update.message.reply_text(
        f"**Bot Status**\n"
        f"Model: {config['model']}\n"
        f"Temp: {config['temperature']}\n"
        f"Ollama: {ollama_status}\n"
        f"Sessions: {len(user_sessions)}"
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" I am Hermes 3:3b from Nous Research. Running locally via Ollama.")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start = time.time()
    await update.message.reply_text(" Pong!")
    latency = (time.time() - start) * 1000
    await update.message.reply_text(f"Latency: {latency:.0f}ms")

async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in user_sessions:
        user_sessions[user_id] = [{'role': 'system', 'content': config['system_prompt']}]
        await update.message.reply_text(" Memory cleared!")
    else:
        await update.message.reply_text("No session to clear.")

async def chat_with_hermes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if is_rate_limited(user_id, cooldown_seconds=3):
        await update.message.reply_text(" Please wait 3 seconds between messages.")
        return
    
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    session = get_session(user_id)
    session.append({'role': 'user', 'content': user_message})
    
    try:
        response = ollama.chat(
            model=config['model'],
            messages=session,
            options={'temperature': config['temperature'], 'max_tokens': config['max_tokens']}
        )
        bot_response = response['message']['content']
        session.append({'role': 'assistant', 'content': bot_response})
        await update.message.reply_text(bot_response)
    except Exception as e:
        await update.message.reply_text(" Error. Please try again.")

print("Bot with rate limiting running...")
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status_command))
app.add_handler(CommandHandler("about", about_command))
app.add_handler(CommandHandler("ping", ping_command))
app.add_handler(CommandHandler("clear", clear_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_hermes))
app.run_polling()
