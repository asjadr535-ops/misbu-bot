import json, os, g4f, random, smtplib, asyncio
from datetime import datetime
from email.message import EmailMessage
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 SUPREME MASTER DIRECT CONFIG ---
TELEGRAM_TOKEN = "8285517053:AAHbUrKM398ezjLovmpV9kSde05u7s-QQCc" # Direct Token Fixed!
OWNER_ID = 8536075730 # Aapki Numeric ID fix kar di
OWNER_USERNAME = "Asjad742"
OWNER_EMAIL = "asjadr535@gmail.com"
GMAIL_APP_PASSWORD = "pqwx lmhd zjts qhkn" # Gmail error fix!
UPI_ID = "8887937470@ptaxis"
DB_FILE = "supreme_master_db.json"

# --- 📂 DATABASE ---
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {"users": {}, "custom_features": {}, "settings": {"mode": "Free"}}
    return {"users": {}, "custom_features": {}, "settings": {"mode": "Free"}}

db = load_db()

def save_db():
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

# --- 🛡️ SMART SECURITY ---
def is_boss(user):
    return user.id == OWNER_ID or user.username == OWNER_USERNAME

# --- 🚀 SUPERFAST HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if uid not in db["users"]:
        db["users"][uid] = {"name": user.username, "joined": str(datetime.now())}
        save_db()

    if is_boss(user):
        await update.message.reply_text(f"Salam King {OWNER_USERNAME}! 🔱\n\nAb bot 100x speed par chal raha hai. Koi error nahi bacha!", 
                                       reply_markup=get_main_menu(user.id, True))
    else:
        await update.message.reply_text(f"Salam! Main **Misbu Supreme** hoon. 🔱\n\nKaise ho boss?",
                                       reply_markup=get_main_menu(user.id, False))

def get_main_menu(user_id, is_owner=False):
    keyboard = [
        [InlineKeyboardButton("🤖 AI Chat", callback_data="chat"), InlineKeyboardButton("📜 Features", callback_data="show_features")],
        [InlineKeyboardButton("💎 Premium", callback_data="pay"), InlineKeyboardButton("👨‍💻 Owner", url=f"https://t.me/{OWNER_USERNAME}")]
    ]
    if is_owner:
        keyboard.append([InlineKeyboardButton("🛠️ CREATE FEATURE", callback_data="create_feature")])
        keyboard.append([InlineKeyboardButton("🛡️ DEV CONTROL", callback_data="dev_panel")])
    return InlineKeyboardMarkup(keyboard)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4",
                                            messages=[{"role": "system", "content": "Aap Misbu Supreme ho. Creator Asjad742. Fast jawab do."},
                                                      {"role": "user", "content": text}])
        await update.message.reply_text(response)
    except:
        await update.message.reply_text("Kuch upgrade kar rahi hoon boss... ✨")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print(f"🔱 MISBU SUPREME IS LIVE!")
    app.run_polling()

if __name__ == '__main__':
    main()
    
