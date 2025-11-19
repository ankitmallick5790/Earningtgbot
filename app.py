import os
from fastapi import FastAPI, Request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TELEGRAM_TOKEN)

custom_keyboard = [['Watch Ads', 'Balance'], ['Refer and Earn', 'Bonus', 'Extra']]
reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "Welcome to the Money Making Bot!\n"
        "Here are your options:\n\n"
        "1. Watch Ads - Earn money by watching ads\n"
        "2. Balance - Check your current balance\n"
        "3. Refer and Earn - Get bonuses by referring friends\n"
        "4. Bonus - Claim your bonuses\n"
        "5. Extra - Additional features"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    responses = {
        "Watch Ads": "Feature to watch ads coming soon.",
        "Balance": "Your balance is currently 0.",
        "Refer and Earn": "Refer your friends using your unique link!",
        "Bonus": "Claim your daily bonus here.",
        "Extra": "Extra features will be available soon."
    }
    await update.message.reply_text(responses.get(text, "Please use the buttons below."))

application = Application.builder().token(TELEGRAM_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

@app.get("/")
async def root():
    return {"message": "Telegram Money Making Bot webhook is running."}

def set_webhook():
    if WEBHOOK_URL:
        bot.set_webhook(WEBHOOK_URL)
        print(f"Webhook set to {WEBHOOK_URL}")
    else:
        print("WEBHOOK_URL is not set. Please configure it in environment variables.")

if __name__ == "__main__":
    set_webhook()
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
