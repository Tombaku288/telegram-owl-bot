import discord
from discord import app_commands
from discord.ext import commands
import ollama
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

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

@bot.tree.command(name="chat", description="Chat with Hermes")
async def chat(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    try:
        r = ollama.chat(model='hermes3:3b', messages=[{'role':'user','content':question}], options={'temperature':0.7})
        await interaction.followup.send(r['message']['content'][:2000])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

bot.run(token)
