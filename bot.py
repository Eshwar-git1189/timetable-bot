import os
import asyncio
from datetime import datetime, timedelta
import pytz
from aiohttp import web
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN is missing. Please set it in your .env file or Render environment.")

# P.E.S. College of Engineering Mandya - VII Sem CSE-A (Room CRC 203)
TIMETABLE = {
    "Monday": [
        "09:30 - 10:30: Research Methodology & IPR (Prof. Sindhu B S)",
        "10:30 - 11:30: Cryptography & Network Security (Prof. Raghavendra Babu T M)",
        "11:30 - 11:45: ☕ Break",
        "11:45 - 12:45: Social Network Analysis (Prof. P Prasanna)",
        "12:45 - 01:45: Mobile Security (Prof. Suraj B S)",
        "01:45 onwards: 🍽️ Lunch / Free"
    ],
    "Tuesday": [
        "09:30 - 10:30: Machine Learning (Dr. M L Anitha)",
        "10:30 - 11:30: Mobile Security (Prof. Suraj B S)",
        "11:30 - 11:45: ☕ Break",
        "11:45 - 12:45: Cryptography & Network Security (Prof. Raghavendra Babu T M)",
        "12:45 - 01:45: Social Network Analysis (Prof. P Prasanna)",
        "01:45 onwards: 🍽️ Lunch / Free"
    ],
    "Wednesday": [
        "09:30 - 10:30: Cryptography & Network Security (Prof. Raghavendra Babu T M)",
        "10:30 - 11:30: Machine Learning (Dr. M L Anitha)",
        "11:30 - 11:45: ☕ Break",
        "11:45 - 12:45: Mobile Security (Prof. Suraj B S)",
        "12:45 - 01:45: Research Methodology & IPR (Prof. Sindhu B S)",
        "01:45 onwards: 🍽️ Lunch / Free"
    ],
    "Thursday": [
        "09:30 - 10:30: Social Network Analysis (Prof. P Prasanna)",
        "10:30 - 11:30: Research Methodology & IPR (Prof. Sindhu B S)",
        "11:30 - 11:45: ☕ Break",
        "11:45 - 12:45: Machine Learning (Dr. M L Anitha)",
        "12:45 - 01:45: Cryptography & Network Security (Prof. Raghavendra Babu T M)",
        "01:45 onwards: 🍽️ Lunch / Free"
    ],
    "Friday": [
        "09:30 - 11:30: Machine Learning Lab (4L)",
        "11:30 - 11:45: ☕ Break",
        "11:45 - 12:45: Research Methodology & IPR (Prof. Sindhu B S)",
        "12:45 - 01:45: Machine Learning (Dr. M L Anitha)",
        "01:45 - 02:45: 🍽️ Lunch Break",
        "02:45 - 03:45: Social Network Analysis (Prof. P Prasanna)",
        "03:45 - 04:45: Mobile Security (Prof. Suraj B S)"
    ],
    "Saturday": [
        "No classes scheduled today! 🎉"
    ],
    "Sunday": [
        "Sunday holiday! 🏖️"
    ]
}

def format_day_schedule(day: str) -> str:
    periods = TIMETABLE.get(day, ["No classes scheduled."])
    text = f"🏛️ *Room: CRC 203*\n📅 *Schedule for {day}*:\n\n"
    for period in periods:
        text += f"• {period}\n"
    return text

TUTORIAL = (
    "📖 *Quick tutorial*\n"
    "Use /today for today's schedule, /tomorrow for tomorrow's, "
    "or /week for the full week."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 *PESCE VII Sem CSE-A Timetable Bot*\n\n"
        f"{TUTORIAL}"
    )
    await update.message.reply_markdown(msg)

async def today(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ist = pytz.timezone("Asia/Kolkata")
    day_name = datetime.now(ist).strftime("%A")
    await update.message.reply_markdown(format_day_schedule(day_name))
    await update.message.reply_markdown(TUTORIAL)

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ist = pytz.timezone("Asia/Kolkata")
    tomorrow_day = (datetime.now(ist) + timedelta(days=1)).strftime("%A")
    await update.message.reply_markdown(format_day_schedule(tomorrow_day))
    await update.message.reply_markdown(TUTORIAL)

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📚 *Weekly Schedule (Room CRC 203)*\n\n"
    for day, slots in TIMETABLE.items():
        msg += f"*{day}*:\n"
        for s in slots:
            msg += f"  • {s}\n"
        msg += "\n"
    await update.message.reply_markdown(msg)
    await update.message.reply_markdown(TUTORIAL)

# --- Render Health Check Endpoint ---
async def health_check(request):
    return web.Response(text="Timetable Bot is healthy and polling Telegram.")

async def main():
    # 1. Setup Telegram Application
    bot_app = ApplicationBuilder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("today", today))
    bot_app.add_handler(CommandHandler("tomorrow", tomorrow))
    bot_app.add_handler(CommandHandler("week", week))

    # Initialize bot and start polling in the background
    await bot_app.initialize()
    await bot_app.start()
    await bot_app.updater.start_polling()

    # 2. Setup Aiohttp Web Server
    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    web_app.router.add_get("/health", health_check)

    # Render automatically injects the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    print(f"Timetable bot is active and web server bound to port {port}...")

    # Keep both running forever
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())