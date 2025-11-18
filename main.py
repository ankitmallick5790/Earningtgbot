import logging
import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the custom keyboard layout
keyboard = [
    ['Watch Ads', 'Balance'],
    ['Refer and Earn', 'Bonus'],
    ['Extra']
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command with welcome message and keyboard."""
    welcome_text = (
        "🎉 Welcome to the Money Making Bot!\n\n"
        "💰 Earn real money through our simple system!\n"
        "👇 Use the buttons below to get started:\n\n"
        "• Watch ads to earn instantly\n"
        "• Check your balance anytime\n"
        "• Refer friends for bonus rewards\n"
        "• Claim daily bonuses\n"
        "• Access extra earning opportunities"
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    logger.info(f"User {update.effective_user.id} started the bot")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button presses from the custom keyboard."""
    text = update.message.text
    user_id = update.effective_user.id

    if text == 'Watch Ads':
        response = (
            "📺 **Watch Ads to Earn**\n\n"
            "Click the link below to watch short ads and earn up to $0.50 per ad!\n"
            "💸 Earnings will be added to your balance instantly.\n\n"
            "[Watch Ads Now] (https://example.com/watch-ads)"
        )
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"User {user_id} clicked Watch Ads")
        
    elif text == 'Balance':
        response = (
            "💰 **Your Current Balance**\n\n"
            "• Total Balance: $0.00\n"
            "• Available for Withdrawal: $0.00\n"
            "• Pending Earnings: $0.00\n\n"
            "Keep earning to reach the $5 minimum withdrawal!"
        )
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"User {user_id} checked balance")
        
    elif text == 'Refer and Earn':
        # Replace YOUR_BOT_USERNAME with your actual bot username
        referral_link = f"https://t.me/YOUR_BOT_USERNAME?start=ref_{user_id}"
        response = (
            "🔗 **Refer and Earn**\n\n"
            f"Share this link with your friends:\n"
            f"`{referral_link}`\n\n"
            "💎 Earn $1.00 for each friend who signs up!\n"
            "• 50% of your referrals' ad earnings\n"
            "• Bonus for every 5 referrals\n\n"
            "Copy and share to start earning!"
        )
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"User {user_id} viewed referral link")
        
    elif text == 'Bonus':
        response = (
            "🎁 **Daily Bonus**\n\n"
            "Claim your daily login bonus of $0.10!\n\n"
            "✅ Bonus claimed successfully!\n"
            "💰 New Balance: $0.10\n\n"
            "• Daily bonus available once per 24 hours\n"
            "• Additional bonuses on weekends"
        )
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"User {user_id} claimed daily bonus")
        
    elif text == 'Extra':
        response = (
            "⚡ **Extra Earning Opportunities**\n\n"
            "🔥 **Premium Features Coming Soon:**\n"
            "• Watch longer ads for higher payouts\n"
            "• Survey completion rewards\n"
            "• Social media tasks\n"
            "• Game rewards and challenges\n\n"
            "Stay tuned for more ways to earn!"
        )
        await update.message.reply_text(response, reply_markup=reply_markup, parse_mode='Markdown')
        logger.info(f"User {user_id} viewed extra features")
        
    else:
        # Fallback for unknown text
        await update.message.reply_text(
            "Please use the buttons below to navigate.",
            reply_markup=reply_markup
        )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors during bot operation."""
    logger.error(f"Update {update} caused error {context.error}")

async def main() -> None:
    """Main function to run the bot."""
    # Get token from environment variable
    token = os.environ.get('TELEGRAM_TOKEN')
    if not token:
        logger.error("TELEGRAM_TOKEN environment variable is required!")
        logger.error("Set it in Render Dashboard > Environment tab")
        return

    try:
        # Create the Application
        application = (
            Application.builder()
            .token(token)
            .concurrent_updates(True)
            .build()
        )

        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
        application.add_error_handler(error_handler)

        # Start the bot
        logger.info("🤖 Starting Money Making Bot...")
        logger.info(f"Bot token validated: {token[:10]}...")

        # Use the new context manager pattern for v22.5
        async with application:
            await application.initialize()
            await application.start()
            await application.updater.start_polling(
                poll_interval=1.0,
                timeout=10,
                bootstrap_retries=-1
            )
            
            logger.info("✅ Bot is running and ready to serve users!")
            logger.info("Press Ctrl+C to stop the bot")
            
            # Keep the bot running
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                logger.info("🛑 Received shutdown signal")
            finally:
                await application.updater.stop()
                await application.stop()
                await application.shutdown()
                
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    asyncio.run(main())
