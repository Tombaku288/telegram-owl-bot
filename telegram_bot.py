#!/usr/bin/env python3
# Simple Telegram Bot - Week 3 Day 1

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load token from file
with open('telegram_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /start is issued."""
    await update.message.reply_text(
        "Hello! I am Hermes, your AI assistant.\n"
        "Send me a message and I'll respond!\n"
        "Type /help for commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message."""
    await update.message.reply_text(
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/clear - Clear conversation memory\n\n"
        "Just send me a message and I'll reply!"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message (will be replaced with Hermes later)."""
    user_message = update.message.text
    await update.message.reply_text(f"You said: {user_message}")

# Create the application
app = ApplicationBuilder().token(token).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

print("Bot is running... Press Ctrl+C to stop.")
app.run_polling()
