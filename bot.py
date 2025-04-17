from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext
import json
from config import BOT_TOKEN, ADMIN_ID
from database import init_db, add_user, get_points

init_db()

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    ref = None
    if context.args:
        try:
            ref = int(context.args[0])
        except:
            pass
    add_user(user.id, user.username or "unknown", ref)
    update.message.reply_text(
        f"👋 Welcome to Gcoin, {user.first_name}!
You have {get_points(user.id)} Gcoins.\n\nUse /tasks, /ads, /quiz, /wallet"
    )

def tasks(update: Update, context: CallbackContext):
    with open("tasks.json") as f:
        tasks = json.load(f)
    msg = "📋 Gcoin Tasks:\n"
    for t in tasks:
        msg += f"- [{t['name']}]({t['url']})\n"
    update.message.reply_text(msg, parse_mode="Markdown")

def ads(update: Update, context: CallbackContext):
    with open("ads.json") as f:
        ads = json.load(f)
    keyboard = [
        [InlineKeyboardButton(ad["title"], url=ad["url"])] for ad in ads
    ]
    update.message.reply_text("🧲 Click Ads to Earn Gcoins:", reply_markup=InlineKeyboardMarkup(keyboard))

def wallet(update: Update, context: CallbackContext):
    points = get_points(update.effective_user.id)
    update.message.reply_text(f"💼 You have {points} Gcoins.")

def quiz(update: Update, context: CallbackContext):
    update.message.reply_poll(
        "🧠 What is the capital of France?",
        ["Berlin", "Paris", "Rome"],
        type='quiz',
        correct_option_id=1,
        explanation="Correct answer: Paris",
        is_anonymous=False
    )

updater = Updater(BOT_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("spin", spin))
import random  # Add at the top

def spin(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    reward = random.choice([0, 5, 10, 15, 20, 25, 50])  # Reward options
    update.message.reply_text(f"🎰 Spinning the Gcoin Wheel... 🎉\nYou won {reward} Gcoins!")
    
    if reward > 0:
        from database import add_points  # You'll create this next
        add_points(user_id, reward)

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("tasks", tasks))
dp.add_handler(CommandHandler("ads", ads))
dp.add_handler(CommandHandler("wallet", wallet))
dp.add_handler(CommandHandler("quiz", quiz))
dp.add_handler(CommandHandler("daily", daily))
def daily(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    from database import can_claim_daily, update_claim_time, add_points

    if can_claim_daily(user_id):
        reward = random.randint(10, 30)
        add_points(user_id, reward)
        update_claim_time(user_id)
        update.message.reply_text(f"🎁 You claimed your daily reward of {reward} Gcoins!")
    else:
        update.message.reply_text("⏳ You've already claimed your daily bonus. Try again in 24 hours!")


print("Gcoin Bot is running...")
updater.start_polling()
updater.idle()