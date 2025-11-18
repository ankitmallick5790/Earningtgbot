import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create the keyboard
def create_keyboard():
    keyboard = [
        ['📺 Watch Ads', '💰 Balance'],
        ['👥 Refer & Earn', '🎁 Bonus'],
        ['⚡ Extra']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message with the custom keyboard."""
    user = update.effective_user
    welcome_message = (
        f"🎉 Welcome {user.first_name}! 🎉\n\n"
        "💰 **MONEY MAKING BOT**\n\n"
        "Earn real money easily:\n"
        "• Watch short ads for instant cash\n"
        "• Refer friends for bonuses\n"
        "• Claim daily rewards\n\n"
        "💡 **Minimum withdrawal: $5**\n"
        "👇 Tap any button to start earning!"
    )
    
    await update.message.reply_text(
        welcome_message, 
        reply_markup=create_keyboard(),
        parse_mode='Markdown'
    )
    logger.info(f"User {user.id} started the bot")

# Handle button presses
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process messages and button clicks."""
    text = update.message.text
    user_id = update.effective_user.id
    
    # Watch Ads button
    if text == '📺 Watch Ads':
        response = (
            "📺 **WATCH ADS TO EARN**\n\n"
            "💸 **Earnings:** $0.10 - $0.50 per ad\n"
            "⏱️ **Duration:** 15-30 seconds\n"
            "⚡ **Instant Payout** to your balance\n\n"
            "🔗 Click below to watch your first ad:\n"
            "[START WATCHING ADS](https://example.com/ads)\n\n"
            "📊 **Today's earnings: $0.00**"
        )
        await update.message.reply_text(response, reply_markup=create_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} clicked Watch Ads")
    
    # Balance button
    elif text == '💰 Balance':
        response = (
            "💰 **YOUR BALANCE**\n\n"
            "💵 **Total Earnings:** $0.00\n"
            "💎 **Available for Withdrawal:** $0.00\n"
            "⏳ **Pending:** $0.00\n\n"
            "🎯 **Withdrawal minimum:** $5.00\n"
            "📈 **Progress to next withdrawal:** 0%\n\n"
            "💡 *Keep watching ads and referring friends!*\n"
            "*Payment methods: PayPal, Crypto, Bank Transfer*"
        )
        await update.message.reply_text(response, reply_markup=create_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} checked balance")
    
    # Refer & Earn button
    elif text == '👥 Refer & Earn':
        # Replace 'YOUR_BOT_USERNAME' with your actual bot username
        bot_username = "YOUR_BOT_USERNAME"  # e.g., "MyMoneyBot"
        referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        response = (
            "👥 **REFER & EARN**\n\n"
            f"🔗 **Your Referral Link:**\n"
            f"`{referral_link}`\n\n"
            "💰 **Earning Structure:**\n"
            "• $1.00 bonus per referral signup\n"
            "• 30% of your referrals' ad earnings\n"
            "• $5 bonus for every 10 active referrals\n\n"
            "📊 **Your Stats:**\n"
            "• Total Referrals: 0\n"
            "• Active Referrals: 0\n"
            "• Referral Earnings: $0.00\n\n"
            "📱 *Share on social media, WhatsApp, or Discord!*"
        )
        await update.message.reply_text(response, reply_markup=create_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} viewed referral system")
    
    # Bonus button
    elif text == '🎁 Bonus':
        response = (
            "🎁 **DAILY BONUS**\n\n"
            "✨ **Today's Login Bonus: $0.10**\n"
            "✅ *Bonus claimed successfully!*\n"
            "💰 *Added to your balance*\n\n"
            "🎯 **Bonus Schedule:**\n"
            "• Daily Login: $0.10\n"
            "• 7-Day Streak: $1.00\n"
            "• Weekend Special: $0.25\n\n"
            "⏰ *Next bonus available in: 24 hours*"
        )
        await update.message.reply_text(response, reply_markup=create_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} claimed bonus")
    
    # Extra button
    elif text == '⚡ Extra':
        response = (
            "⚡ **EXTRA EARNING OPPORTUNITIES**\n\n"
            "🔥 **Premium Features:**\n"
            "• High-Paying Video Ads ($1.00+)\n"
            "• Paid Surveys ($2.00 - $10.00)\n"
            "• Social Media Tasks ($0.50)\n"
            "• Game Challenges ($5.00+ rewards)\n\n"
            "💎 **VIP Membership:** $9.99/month\n"
            "• 2x ad earnings\n"
            "• Priority withdrawals\n"
            "• Exclusive bonus events\n\n"
            "📈 *Coming soon: Affiliate programs & cashback offers!*"
        )
        await update.message.reply_text(response, reply_markup=create_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} viewed extra opportunities")
    
    # Handle /start command in text
    elif text.lower() == '/start':
        await start(update, context)
    
    # Unknown messages
    else:
        await update.message.reply_text(
            "❓ **Please use the buttons below to navigate**\n\n"
            "Or type /start to begin!",
            reply_markup=create_keyboard()
        )

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    """Start the bot."""
    # Get the token from environment variable
    token = os.getenv('TELEGRAM_TOKEN')
    
    if token is None:
        logger.error("❌ TELEGRAM_TOKEN environment variable is not set!")
        logger.error("Please set it in your Render dashboard under Environment Variables")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Run the bot
    logger.info("🚀 Starting Money Making Bot...")
    logger.info(f"🤖 Bot token loaded: {token[:10]}...")
    
    # Start polling
    application.run_polling(
        poll_interval=1.0,
        timeout=10,
        bootstrap_retries=5
    )

if __name__ == '__main__':
    main()
