import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define keyboard layout
keyboard = [
    ['Watch Ads', 'Balance'],
    ['Refer and Earn', 'Bonus'],
    ['Extra']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Welcome to the Money Making Bot!\n\n"
        "Earn money by watching ads, referring friends, and more.\n"
        "Use the buttons below to get started."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

# Button handler
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    if text == 'Watch Ads':
        await update.message.reply_text("Click here to watch ads and earn money!", reply_markup=reply_markup)
    elif text == 'Balance':
        await update.message.reply_text("Your current balance is $0.00", reply_markup=reply_markup)
    elif text == 'Refer and Earn':
        await update.message.reply_text("Share your referral link to earn rewards!", reply_markup=reply_markup)
    elif text == 'Bonus':
        await update.message.reply_text("Claim your daily bonus here!", reply_markup=reply_markup)
    elif text == 'Extra':
        await update.message.reply_text("Extra features coming soon!", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Please use the buttons below.", reply_markup=reply_markup)

def main():
    # Get the bot token from environment variables for Render
    import os
    TOKEN = os.environ.get('TELEGRAM_TOKEN', 'YOUR_TOKEN')

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    application.run_polling()

if __name__ == '__main__':
    main()
