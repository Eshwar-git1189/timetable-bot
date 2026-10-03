from datetime import datetime, timedelta
import pytz
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv

# --- Paste your BotFather token here ---

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN is missing. Please set it in your .env file.")
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
    await update.message.reply_markdown(TUTORIAL)
    await update.message.reply_markdown(format_day_schedule(day_name))

async def tomorrow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ist = pytz.timezone("Asia/Kolkata")
    tomorrow_day = (datetime.now(ist) + timedelta(days=1)).strftime("%A")
    await update.message.reply_markdown(TUTORIAL)
    await update.message.reply_markdown(format_day_schedule(tomorrow_day))

async def week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📚 *Weekly Schedule (Room CRC 203)*\n\n"
    for day, slots in TIMETABLE.items():
        msg += f"*{day}*:\n"
        for s in slots:
            msg += f"  • {s}\n"
        msg += "\n"
    await update.message.reply_markdown(TUTORIAL)
    await update.message.reply_markdown(msg)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("tomorrow", tomorrow))
    app.add_handler(CommandHandler("week", week))

    print("Timetable bot is active and polling...")
    app.run_polling()