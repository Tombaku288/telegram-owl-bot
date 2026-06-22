import os, json, logging, datetime, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENROUTER_KEY = os.environ.get('OPENROUTER_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment")
if not OPENROUTER_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in environment")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_KEY)

tools = [
    {"type": "function", "function": {"name": "get_current_time", "description": "Get current date and time", "parameters": {"type": "object", "properties": {}, "required": []}}},
    {"type": "function", "function": {"name": "calculate", "description": "Do math", "parameters": {"type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}},
    {"type": "function", "function": {"name": "get_weather", "description": "Get weather for a city", "parameters": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}}
]

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression):
    try: return f"{expression} = {eval(expression)}"
    except Exception as e: return f"Error: {e}"

def get_weather(city):
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

user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" Hello! I am Owl Alpha. Send /help for commands.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("/start - Start\n/help - Help\n/ping - Latency\n/clear - Clear memory\n/chat <question> - Ask with tools")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(" Pong!")

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in user_sessions:
        del user_sessions[user_id]
    await update.message.reply_text(" Memory cleared!")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("Usage: /chat <question>")
        return
    await update.message.reply_text(" Thinking...")
    try:
        r = client.chat.completions.create(
            model="openrouter/owl-alpha",
            messages=[{"role": "user", "content": question}],
            tools=tools,
            tool_choice="auto"
        )
        msg = r.choices[0].message
        if msg.tool_calls:
            results = []
            for call in msg.tool_calls:
                name = call.function.name
                args = json.loads(call.function.arguments)
                result = execute_tool(name, args)
                results.append(f"{name}: {result}")
                logger.info(f" {name}  {result}")
            messages = [
                {"role": "user", "content": question},
                msg,
                {"role": "tool", "content": "\n".join(results), "tool_call_id": call.id}
            ]
            final = client.chat.completions.create(
                model="openrouter/owl-alpha",
                messages=messages
            )
            answer = final.choices[0].message.content
        else:
            answer = msg.content
        await update.message.reply_text(answer[:4000])
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("ping", ping))
app.add_handler(CommandHandler("clear", clear))
app.add_handler(CommandHandler("chat", chat))

print(" Telegram bot with Owl Alpha running...")
app.run_polling()
