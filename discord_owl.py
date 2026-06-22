#!/usr/bin/env python3
# Discord Bot with OpenRouter Owl Alpha

import discord, json, logging
from discord import app_commands
from discord.ext import commands
from openai import OpenAI

# Load config
with open('openrouter.env', 'r') as f:
    key = f.read().strip().split('=')[1]

with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

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

@bot.tree.command(name="chat", description="Chat with Owl Alpha")
async def chat(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        response = client.chat.completions.create(
            model="openrouter/owl-alpha",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        await interaction.followup.send(answer[:2000])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

bot.run(token)
