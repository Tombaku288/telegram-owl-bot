#!/usr/bin/env python3
# Discord Bot with Slash Commands - Fixed - Week 4 Day 2

import os
import json
import logging
import ollama
import discord
from discord import app_commands
from discord.ext import commands

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

# Load Discord token
with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# User sessions
user_sessions = {}

def get_session(user_id, channel_id):
    key = f"{user_id}_{channel_id}"
    if key not in user_sessions:
        user_sessions[key] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
    return user_sessions[key]

@bot.event
async def on_ready():
    logger.info(f" Logged in as {bot.user}")
    logger.info(f" Bot is ready!")
    await bot.change_presence(activity=discord.Game(name="/help for commands"))
    try:
        synced = await bot.tree.sync()
        logger.info(f" Synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

# === SLASH COMMANDS ===

@bot.tree.command(name="hello", description="Say hello to Hermes")
async def slash_hello(interaction: discord.Interaction):
    await interaction.response.send_message(" Hello! I am Hermes, your AI assistant. Type `/help` for commands.")

@bot.tree.command(name="help", description="Show available commands")
async def slash_help(interaction: discord.Interaction):
    await interaction.response.send_message(
        " **Slash Commands**\n\n"
        "`/hello` - Say hello\n"
        "`/help` - Show this help\n"
        "`/ping` - Check latency\n"
        "`/status` - Bot status\n"
        "`/clear` - Clear memory\n\n"
        "Just type a message and I'll respond with Hermes!"
    )

@bot.tree.command(name="ping", description="Check bot latency")
async def slash_ping(interaction: discord.Interaction):
    await interaction.response.send_message(f" Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.tree.command(name="status", description="Show bot status")
async def slash_status(interaction: discord.Interaction):
    # Defer the response to allow longer processing time
    await interaction.response.defer()
    
    try:
        ollama.chat(model=config['model'], messages=[{'role': 'user', 'content': 'OK'}], options={'max_tokens': 2})
        ollama_status = " Connected"
    except:
        ollama_status = " Error"
    
    await interaction.followup.send(
        f" **Bot Status**\n"
        f"Model: `{config['model']}`\n"
        f"Temp: `{config['temperature']}`\n"
        f"Ollama: {ollama_status}\n"
        f"Sessions: `{len(user_sessions)}`"
    )

@bot.tree.command(name="clear", description="Clear conversation memory")
async def slash_clear(interaction: discord.Interaction):
    key = f"{interaction.user.id}_{interaction.channel_id}"
    if key in user_sessions:
        user_sessions[key] = [{'role': 'system', 'content': config['system_prompt']}]
        await interaction.response.send_message(" Memory cleared!")
    else:
        await interaction.response.send_message("No session to clear.")

# === TEXT CHAT ===

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    await bot.process_commands(message)
    
    if message.content.startswith('!'):
        return
    
    user_id = message.author.id
    channel_id = message.channel.id
    user_message = message.content
    
    async with message.channel.typing():
        session = get_session(user_id, channel_id)
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
            
            if len(bot_response) > 2000:
                for i in range(0, len(bot_response), 2000):
                    await message.channel.send(bot_response[i:i+2000])
            else:
                await message.channel.send(bot_response)
                
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.channel.send(" Error. Please try again.")

print("\n" + "="*50)
print("     DISCORD BOT WITH SLASH COMMANDS (FIXED)")
print("="*50)
print(f"Model: {config['model']}")
print("Slash commands: /hello, /help, /ping, /status, /clear")
print("="*50 + "\n")

bot.run(token)
