#!/usr/bin/env python3
# Quick Discord bot test

import discord
import os

# Load token
with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f' Logged in as {self.user}')
        print(f' Bot is ready!')
        await self.close()

client = MyClient(intents=discord.Intents.default())
client.run(token)
