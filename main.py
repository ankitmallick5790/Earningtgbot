import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Create the custom keyboard
def get_main_keyboard():
    keyboard = [
        ['📺 Watch Ads', '💰 Balance'],
        ['👥 Refer & Earn', '🎁 Bonus'],
        ['⚡ Extra']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with welcome message."""
    user = update.effective_user
    welcome_msg = (
        f"🎉 Hey {user.first_name}! Welcome to Money Maker Bot! 🎉\n\n"
        "💰 *Earn Real Money Easily:*\n\n"
        "• Watch ads (15-30s) → $0.10-$0.50 each\n"
        "• Refer friends → $1.00 bonus each\n"
        "• Daily login → $0.10 free\n"
        "• Weekend bonuses → Extra rewards\n\n"
        "💸 *Minimum withdrawal: $5.00*\n"
        "💳 *Payment methods: PayPal, Crypto*\n\n"
        "👇 Tap any button below to start earning!"
    )
    
    await update.message.reply_text(
        welcome_msg,
        reply_markup=get_main_keyboard(),
        parse_mode='Markdown'
    )
    logger.info(f"User {user.id} ({user.first_name}) started the bot")

# Handle all text messages (including button clicks)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button clicks and text messages."""
    text = update.message.text
    user_id = update.effective_user.id
    
    # Watch Ads button
    if text == '📺 Watch Ads':
        response = (
            "📺 *Watch Ads to Earn Money*\n\n"
            "💸 *Earnings per ad:* $0.10 - $0.50\n"
            "⏱️ *Duration:* 15-30 seconds\n"
            "⚡ *Payout:* Instant to your balance\n\n"
            "🔗 *Ready to earn? Click below:*\n"
            "[START WATCHING ADS](https://example.com/ads)\n\n"
            "📊 *Today's ad earnings: $0.00*\n"
            "*Tip: Watch 5+ ads daily for bonus rewards!*"
        )
        await update.message.reply_text(
            response,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} clicked Watch Ads")
    
    # Balance button
    elif text == '💰 Balance':
        response = (
            "💰 *Your Account Balance*\n\n"
            "💵 *Total Earnings:* $0.00\n"
            "💎 *Available for Withdrawal:* $0.00\n"
            "⏳ *Pending Earnings:* $0.00\n\n"
            "🎯 *Next Withdrawal Milestone:* $5.00\n"
            "📈 *Progress:* 0% (0/$5.00)\n\n"
            "💳 *Available Payment Methods:*\n"
            "• PayPal\n"
            "• Bitcoin\n"
            "• Bank Transfer\n\n"
            "*Keep earning to unlock withdrawals!*"
        )
        await update.message.reply_text(
            response,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} checked balance")
    
    # Refer & Earn button
    elif text == '👥 Refer & Earn':
        # Replace with your actual bot username (without @ or 'bot')
        bot_username = "MoneyMakerBot"  # Change this!
        referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        response = (
            "👥 *Refer Friends & Earn Big!*\n\n"
            f"🔗 *Your Unique Referral Link:*\n"
            f"`{referral_link}`\n\n"
            "💰 *Earning Structure:*\n"
            "• $1.00 bonus per signup\n"
            "• 30% of friends' ad earnings\n"
            "• $5 bonus for 10 active referrals\n"
            "• $25 bonus for 50 active referrals\n\n"
            "📊 *Your Referral Stats:*\n"
            "• Total Referrals: 0\n"
            "• Active Referrals: 0\n"
            "• Referral Earnings: $0.00\n\n"
            "📱 *Share on: WhatsApp, Discord, Instagram, Twitter*\n"
            "*Pro tip: Create a referral group for max earnings!*"
        )
        await update.message.reply_text(
            response,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} viewed referral system")
    
    # Bonus button
    elif text == '🎁 Bonus':
        response = (
            "🎁 *Daily Login Bonus!*\n\n"
            "✨ *Congratulations!*\n"
            "✅ *You've claimed your $0.10 daily bonus!*\n"
            "💰 *Added to your balance automatically*\n\n"
            "🎯 *Bonus Tiers:*\n"
            "• Daily Login: $0.10\n"
            "• 3-Day Streak: $0.30\n"
            "• 7-Day Streak: $1.00\n"
            "• Weekend Special: $0.25\n\n"
            "⏰ *Next bonus available:* 24 hours\n"
            "*Don't miss your daily login!*"
        )
        await update.message.reply_text(
            response,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} claimed daily bonus")
    
    # Extra button
    elif text == '⚡ Extra':
        response = (
            "⚡ *Extra Earning Opportunities*\n\n"
            "🔥 *Premium Features Coming Soon:*\n\n"
            "💎 *VIP Membership* ($9.99/month):\n"
            "• 2x ad earnings multiplier\n"
            "• Priority 24h withdrawals\n"
            "• Exclusive high-paying ads\n"
            "• Personal earnings coach\n\n"
            "🎮 *Game & Task Rewards:*\n"
            "• Complete mobile games → $5.00+\n"
            "• Social media tasks → $0.50 each\n"
            "• App downloads → $1.00 each\n"
            "• Survey completion → $2.00-$10.00\n\n"
            "🔔 *Stay tuned for:*\n"
            "• Affiliate marketing programs\n"
            "• Cashback shopping rewards\n"
            "• Crypto staking bonuses\n"
            "*More ways to earn = more money in your pocket!*"
        )
        await update.message.reply_text(
            response,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} viewed extra opportunities")
    
    # Handle direct /start in text
    elif '/start' in text.lower():
        await start(update, context)
    
    # Handle unknown messages
    else:
        unknown_msg = (
            "❓ *I didn't understand that command.*\n\n"
            "💡 *Please use the buttons below or type /start*\n"
            "👇 *Tap any button to continue earning!*"
        )
        await update.message.reply_text(
            unknown_msg,
            reply_markup=get_main_keyboard(),
            parse_mode='Markdown'
        )
        logger.info(f"User {user_id} sent unknown message: {text}")

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors from updates."""
    logger.error(f"Update {update} caused error: {context.error}")

def main() -> None:
    """Run the bot."""
    # Get token from environment
    token = os.getenv('TELEGRAM_TOKEN')
    
    if not token:
        logger.error("❌ TELEGRAM_TOKEN environment variable is missing!")
        logger.error("Set it in Render Dashboard > Environment > Add Variable")
        logger.error("Key: TELEGRAM_TOKEN | Value: YourBotTokenFromBotFather")
        return
    
    logger.info("🚀 Starting Money Making Bot...")
    logger.info(f"🤖 Token loaded: {token[:20]}...")
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("✅ Bot started successfully! Polling for updates...")
    application.run_polling(
        poll_interval=1.0,
        timeout=10,
        bootstrap_retries=5
    )

if __name__ == '__main__':
    main()
