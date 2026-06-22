#!/usr/bin/env python3
# Discord Bot with Embeds and Advanced Features - Week 4 Day 3

import os
import json
import logging
import time
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

# === COMMAND PERMISSIONS ===
# Define admin role name (change to match your server)
ADMIN_ROLE = "Admin"

def is_admin(interaction: discord.Interaction) -> bool:
    """Check if user has admin role"""
    if interaction.guild is None:
        return False
    role = discord.utils.get(interaction.guild.roles, name=ADMIN_ROLE)
    if role is None:
        return False
    return role in interaction.user.roles

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

# === CREATE EMBED HELPER ===
def create_embed(title, description, color=discord.Color.blue(), fields=None, footer=None):
    """Create a formatted embed message"""
    embed = discord.Embed(title=title, description=description, color=color)
    if fields:
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
    if footer:
        embed.set_footer(text=footer)
    return embed

# === SLASH COMMANDS ===

@bot.tree.command(name="hello", description="Say hello to Hermes")
async def slash_hello(interaction: discord.Interaction):
    embed = create_embed(
        title=" Hello!",
        description="I am Hermes, your AI assistant. Type `/help` for commands.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show available commands")
async def slash_help(interaction: discord.Interaction):
    embed = create_embed(
        title=" Available Commands",
        description="Use these slash commands to interact with Hermes.",
        color=discord.Color.blue(),
        fields=[
            ("`/hello`", "Say hello to Hermes"),
            ("`/help`", "Show this help message"),
            ("`/ping`", "Check bot latency"),
            ("`/status`", "Show bot status"),
            ("`/clear`", "Clear conversation memory"),
            ("`/stats`", "Show statistics (Admin only)"),
            ("`/about`", "About Hermes")
        ],
        footer="Just type a message to chat with Hermes!"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Check bot latency")
async def slash_ping(interaction: discord.Interaction):
    start = time.time()
    await interaction.response.defer()
    end = time.time()
    latency = round((end - start) * 1000)
    embed = create_embed(
        title=" Pong!",
        description=f"Latency: `{latency}ms`\nWebSocket: `{round(bot.latency * 1000)}ms`",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="status", description="Show bot status")
async def slash_status(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        ollama.chat(model=config['model'], messages=[{'role': 'user', 'content': 'OK'}], options={'max_tokens': 2})
        ollama_status = " Connected"
        ollama_color = discord.Color.green()
    except:
        ollama_status = " Error"
        ollama_color = discord.Color.red()
    
    embed = create_embed(
        title=" Bot Status",
        description="Current bot status and configuration.",
        color=ollama_color,
        fields=[
            ("Model", f"`{config['model']}`"),
            ("Temperature", f"`{config['temperature']}`"),
            ("Ollama", ollama_status),
            ("Sessions", f"`{len(user_sessions)}` active")
        ],
        footer="Hermes 3:3b - Running locally via Ollama"
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="about", description="About Hermes")
async def slash_about(interaction: discord.Interaction):
    embed = create_embed(
        title=" About Hermes",
        description="I am an AI assistant powered by Hermes 3:3b.",
        color=discord.Color.purple(),
        fields=[
            ("Model", "Hermes 3:3b from Nous Research"),
            ("Framework", "Python + discord.py + Ollama"),
            ("Running on", "WSL2 Ubuntu"),
            ("Creator", "EliteAgent")
        ],
        footer="Built for learning and practice"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Clear conversation memory")
async def slash_clear(interaction: discord.Interaction):
    key = f"{interaction.user.id}_{interaction.channel_id}"
    if key in user_sessions:
        user_sessions[key] = [{'role': 'system', 'content': config['system_prompt']}]
        embed = create_embed(
            title=" Memory Cleared!",
            description="Your conversation history has been reset.",
            color=discord.Color.green()
        )
    else:
        embed = create_embed(
            title="ℹ No Session",
            description="You don't have an active session to clear.",
            color=discord.Color.yellow()
        )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="stats", description="Show statistics (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_stats(interaction: discord.Interaction):
    await interaction.response.defer()
    
    total_messages = 0
    for session in user_sessions.values():
        total_messages += len(session)
    
    embed = create_embed(
        title=" Statistics",
        description="Bot usage statistics",
        color=discord.Color.gold(),
        fields=[
            ("Total Sessions", f"`{len(user_sessions)}`"),
            ("Total Messages", f"`{total_messages}`"),
            ("Model", f"`{config['model']}`"),
            ("Temperature", f"`{config['temperature']}`"),
            ("Uptime", "Running"),
            ("Commands Synced", f"`{len(bot.tree.get_commands())}`")
        ],
        footer="Admin only - Statistics"
    )
    await interaction.followup.send(embed=embed)

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
            await message.channel.send(" An error occurred. Please try again.")

print("\n" + "="*50)
print("     DISCORD BOT WITH EMBEDS (ADVANCED)")
print("="*50)
print(f"Model: {config['model']}")
print("Slash commands: /hello, /help, /ping, /status, /about, /clear, /stats")
print("Features: Rich embeds, Admin commands, Error handling")
print("="*50 + "\n")

bot.run(token)
