from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Custom keyboard buttons
custom_keyboard = [['Watch Ads', 'Balance'], ['Refer and Earn', 'Bonus', 'Extra']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Custom welcome message and instruction
    welcome_message = (
        "Welcome to the Money Making Bot!\nHere are your options:\n\n"
        "1. Watch Ads - Earn money by watching ads\n"
        "2. Balance - Check your current balance\n"
        "3. Refer and Earn - Get bonuses by referring friends\n"
        "4. Bonus - Claim your bonuses\n"
        "5. Extra - Additional features"
    )
    
    # Create ReplyKeyboardMarkup with custom buttons
    reply_markup = ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)

    # Send the welcome message with custom keyboard
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Placeholder handling for each button press
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

if __name__ == '__main__':
    import os

    token = os.environ.get('TELEGRAM_TOKEN')
    assert token, 'TELEGRAM_TOKEN environment variable missing'

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_button))

    # Run the bot
    app.run_polling()
