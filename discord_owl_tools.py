import discord, json, logging, datetime, requests
from discord import app_commands
from discord.ext import commands
from openai import OpenAI

with open('openrouter.env', 'r') as f:
    key = f.read().strip().split('=')[1]

with open('discord_token.env', 'r') as f:
    token = f.read().strip().split('=')[1]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)

tools = [
    {"type": "function", "function": {"name": "get_current_time", "description": "Get current date and time", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "calculate", "description": "Do math", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "get_weather", "description": "Get weather for a city", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}
]

def get_current_time():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression):
    try: return f"{expression} = {eval(expression)}"
    except Exception as e: return f"Error: {e}"

def get_weather(city):
    import requests
    try:
        url = f"https://wttr.in/{city}?format=%C+%t+%w"
        r = requests.get(url, timeout=10)
        return f"Weather in {city}: {r.text.strip()}" if r.status_code == 200 else f"Error: {city}"
    except Exception as e: return f"Error: {e}"

def execute_tool(name, args):
    if name == "get_current_time": return get_current_time()
    if name == "calculate": return calculate(args.get("expression", ""))
    if name == "get_weather": return get_weather(args.get("city", ""))
    return f"Unknown tool: {name}"

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
        r = client.chat.completions.create(model="openrouter/owl-alpha", messages=[{"role":"user","content":question}], tools=tools, tool_choice="auto")
        msg = r.choices[0].message
        if msg.tool_calls:
            results = []
            for call in msg.tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments)
                results.append(f"{name}: {execute_tool(name, args)}")
            final = client.chat.completions.create(model="openrouter/owl-alpha", messages=[{"role":"user","content":question}, msg, {"role":"tool","content":"\n".join(results), "tool_call_id": call.id}])
            answer = final.choices[0].message.content
        else:
            answer = msg.content
        await interaction.followup.send(answer[:2000])
    except Exception as e:
        await interaction.followup.send(f"Error: {e}")

bot.run(token)
