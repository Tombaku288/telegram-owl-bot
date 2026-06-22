#!/usr/bin/env python3
# FINAL POLISHED DISCORD BOT - Week 4 Day 5
# All features combined: embeds, cooldowns, error handling, multi-server

import os
import json
import logging
import time
import ollama
import discord
from discord import app_commands
from discord.ext import commands

# ===== CONFIGURATION =====
with open('config.json', 'r') as f:
    config = json.load(f)

with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

# ===== LOGGING =====
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ===== BOT SETUP =====
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ===== USER SESSIONS =====
user_sessions = {}

def get_session(guild_id, user_id, channel_id):
    key = f"{guild_id}_{user_id}_{channel_id}"
    if key not in user_sessions:
        user_sessions[key] = [
            {'role': 'system', 'content': config['system_prompt']}
        ]
    return user_sessions[key]

# ===== EMBED HELPER =====
def create_embed(title, description, color=discord.Color.blue(), fields=None, footer=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if fields:
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)
    if footer:
        embed.set_footer(text=footer)
    return embed

# ===== ON READY =====
@bot.event
async def on_ready():
    logger.info(f" Logged in as {bot.user}")
    logger.info(f" Connected to {len(bot.guilds)} servers")
    await bot.change_presence(activity=discord.Game(name=f"/help on {len(bot.guilds)} servers"))
    try:
        synced = await bot.tree.sync()
        logger.info(f" Synced {len(synced)} slash commands")
    except Exception as e:
        logger.error(f"Failed to sync: {e}")

# ===== SLASH COMMANDS =====

@bot.tree.command(name="hello", description="Say hello to Hermes")
async def slash_hello(interaction: discord.Interaction):
    embed = create_embed(
        title=" Hello!",
        description="I am **Hermes**, your AI assistant. Type `/help` for commands.",
        color=discord.Color.green()
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="Show all available commands")
@app_commands.checks.cooldown(1, 10.0)  # 1 use per 10 seconds
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
            ("`/about`", "About Hermes"),
            ("`/clear`", "Clear your conversation memory"),
            ("`/stats`", "Show statistics (Admin only)"),
            ("`/servers`", "List all servers (Admin only)")
        ],
        footer="Type a message to chat with Hermes!"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Check bot latency")
async def slash_ping(interaction: discord.Interaction):
    start = time.time()
    await interaction.response.defer()
    latency = round((time.time() - start) * 1000)
    embed = create_embed(
        title=" Pong!",
        description=f"**Latency:** `{latency}ms`\n**WebSocket:** `{round(bot.latency * 1000)}ms`",
        color=discord.Color.green()
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="status", description="Show bot status")
async def slash_status(interaction: discord.Interaction):
    await interaction.response.defer()
    
    try:
        ollama.chat(model=config['model'], messages=[{'role': 'user', 'content': 'OK'}], options={'max_tokens': 2})
        ollama_status = " Connected"
        color = discord.Color.green()
    except:
        ollama_status = " Error"
        color = discord.Color.red()
    
    total_messages = 0
    for session in user_sessions.values():
        total_messages += len(session)
    
    embed = create_embed(
        title=" Bot Status",
        description=f"Server: **{interaction.guild.name if interaction.guild else 'DM'}**",
        color=color,
        fields=[
            ("Model", f"`{config['model']}`"),
            ("Temperature", f"`{config['temperature']}`"),
            ("Ollama", ollama_status),
            ("Sessions", f"`{len(user_sessions)}`"),
            ("Total Messages", f"`{total_messages}`"),
            ("Servers", f"`{len(bot.guilds)}`")
        ]
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="about", description="About Hermes")
async def slash_about(interaction: discord.Interaction):
    embed = create_embed(
        title=" About Hermes",
        description="I am an AI assistant powered by **Hermes 3:3b**.",
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

@bot.tree.command(name="clear", description="Clear your conversation memory")
async def slash_clear(interaction: discord.Interaction):
    guild_id = interaction.guild_id or "DM"
    key = f"{guild_id}_{interaction.user.id}_{interaction.channel_id}"
    
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
            ("Servers", f"`{len(bot.guilds)}`"),
            ("Commands", f"`{len(bot.tree.get_commands())}`")
        ],
        footer="Admin only"
    )
    await interaction.followup.send(embed=embed)

@bot.tree.command(name="servers", description="List all servers (Admin only)")
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
        description=f"I am connected to {len(bot.guilds)} server(s):",
        color=discord.Color.gold(),
        fields=[("Servers", server_list)],
        footer=f"Requested by {interaction.user.display_name}"
    )
    await interaction.followup.send(embed=embed)

# ===== TEXT CHAT =====
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
        session = get_session(guild_id, user_id, channel_id)
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

# ===== ERROR HANDLING =====
@slash_help.error
async def help_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        embed = create_embed(
            title=" Cooldown",
            description=f"Please wait `{round(error.retry_after)}` seconds before using this command again.",
            color=discord.Color.yellow()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ===== MAIN =====
print("\n" + "="*50)
print("      FINAL POLISHED DISCORD BOT")
print("="*50)
print(f"Model: {config['model']}")
print(f"Temperature: {config['temperature']}")
print("Commands: /hello, /help, /ping, /status, /about, /clear, /stats, /servers")
print("Features: Embeds, Cooldowns, Error handling, Multi-server")
print("="*50 + "\n")

bot.run(token)
