#!/usr/bin/env python3
# Discord Agent Bot - Simple Version

import logging
import discord
from discord import app_commands
from discord.ext import commands

with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    logger.info(f" Logged in as {bot.user}")
    await bot.tree.sync()
    logger.info(" Commands synced")

@bot.tree.command(name="ping", description="Test bot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(" Pong!")

@bot.tree.command(name="echo", description="Echo your message")
async def echo(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"You said: {message}")

print("="*50)
print("     DISCORD SIMPLE BOT")
print("="*50)
print("Commands: /ping, /echo")
print("="*50 + "\n")

bot.run(token)
