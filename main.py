#!/usr/bin/env python3
# This program is dedicated to the public domain under the CC0 license.
# Enhanced Telegram bot with improved /start command for money-making features.
# Uses webhook for Render deployment.

import asyncio
import logging
import os
from http import HTTPStatus

import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask, Response, request

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ExtBot,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration - Set these as environment variables on Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app.onrender.com")
PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_PATH = f"/webhook/{TOKEN}"

# Simple in-memory user state (use database for production)
user_states = {}  # user_id: last_interaction

async def start(update: Update, context: ContextTypes[ExtBot, dict, dict, dict]) -> None:
    """Handle /start command with custom text, instructions, and keyboard.
    Enhanced to check for first-time or returning users."""
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

async def handle_buttons(update: Update, context: ContextTypes[ExtBot, dict, dict, dict]) -> None:
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

async def main() -> None:
    """Set up the bot application and webhook server."""
    application = Application.builder().token(TOKEN).updater(None).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    # Set webhook
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}{WEBHOOK_PATH}")
    
    # Set up Flask app for webhook
    flask_app = Flask(__name__)
    
    @flask_app.route(WEBHOOK_PATH, methods=["POST"])
    def webhook() -> Response:
        """Handle incoming Telegram updates synchronously for Flask."""
        update_json = request.get_json()
        if update_json:
            update = Update.de_json(data=update_json, bot=application.bot)
            asyncio.create_task(application.process_update(update))
        return Response(status=HTTPStatus.OK)
    
    # Run webserver with Uvicorn for ASGI support
    config = uvicorn.Config(
        app=WsgiToAsgi(flask_app),
        port=PORT,
        use_colors=False,
        host="0.0.0.0",
    )
    webserver = uvicorn.Server(config)
    
    async with application:
        await application.initialize()
        await application.start()
        await webserver.serve()
        await application.stop()
        await application.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
