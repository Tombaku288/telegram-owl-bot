import discord, ollama, logging, json, re
from discord import app_commands
from discord.ext import commands
from tools import execute_tool

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

def parse_calls(text):
    calls = []
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    stack, start = [], -1
    for i, c in enumerate(text):
        if c == '{':
            if not stack: start = i
            stack.append('{')
        elif c == '}':
            if stack:
                stack.pop()
                if not stack:
                    try:
                        obj = json.loads(text[start:i+1])
                        if 'tool_name' in obj: calls.append(obj)
                    except: pass
    return calls

def agent_chat(q):
    try:
        r = ollama.chat(model='hermes3:3b', messages=[
            {'role':'system','content':"You have tools: get_current_time, calculate, web_search, get_weather. Respond with JSON."},
            {'role':'user','content':q}
        ], options={'temperature':0.1})
        plan = r['message']['content'].strip()
        calls = parse_calls(plan)
        if not calls: return plan
        results = [f"{c.get('tool_name')}: {execute_tool(c.get('tool_name'), c.get('parameters', {}))}" for c in calls if c.get('tool_name')]
        if not results: return plan
        final = ollama.chat(model='hermes3:3b', messages=[
            {'role':'system','content':"Use tool results to answer."},
            {'role':'user','content':f"Q: {q}\n\nResults:\n" + "\n".join(results)}
        ], options={'temperature':0.3})
        return final['message']['content']
    except Exception as e:
        return f"Error: {e}"

@bot.tree.command(name="ping", description="Test")
async def ping(interaction): await interaction.response.send_message(" Pong!")

@bot.tree.command(name="chat", description="Chat")
async def chat(interaction, question: str):
    await interaction.response.defer()
    try:
        if any(w in question.lower() for w in ['weather','time','calc','search','news']):
            answer = agent_chat(question)
        else:
            r = ollama.chat(model='hermes3:3b', messages=[{'role':'user','content':question}], options={'temperature':0.7})
            answer = r['message']['content']
        await interaction.followup.send(answer[:2000])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

bot.run(token)
