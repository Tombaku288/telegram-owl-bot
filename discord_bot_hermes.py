#!/usr/bin/env python3
# Discord Bot with Hermes - Week 4 Day 1 (Fixed)

import os
import json
import logging
import ollama
import discord
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

# User sessions (per user, per channel)
user_sessions = {}

def get_session(user_id, channel_id):
    key = f"{user_id}_{channel_id}"
    if key not in user_sessions:
        user_sessions[key] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
        logger.info(f"New session for {key}")
    return user_sessions[key]

@bot.event
async def on_ready():
    logger.info(f" Logged in as {bot.user}")
    logger.info(f" Bot is ready!")
    await bot.change_presence(activity=discord.Game(name="Hermes 3:3b"))

@bot.command(name='hello')
async def hello(ctx):
    """Say hello"""
    await ctx.send(" Hello! I am Hermes, your AI assistant. Type `!bothelp` for commands.")

@bot.command(name='bothelp')
async def bothelp(ctx):
    """Show help"""
    await ctx.send(
        " **Commands**\n\n"
        "`!hello` - Say hello\n"
        "`!bothelp` - Show this help\n"
        "`!clear` - Clear memory\n"
        "`!ping` - Check latency\n"
        "`!status` - Bot status\n\n"
        "Just type a message and I'll respond with Hermes!"
    )

@bot.command(name='ping')
async def ping(ctx):
    """Check latency"""
    await ctx.send(f" Pong! Latency: {round(bot.latency * 1000)}ms")

@bot.command(name='status')
async def status(ctx):
    """Show bot status"""
    try:
        ollama.chat(model=config['model'], messages=[{'role': 'user', 'content': 'OK'}], options={'max_tokens': 2})
        ollama_status = " Connected"
    except:
        ollama_status = " Error"
    
    await ctx.send(
        f" **Bot Status**\n"
        f"Model: `{config['model']}`\n"
        f"Temp: `{config['temperature']}`\n"
        f"Ollama: {ollama_status}\n"
        f"Sessions: `{len(user_sessions)}`"
    )

@bot.command(name='clear')
async def clear(ctx):
    """Clear conversation memory"""
    key = f"{ctx.author.id}_{ctx.channel.id}"
    if key in user_sessions:
        user_sessions[key] = [{'role': 'system', 'content': config['system_prompt']}]
        await ctx.send(" Memory cleared!")
    else:
        await ctx.send("No session to clear.")

@bot.event
async def on_message(message):
    # Don't respond to bot messages
    if message.author.bot:
        return
    
    # Process commands first
    await bot.process_commands(message)
    
    # If it's a command, don't process as chat
    if message.content.startswith('!'):
        return
    
    # Chat with Hermes
    user_id = message.author.id
    channel_id = message.channel.id
    user_message = message.content
    
    # Show typing indicator
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
            
            # Split long messages (Discord limit is 2000 chars)
            if len(bot_response) > 2000:
                for i in range(0, len(bot_response), 2000):
                    await message.channel.send(bot_response[i:i+2000])
            else:
                await message.channel.send(bot_response)
                
        except Exception as e:
            logger.error(f"Error: {e}")
            await message.channel.send(" Error. Please try again.")

print("\n" + "="*50)
print("     DISCORD BOT WITH HERMES")
print("="*50)
print(f"Model: {config['model']}")
print(f"Temperature: {config['temperature']}")
print("="*50 + "\n")

bot.run(token)
