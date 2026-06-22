#!/usr/bin/env python3
# Advanced Telegram Bot - Week 3 Day 5

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

# Admin user ID (replace with your Telegram user ID)
ADMIN_USER_ID = 123456789  # <- Replace with your actual user ID

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

# Rate limiting
user_last_message = {}

def is_rate_limited(user_id, cooldown_seconds=3):
    current_time = time.time()
    if user_id in user_last_message:
        if current_time - user_last_message[user_id] < cooldown_seconds:
            return True
    user_last_message[user_id] = current_time
    return False

# User sessions with persistence
user_sessions = {}
SESSION_FILE = "user_sessions.json"

def load_sessions():
    global user_sessions
    try:
        with open(SESSION_FILE, 'r') as f:
            user_sessions = json.load(f)
        logger.info(f"Loaded {len(user_sessions)} sessions from file")
    except:
        user_sessions = {}
        logger.info("No existing sessions found")

def save_sessions():
    try:
        with open(SESSION_FILE, 'w') as f:
            json.dump(user_sessions, f)
    except Exception as e:
        logger.error(f"Failed to save sessions: {e}")

def get_session(user_id):
    user_id_str = str(user_id)
    if user_id_str not in user_sessions:
        user_sessions[user_id_str] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
        save_sessions()
    return user_sessions[user_id_str]

# Load sessions on startup
load_sessions()

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
        "/ping - Check latency\n"
        "/save - Save conversations\n"
        "/stats - Show stats (admin only)"
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
    user_id = str(update.effective_user.id)
    if user_id in user_sessions:
        user_sessions[user_id] = [{'role': 'system', 'content': config['system_prompt']}]
        save_sessions()
        await update.message.reply_text(" Memory cleared!")
    else:
        await update.message.reply_text("No session to clear.")

async def save_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_sessions()
    await update.message.reply_text(" Conversations saved!")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text(" Admin only.")
        return
    
    total_messages = 0
    for session in user_sessions.values():
        total_messages += len(session)
    
    await update.message.reply_text(
        f"**Stats**\n"
        f"Total sessions: {len(user_sessions)}\n"
        f"Total messages: {total_messages}\n"
        f"Model: {config['model']}\n"
        f"Temperature: {config['temperature']}"
    )

async def chat_with_hermes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    
    if is_rate_limited(user_id, cooldown_seconds=3):
        await update.message.reply_text(" Please wait 3 seconds.")
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
        save_sessions()
        await update.message.reply_text(bot_response)
    except Exception as e:
        await update.message.reply_text(" Error. Please try again.")

print("\n" + "="*50)
print("     TELEGRAM BOT (ADVANCED)")
print("="*50)
print(f"Model: {config['model']}")
print(f"Rate limit: 3 seconds")
print(f"Sessions loaded: {len(user_sessions)}")
print("="*50 + "\n")

app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("status", status_command))
app.add_handler(CommandHandler("about", about_command))
app.add_handler(CommandHandler("ping", ping_command))
app.add_handler(CommandHandler("clear", clear_command))
app.add_handler(CommandHandler("save", save_command))
app.add_handler(CommandHandler("stats", stats_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_hermes))

print("Bot is running... Press Ctrl+C to stop.\n")
app.run_polling()
