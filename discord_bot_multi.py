#!/usr/bin/env python3
# Discord Bot with Multi-Server Support - Week 4 Day 4

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

# User sessions (per user, per channel, per server)
user_sessions = {}

def get_session(user_id, channel_id, guild_id):
    """Get or create a session for a specific user in a specific channel on a specific server"""
    key = f"{guild_id}_{user_id}_{channel_id}"
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
    logger.info(f" Connected to {len(bot.guilds)} servers:")
    for guild in bot.guilds:
        logger.info(f"   - {guild.name} (ID: {guild.id})")
    await bot.change_presence(activity=discord.Game(name=f"/help on {len(bot.guilds)} servers"))
    try:
        synced = await bot.tree.sync()
        logger.info(f" Synced {len(synced)} slash commands globally")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

# === EMBED HELPER ===
def create_embed(title, description, color=discord.Color.blue(), fields=None, footer=None):
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
        description=f"Hello from **{interaction.guild.name if interaction.guild else 'DM'}**! I am Hermes, your AI assistant.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show available commands")
async def slash_help(interaction: discord.Interaction):
    embed = create_embed(
        title=" Available Commands",
        description=f"Server: **{interaction.guild.name if interaction.guild else 'DM'}**",
        color=discord.Color.blue(),
        fields=[
            ("`/hello`", "Say hello to Hermes"),
            ("`/help`", "Show this help message"),
            ("`/ping`", "Check bot latency"),
            ("`/status`", "Show bot status"),
            ("`/clear`", "Clear conversation memory"),
            ("`/stats`", "Show statistics (Admin only)"),
            ("`/about`", "About Hermes"),
            ("`/servers`", "List servers the bot is in (Admin only)")
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
    
    total_messages = 0
    for session in user_sessions.values():
        total_messages += len(session)
    
    embed = create_embed(
        title=" Bot Status",
        description=f"Server: **{interaction.guild.name if interaction.guild else 'DM'}**",
        color=ollama_color,
        fields=[
            ("Model", f"`{config['model']}`"),
            ("Temperature", f"`{config['temperature']}`"),
            ("Ollama", ollama_status),
            ("Sessions", f"`{len(user_sessions)}` active"),
            ("Total Messages", f"`{total_messages}`"),
            ("Servers", f"`{len(bot.guilds)}` connected")
        ],
        footer="Hermes 3:3b - Running locally via Ollama"
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="servers", description="List all servers the bot is in (Admin only)")
@app_commands.default_permissions(administrator=True)
async def slash_servers(interaction: discord.Interaction):
    await interaction.response.defer()
    
    server_list = ""
    for guild in bot.guilds:
        server_list += f" **{guild.name}** (ID: `{guild.id}`) - {guild.member_count} members\n"
    
    if not server_list:
        server_list = "No servers found."
    
    embed = create_embed(
        title=" Servers",
        description=f"I am connected to {len(bot.guilds)} servers:",
        color=discord.Color.gold(),
        fields=[("Servers", server_list)],
        footer=f"Requested by {interaction.user.display_name}"
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="about", description="About Hermes")
async def slash_about(interaction: discord.Interaction):
    embed = create_embed(
        title=" About Hermes",
        description=f"Running on server: **{interaction.guild.name if interaction.guild else 'DM'}**",
        color=discord.Color.purple(),
        fields=[
            ("Model", "Hermes 3:3b from Nous Research"),
            ("Framework", "Python + discord.py + Ollama"),
            ("Running on", "WSL2 Ubuntu"),
            ("Creator", "EliteAgent"),
            ("Servers", f"`{len(bot.guilds)}` connected")
        ],
        footer="Built for learning and practice"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="Clear conversation memory")
async def slash_clear(interaction: discord.Interaction):
    key = f"{interaction.guild_id}_{interaction.user.id}_{interaction.channel_id}"
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
        description=f"Server: **{interaction.guild.name if interaction.guild else 'DM'}**",
        color=discord.Color.gold(),
        fields=[
            ("Total Sessions", f"`{len(user_sessions)}`"),
            ("Total Messages", f"`{total_messages}`"),
            ("Model", f"`{config['model']}`"),
            ("Temperature", f"`{config['temperature']}`"),
            ("Servers", f"`{len(bot.guilds)}` connected"),
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
    
    guild_id = message.guild.id if message.guild else "DM"
    user_id = message.author.id
    channel_id = message.channel.id
    user_message = message.content
    
    async with message.channel.typing():
        session = get_session(user_id, channel_id, guild_id)
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
print("     DISCORD BOT WITH MULTI-SERVER SUPPORT")
print("="*50)
print(f"Model: {config['model']}")
print("Features: Multi-server sessions, Global commands, Server stats")
print("="*50 + "\n")

bot.run(token)
