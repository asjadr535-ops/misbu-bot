import json, os, g4f, random, smtplib, asyncio
from datetime import datetime
from email.message import EmailMessage
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 SUPREME MASTER CONFIG ---
TELEGRAM_TOKEN = "8285517053:AAEoo0PLt8dPqwA6ApdRbk_-vWwD73xGxb4"
OWNER = "Asjad742"
OWNER_EMAIL = "asjadr535@gmail.com"
GMAIL_APP_PASSWORD = "auys rqjj inva xjcq"
UPI_ID = "8887937470@ptaxis"
DB_FILE = "supreme_master_db.json"

# --- 📂 ATOMIC DATABASE LOAD/SAVE ---
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f: return json.load(f)
        except: return {"users": {}, "custom_features": {}, "settings": {"mode": "Free", "allowed_groups": []}}
    return {"users": {}, "custom_features": {}, "settings": {"mode": "Free", "allowed_groups": []}}

db = load_db()
verified_boss = set()
verification_codes = {}

def save_db():
    with open(DB_FILE, "w") as f: json.dump(db, f, indent=4)

# --- 🛡️ GMAIL SECURITY (OTP) ---
def send_otp(code):
    msg = EmailMessage()
    msg.set_content(f"Salam Boss Asjad742! 🔱\n\nAapka Access Code: {code}\n\nIse bot mein enter karein.")
    msg['Subject'] = '🔱 Misbu Supreme Access'
    msg['From'] = OWNER_EMAIL
    msg['To'] = OWNER_EMAIL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(OWNER_EMAIL, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)

# --- 🔘 MASTER BUTTON INTERFACE ---
def get_main_menu(user_id, is_owner=False):
    keyboard = [
        [InlineKeyboardButton("🤖 AI Chat", callback_data="chat"), InlineKeyboardButton("📜 Features", callback_data="show_features")],
        [InlineKeyboardButton("💎 Buy Premium", callback_data="pay"), InlineKeyboardButton("👨‍💻 Owner", url=f"https://t.me/{OWNER}")]
    ]
    for feat in db.get("custom_features", {}):
        keyboard.append([InlineKeyboardButton(f"✨ {feat}", callback_data=f"custom_{feat}")])

    if is_owner:
        keyboard.append([InlineKeyboardButton("🛠️ CREATE FEATURE", callback_data="create_feature")])
        keyboard.append([InlineKeyboardButton("🛡️ DEV CONTROL", callback_data="dev_panel")])

    return InlineKeyboardMarkup(keyboard)

# --- 🚀 SUPERFAST HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = str(user.id)

    if uid not in db["users"]:
        db["users"][uid] = {"name": user.username, "joined": str(datetime.now()), "status": "Free", "last_seen": str(datetime.now())}
        save_db()

    if user.username == OWNER and user.id not in verified_boss:
        code = str(random.randint(111111, 999999))
        verification_codes[user.id] = code
        try:
            send_otp(code)
            await update.message.reply_text("🛡️ **Boss, Security Code Gmail par bhej diya hai!** ✨")
        except:
            await update.message.reply_text("❌ Gmail error! Check App Password.")
        return

    await update.message.reply_text(f"Salam! Main **Misbu Supreme** hoon. 🔱\n\nAb main pehle se 10x Fast aur intelligent hoon! 🚀",
                                   reply_markup=get_main_menu(user.id, user.username == OWNER))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    data = query.data
    await query.answer()

    if data == "dev_panel" and user.username == OWNER:
        kb = [[InlineKeyboardButton("🔓 SET FREE", callback_data="mode_free"), InlineKeyboardButton("🔒 SET PAID", callback_data="mode_paid")],
              [InlineKeyboardButton("📊 Stats", callback_data="stats"), InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")]]
        await query.edit_message_text("🛠️ **Dev Control Center**", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "create_feature" and user.username == OWNER:
        await query.message.reply_text("📝 **Feature Creator**\n\nIs format mein likhein:\n`Feature: Naam, Kaam: Detail` ")
        context.user_data['waiting_feature'] = True

    elif data.startswith("custom_"):
        feat_name = data.split("_")[1]
        await query.message.reply_text(f"🚀 **Running {feat_name}...**")
        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": f"Execute: {db['custom_features'][feat_name]}"}])
        await query.message.reply_text(res)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    if user.username == OWNER and user.id not in verified_boss:
        if text == verification_codes.get(user.id):
            verified_boss.add(user.id)
            await update.message.reply_text("✅ **Hello King!** Ab aap commands ke bina sab buttons se control karein. 🔱")
        return

    if context.user_data.get('waiting_feature') and user.username == OWNER:
        try:
            name = text.split("Feature:")[1].split(",")[0].strip()
            desc = text.split("Kaam:")[1].strip()
            db["custom_features"][name] = desc
            save_db()
            context.user_data['waiting_feature'] = False
            await update.message.reply_text(f"✅ **BINGO!** Feature '{name}' add ho gaya. 🚀")
        except:
            await update.message.reply_text("❌ Format galat hai!")
        return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4",
                                            messages=[{"role": "system", "content": f"Aap Misbu Supreme ho, creator {OWNER}. Superfast jawab do."},
                                                      {"role": "user", "content": text}])
        await update.message.reply_text(response, reply_markup=get_main_menu(user.id, user.username == OWNER))
    except:
        await update.message.reply_text("Evolution in progress... ✨")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print(f"🔱 MISBU SUPREME IS LIVE! Boss: {OWNER}")
    app.run_polling()

if __name__ == '__main__':
    main()
          
