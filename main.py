#!/usr/bin/env python3
import os
import logging
from http import HTTPStatus

from flask import Flask, request, Response
import asyncio
import nest_asyncio

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Allow nested event loops (needed for Flask + asyncio on Render)
nest_asyncio.apply()

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Environment variables from Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # e.g. https://yourrenderapp.onrender.com
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_PATH = f"/webhook/{TOKEN}"

if not TOKEN or not WEBHOOK_URL:
    logger.error("Please set TELEGRAM_BOT_TOKEN and WEBHOOK_URL environment variables.")
    exit(1)

# In-memory user session store (for demo; replace with DB for production)
user_states = {}

# Initialize Flask app
app = Flask(__name__)

# Initialize telegram Application globally
application = Application.builder().token(TOKEN).build()

# Handlers:
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} triggered /start")

    text = (
        "Welcome to the Money-Making Bot! 🚀\n\n"
        "Use the buttons below to:\n"
        "1. Watch ads\n"
        "2. Check balance\n"
        "3. Refer and earn\n"
        "4. Claim bonuses\n"
        "5. Explore extras\n\n"
        "Start by pressing any button below!"
    )

    keyboard = [
        [KeyboardButton("Watch Ads")],
        [KeyboardButton("Balance")],
        [KeyboardButton("Refer and Earn")],
        [KeyboardButton("Bonus")],
        [KeyboardButton("Extra")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    user_states[user_id] = text
    logger.info(f"User {user_id} pressed button: {text}")

    responses = {
        "Watch Ads": "Watch Ads feature coming soon! Stay tuned for rewards.",
        "Balance": "Your current balance: $0.00 (demo).",
        "Refer and Earn": f"Share your referral link: https://t.me/{context.bot.username}?start=ref_{user_id}",
        "Bonus": "Congrats! You claimed a daily bonus of $1.00.",
        "Extra": "Extra features coming soon! Keep watching here.",
    }

    reply = responses.get(text, "Please use the provided buttons to interact.")
    await update.message.reply_text(reply)

# Setup handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))


# Flask route for Telegram webhook
@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    update_json = request.get_json(force=True)
    update = Update.de_json(update_json, application.bot)

    # Use new event loop for Flask sync context
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.process_update(update))
    loop.close()

    return Response(status=HTTPStatus.OK)

# Health check endpoint for Render
@app.route("/", methods=["GET", "HEAD"])
def health():
    return Response("Bot is alive!", status=HTTPStatus.OK)

# Main run
if __name__ == "__main__":
    # Before starting, set webhook with Telegram API
    import requests

    webhook_url = f"{WEBHOOK_URL.rstrip('/')}{WEBHOOK_PATH}"
    resp = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={webhook_url}"
    )
    logger.info(f"SetWebhook response: {resp.text}")

    logger.info(f"Starting Flask server on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
