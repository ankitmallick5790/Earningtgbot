#!/usr/bin/env python3
# This program is dedicated to the public domain under the CC0 license.
# Fixed Telegram bot webhook for Render deployment using pure Flask.
# Simplified for stability without ASGI/WSGI conflicts.

import logging
import os
import threading
from http import HTTPStatus

from flask import Flask, request, Response
import requests

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - Set these as environment variables on Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app.onrender.com")
PORT = int(os.environ.get("PORT", 10000))  # Render default is 10000
WEBHOOK_PATH = f"/webhook/{TOKEN}"

# Global application instance
application = None
app = Flask(__name__)

# Simple in-memory user state (use database for production)
user_states = {}  # user_id: last_interaction

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with custom text, instructions, and keyboard."""
    user_id = update.effective_user.id
    custom_text = (
        "Welcome to the Money-Making Bot! 🚀\n\n"
        "This bot helps you earn money through various features.\n"
        "Follow the instructions below to get started:\n\n"
        "1. Use the buttons to explore earning options.\n"
        "2. Watch ads for quick rewards.\n"
        "3. Check your balance anytime.\n"
        "4. Refer friends to earn bonuses.\n"
        "5. Claim daily bonuses and extras.\n\n"
        "Start by pressing a button below!"
    )
    
    # Check if user is new or returning
    if user_id not in user_states or user_states[user_id] == "new":
        custom_text = "🎉 Great! You're new here. " + custom_text
        user_states[user_id] = "started"
    
    # Create keyboard with 5 buttons
    keyboard = [
        [KeyboardButton("Watch Ads")],
        [KeyboardButton("Balance")],
        [KeyboardButton("Refer and Earn")],
        [KeyboardButton("Bonus")],
        [KeyboardButton("Extra")],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        text=custom_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML,
    )
    
    logger.info(f"Start command executed for user {user_id}")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages from the custom keyboard buttons."""
    user_id = update.effective_user.id
    text = update.message.text
    user_states[user_id] = text  # Track interaction
    
    if text == "Watch Ads":
        await update.message.reply_text(
            "Watch Ads feature: Coming soon! This will show video ads for rewards. "
            "Further instructions pending."
        )
    elif text == "Balance":
        await update.message.reply_text(
            "Balance: $0.00 (Demo). Your current earnings will be displayed here. "
            "Further instructions pending."
        )
    elif text == "Refer and Earn":
        await update.message.reply_text(
            "Refer and Earn: Share your referral link with friends to earn commissions. "
            "Your link: t.me/YourBot?start=ref_12345\n"
            "Further instructions pending."
        )
    elif text == "Bonus":
        await update.message.reply_text(
            "Bonus: Claim your daily bonus! +$1.00 added.\n"
            "Further instructions pending."
        )
    elif text == "Extra":
        await update.message.reply_text(
            "Extra: Special offers and tasks for more earnings.\n"
            "Further instructions pending."
        )
    else:
        # If not a button, remind to use /start
        await update.message.reply_text(
            "Use /start to begin or select from the buttons below."
        )

def init_bot():
    """Initialize the bot application in a background thread."""
    global application
    application = Application.builder().token(TOKEN).read_timeout(10).write_timeout(10).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    # Start the application
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
        poll_interval=1.0,
        timeout=10,
    )

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Handle incoming Telegram webhook updates synchronously."""
    if application is None:
        return Response(status=HTTPStatus.SERVICE_UNAVAILABLE)
    
    try:
        update_json = request.get_json(force=True)
        if update_json:
            update = Update.de_json(data=update_json, bot=application.bot)
            # Process update in the application (synchronous wrapper)
            future = asyncio.run_coroutine_threadsafe(
                application.process_update(update), application.loop
            )
            future.result(timeout=10)  # Wait for processing
        return Response(status=HTTPStatus.OK)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

@app.route("/", methods=["GET", "HEAD"])
def health_check():
    """Simple health check endpoint for Render."""
    return Response(status=HTTPStatus.OK)

def run_bot_thread():
    """Run the bot polling in a separate thread to keep Flask responsive."""
    init_bot()

if __name__ == "__main__":
    # Start bot in background thread (for local testing; Render uses gunicorn)
    bot_thread = threading.Thread(target=run_bot_thread, daemon=True)
    bot_thread.start()
    
    # For Render, use gunicorn to run Flask
    app.run(host="0.0.0.0", port=PORT, debug=False)
