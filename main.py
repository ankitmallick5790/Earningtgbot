import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ----- CONFIG -----
BOT_TOKEN = os.getenv("BOT_TOKEN")  # set in Render env vars
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "mysecretpath")  # optional

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI()

# Global application (telegram)
telegram_app: Application | None = None


# ----- HANDLERS -----

def main_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton("Watch Ads")],
        [KeyboardButton("Balance")],
        [KeyboardButton("Refer & Earn")],
        [KeyboardButton("Bonus")],
        [KeyboardButton("Extra")],
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "Welcome to your money-making bot!\n\n"
        "Use the buttons below:\n"
        "1. Watch Ads – earn by watching ads\n"
        "2. Balance – check your current balance\n"
        "3. Refer & Earn – invite friends and earn\n"
        "4. Bonus – claim daily/periodic bonuses\n"
        "5. Extra – more earning options\n"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard())


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text

    if text == "Watch Ads":
        await handle_watch_ads(update, context)
    elif text == "Balance":
        await handle_balance(update, context)
    elif text == "Refer & Earn":
        await handle_refer(update, context)
    elif text == "Bonus":
        await handle_bonus(update, context)
    elif text == "Extra":
        await handle_extra(update, context)
    else:
        # Fallback
        await update.message.reply_text(
            "Use the menu buttons below to interact with the bot.",
            reply_markup=main_keyboard(),
        )


async def handle_watch_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Add your ad display / earning logic here
    await update.message.reply_text(
        "Watch Ads: here you will see available ads to watch and earn coins."
    )


async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Get real balance from DB
    fake_balance = 0
    await update.message.reply_text(f"Your current balance is: {fake_balance} coins.")


async def handle_refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # You will later generate real referral links or codes
    refer_link = f"https://t.me/{context.bot.username}?start={user_id}"
    await update.message.reply_text(
        "Refer & Earn:\n"
        f"Share this link with friends:\n{refer_link}\n\n"
        "You will get rewards when they join and start using the bot."
    )


async def handle_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Implement daily/periodic bonus with DB & cooldown
    await update.message.reply_text(
        "Bonus: you can claim a daily bonus here. (Logic not implemented yet.)"
    )


async def handle_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # TODO: Add any extra earning tasks/features
    await update.message.reply_text(
        "Extra: additional earning options will appear here."
    )


# ----- FASTAPI ROUTES -----


@app.on_event("startup")
async def on_startup():
    """
    Build the telegram Application once at startup.
    """
    global telegram_app
    if BOT_TOKEN is None:
        logger.error("BOT_TOKEN is not set")
        raise RuntimeError("BOT_TOKEN env var is required")

    telegram_app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register handlers
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Start the application (without polling, we only use webhooks)
    await telegram_app.initialize()
    await telegram_app.start()
    logger.info("Telegram application started")


@app.on_event("shutdown")
async def on_shutdown():
    global telegram_app
    if telegram_app is not None:
        await telegram_app.stop()
        await telegram_app.shutdown()
        logger.info("Telegram application stopped")


@app.post("/webhook/{secret}")
async def telegram_webhook(secret: str, request: Request):
    """
    Telegram will POST updates to this endpoint.
    """
    if WEBHOOK_SECRET and secret != WEBHOOK_SECRET:
        return JSONResponse(status_code=403, content={"ok": False, "error": "Forbidden"})

    global telegram_app
    if telegram_app is None:
        return JSONResponse(status_code=500, content={"ok": False, "error": "Bot not ready"})

    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.process_update(update)

    return JSONResponse(content={"ok": True})


@app.get("/")
async def root():
    return {"status": "ok", "message": "Telegram bot is running"}

