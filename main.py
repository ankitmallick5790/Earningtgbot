import logging
import os
import time
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TOKEN:
    logger.error("❌ TELEGRAM_TOKEN environment variable is required!")
    exit(1)

bot = TeleBot(TOKEN)

# Create main keyboard with 5 buttons
def create_main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.row(KeyboardButton('📺 Watch Ads'), KeyboardButton('💰 Balance'))
    markup.row(KeyboardButton('👥 Refer & Earn'), KeyboardButton('🎁 Bonus'))
    markup.row(KeyboardButton('⚡ Extra'))
    return markup

# /start command handler
@bot.message_handler(commands=['start'])
def start_message(message):
    user = message.from_user
    welcome_text = (
        f"🎉 Welcome {user.first_name} to Money Making Bot! 🎉\n\n"
        "💰 *Earn Real Money Easily:*\n\n"
        "• 📺 Watch ads (15-30s) → $0.10-$0.50 each\n"
        "• 👥 Refer friends → $1.00 bonus each\n"
        "• 🎁 Daily login → $0.10 free\n"
        "• ⚡ Extra tasks → $2.00-$10.00\n"
        "• 💰 Track your balance anytime\n\n"
        "💸 *Minimum withdrawal: $5.00*\n"
        "💳 *Payments: PayPal, Crypto, Bank*\n\n"
        "👇 Tap any button below to start earning!"
    )
    
    bot.reply_to(message, welcome_text, reply_markup=create_main_keyboard(), parse_mode='Markdown')
    logger.info(f"User {user.id} ({user.first_name}) started the bot")

# Handle button clicks and text messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text
    
    # Watch Ads button
    if text == '📺 Watch Ads':
        response = (
            "📺 *Watch Ads to Earn Instantly!*\n\n"
            "💸 *Earnings:* $0.10 - $0.50 per ad\n"
            "⏱️ *Duration:* 15-30 seconds\n"
            "⚡ *Payout:* Instant to balance\n\n"
            "🔗 *Ready to watch? Click here:*\n"
            "[START EARNING FROM ADS](https://example.com/ads)\n\n"
            "📊 *Today's ad earnings: $0.00*\n"
            "*Pro tip: Watch 5+ ads daily for 20% bonus!*"
        )
        bot.reply_to(message, response, reply_markup=create_main_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} clicked Watch Ads")
    
    # Balance button
    elif text == '💰 Balance':
        response = (
            "💰 *Your Account Dashboard*\n\n"
            "💵 *Total Lifetime Earnings:* $0.00\n"
            "💎 *Available for Withdrawal:* $0.00\n"
            "⏳ *Pending Earnings:* $0.00\n"
            "👥 *Referral Earnings:* $0.00\n\n"
            "🎯 *Withdrawal Goal:* $5.00\n"
            "📈 *Progress:* 0% ($0.00 / $5.00)\n\n"
            "💳 *Payment Options:*\n"
            "• PayPal (instant)\n"
            "• Bitcoin (24h)\n"
            "• Bank Transfer (3-5 days)\n\n"
            "*Keep earning to unlock instant withdrawals!*"
        )
        bot.reply_to(message, response, reply_markup=create_main_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} checked balance")
    
    # Refer & Earn button
    elif text == '👥 Refer & Earn':
        # Replace 'YOUR_BOT_USERNAME' with your actual bot username (without @ or 'bot')
        bot_username = "MoneyMakerBot"  # CHANGE THIS to your bot's username!
        referral_link = f"https://t.me/{bot_username}?start=ref_{user_id}"
        
        response = (
            "👥 *Refer Friends & Get Paid!*\n\n"
            f"🔗 *Your Personal Referral Link:*\n"
            f"`{referral_link}`\n\n"
            "💰 *How You Earn:*\n"
            "• $1.00 cash per signup\n"
            "• 30% of friends' ad earnings\n"
            "• $5 bonus for 10 referrals\n"
            "• $25 bonus for 50 referrals\n"
            "• $100 bonus for 100 referrals\n\n"
            "📊 *Your Stats:*\n"
            "• Total Referrals: 0\n"
            "• Active Referrals: 0\n"
            "• Referral Income: $0.00\n\n"
            "📱 *Share on WhatsApp, Discord, Instagram, Twitter*\n"
            "*Unlimited earnings - no limits on referrals!*"
        )
        bot.reply_to(message, response, reply_markup=create_main_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} viewed referral system")
    
    # Bonus button
    elif text == '🎁 Bonus':
        response = (
            "🎁 *Daily Login Bonus Claimed!*\n\n"
            "✨ *Congratulations!*\n"
            "✅ *$0.10 added to your balance!*\n"
            "💰 *New total: $0.10*\n\n"
            "🎯 *Bonus Levels:*\n"
            "• Daily Login: $0.10\n"
            "• 3-Day Streak: $0.30 bonus\n"
            "• 7-Day Streak: $1.00 bonus\n"
            "• Weekend Special: $0.25 extra\n\n"
            "⏰ *Next bonus:* Tomorrow at 00:00\n"
            "*Never miss a day - streaks multiply your earnings!*"
        )
        bot.reply_to(message, response, reply_markup=create_main_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} claimed daily bonus")
    
    # Extra button
    elif text == '⚡ Extra':
        response = (
            "⚡ *Premium Earning Opportunities*\n\n"
            "🔥 *VIP Membership* ($9.99/month):\n"
            "• 2x higher ad payouts\n"
            "• Priority instant withdrawals\n"
            "• Exclusive high-value ads\n"
            "• Personal earnings manager\n"
            "• Weekend cash tournaments\n\n"
            "🎮 *Task & Game Rewards:*\n"
            "• Mobile games → $5.00+ per completion\n"
            "• App downloads → $1.00 each\n"
            "• Social tasks → $0.50 per action\n"
            "• Paid surveys → $2.00-$10.00\n"
            "• Video challenges → $3.00 bonus\n\n"
            "🔔 *Coming Soon:*\n"
            "• Affiliate programs (10% commission)\n"
            "• Cashback shopping (5% back)\n"
            "• Crypto staking rewards\n"
            "*Unlimited earning potential - join VIP for max profits!*"
        )
        bot.reply_to(message, response, reply_markup=create_main_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} viewed extra opportunities")
    
    # Handle direct /start in regular text
    elif text.lower() == '/start':
        start_message(message)
    
    # Unknown commands or text
    else:
        unknown_response = (
            "❓ *Sorry, I didn't understand that.*\n\n"
            "💡 *Please use the buttons below or type /start*\n"
            "👇 *Tap any button to continue earning money!*"
        )
        bot.reply_to(message, unknown_response, reply_markup=create_main_keyboard(), parse_mode='Markdown')
        logger.info(f"User {user_id} sent unknown message: {text}")

# Error handler for polling
def handle_polling_errors():
    """Handle polling errors gracefully."""
    while True:
        try:
            logger.info("🚀 Starting Money Making Bot...")
            logger.info(f"🤖 Bot initialized with token: {TOKEN[:20]}...")
            
            # Start polling with error handling
            bot.infinity_polling(timeout=10, long_polling_timeout=5)
            
        except Exception as e:
            logger.error(f"❌ Bot polling error: {e}")
            logger.info("⏳ Restarting in 10 seconds...")
            time.sleep(10)

if __name__ == '__main__':
    handle_polling_errors()
