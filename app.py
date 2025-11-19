import os
import asyncio
from fastapi import FastAPI, Request, Response
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Initialize FastAPI
app = FastAPI()

# Get environment variables
TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://yourapp.onrender.com/webhook

# Initialize bot
bot = Bot(token=TOKEN)

# Create Application instance
ptb_app = Application.builder().token(TOKEN).updater(None).build()

# Keyboard buttons
keyboard = [['Watch Ads', 'Balance'], ['Refer and Earn', 'Bonus', 'Extra']]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# Command handlers
async def start_command(update: Update, context):
    await update.message.reply_text(
        "💰 Welcome to Money Making Bot!\n\n"
        "Choose an option below:",
        reply_markup=markup
    )


async def button_handler(update: Update, context):
    text = update.message.text
    
    if text == 'Watch Ads':
        response = "📺 Watch ads feature coming soon!"
    elif text == 'Balance':
        response = "💵 Your balance: $0.00"
    elif text == 'Refer and Earn':
        response = "👥 Refer friends and earn rewards!"
    elif text == 'Bonus':
        response = "🎁 Daily bonus feature coming soon!"
    elif text == 'Extra':
        response = "⚡ Extra features coming soon!"
    else:
        response = "Please use the buttons below ⬇️"
    
    await update.message.reply_text(response)


# Register handlers
ptb_app.add_handler(CommandHandler("start", start_command))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))


# FastAPI routes
@app.post("/webhook")
async def webhook_endpoint(request: Request):
    try:
        json_data = await request.json()
        update = Update.de_json(json_data, bot)
        await ptb_app.process_update(update)
        return Response(status_code=200)
    except Exception as e:
        print(f"Error: {e}")
        return Response(status_code=500)


@app.get("/")
async def root():
    return {"status": "Bot is running", "webhook": WEBHOOK_URL}


@app.on_event("startup")
async def on_startup():
    # Set webhook on startup
    if WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
        print(f"✅ Webhook set to: {WEBHOOK_URL}")
    else:
        print("⚠️ WEBHOOK_URL not set!")
    
    # Initialize application
    await ptb_app.initialize()
    await ptb_app.start()


@app.on_event("shutdown")
async def on_shutdown():
    await ptb_app.stop()
    await ptb_app.shutdown()


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
