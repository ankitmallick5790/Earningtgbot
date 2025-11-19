from fastapi import FastAPI, Request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, filters, ContextTypes
import os

app = FastAPI()

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

custom_keyboard = [['Watch Ads', 'Balance'], ['Refer and Earn', 'Bonus', 'Extra']]
reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Welcome to the Money Making Bot!\nHere are your options:\n\n"
        "1. Watch Ads - Earn money by watching ads\n"
        "2. Balance - Check your current balance\n"
        "3. Refer and Earn - Get bonuses by referring friends\n"
        "4. Bonus - Claim your bonuses\n"
        "5. Extra - Additional features"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == 'Watch Ads':
        await update.message.reply_text("Feature to watch ads coming soon.")
    elif text == 'Balance':
        await update.message.reply_text("Your balance is currently 0.")
    elif text == 'Refer and Earn':
        await update.message.reply_text("Refer your friends using your unique link!")
    elif text == 'Bonus':
        await update.message.reply_text("Claim your daily bonus here.")
    elif text == 'Extra':
        await update.message.reply_text("Extra features will be available soon.")
    else:
        await update.message.reply_text("Please use the buttons below.")

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_button))

@app.post('/webhook')
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await dispatcher.process_update(update)
    return {"ok": True}

@app.get('/')
async def root():
    return {"message": "Telegram Money Making Bot webhook is running."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 10000))
    uvicorn.run(app, host='0.0.0.0', port=port)
