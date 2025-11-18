#!/usr/bin/env python3
# This program is dedicated to the public domain under the CC0 license.
# Simplified Telegram bot using pure webhook for Render deployment.
# Based on official python-telegram-bot v20+ custom webhook example.

import logging
import os
from http import HTTPStatus
import asyncio

from flask import Flask, Response, request
from asgiref.wsgi import WsgiToAsgi
import uvicorn

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

# Reduce httpx logging noise
logging.getLogger("httpx").setLevel(logging.WARNING)

# Configuration - Set these as environment variables on Render
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app.onrender.com")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_PATH = f"/webhook/{TOKEN}"

# Simple in-memory user state (use database for production)
user_states = {}

async def start(update: Update, context: ContextTypes[ExtBot, dict, dict, dict]) -> None:
    """Handle /start command with custom text, instructions, and keyboard."""
    user_id = update.effective_user.id
    logger.info(f"Received /start from user {user_id}. Processing...")
    
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
    
    logger.info(f"Start command executed successfully for user {user_id}")

async def handle_buttons(update: Update, context: ContextTypes[ExtBot, dict, dict, dict]) -> None:
    """Handle messages from the custom keyboard buttons."""
    user_id = update.effective_user.id
    text = update.message.text
    user_states[user_id] = text  # Track interaction
    logger.info(f"Button '{text}' pressed by user {user_id}")
    
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
        await update.message.reply_text(
            "Use /start to begin or select from the buttons below."
        )

async def main() -> None:
    """Start the bot and webhook server."""
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    # Create application (no updater for custom webhook)
    application = (
        Application.builder().token(TOKEN).updater(None).build()
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    
    # Set webhook
    webhook_url = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
    await application.bot.set_webhook(url=webhook_url, allowed_updates=Update.ALL_TYPES)
    logger.info(f"Webhook set to {webhook_url}")
    
    # Create Flask app
    flask_app = Flask(__name__)
    
    @flask_app.post(WEBHOOK_PATH)
    async def webhook_update() -> Response:
        """Handle incoming Telegram updates."""
        try:
            update = Update.de_json(data=request.get_json(), bot=application.bot)
            if update:
                logger.info(f"Received update: {update.update_id} from user {update.effective_user.id if update.effective_user else 'unknown'}")
                await application.process_update(update)
        except Exception as e:
            logger.error(f"Webhook processing error: {e}")
        
        return Response(status=HTTPStatus.OK)
    
    @flask_app.route("/", methods=["GET", "HEAD"])
    async def health_check():
        """Health check for Render."""
        return Response(status=HTTPStatus.OK)
    
    # Convert to ASGI and run with Uvicorn
    asgi_app = WsgiToAsgi(flask_app)
    
    config = uvicorn.Config(
        app=asgi_app,
        host="0.0.0.0",
        port=PORT,
        log_level="info",
        use_colors=False,
    )
    webserver = uvicorn.Server(config)
    
    # Run everything
    async with application:
        await application.start()
        await application.updater.start_polling(  # This processes updates from webhook
            drop_pending_updates=True,
            poll_interval=1.0,
            timeout=10,
        )
        try:
            await webserver.serve()
        finally:
            await application.updater.stop()
            await application.stop()

if __name__ == "__main__":
    asyncio.run(main())
