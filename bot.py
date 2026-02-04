import json, os, g4f, asyncio, requests, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 MASTER CONFIG ---
TELEGRAM_TOKEN = "8285517053:AAE-99tylt5Wh0r3qYbCOsdOJ-s9vBb2Gho" 
OWNER_ID = 8536075730 
OWNER_USERNAME = "Asjad742"
UPI_ID = "8887937470@ptaxis" #

# --- 🧠 PERMANENT DATABASE (Memory) ---
PREMIUM_USERS = set()
# Dynamic Control: Buttons, Content, and Access
DB = {
    "buttons": {
        "👻 AATMA": {"msg": "Aatma Mode Active! ✨", "access": "PREMIUM"},
        "🎓 STUDENT": {"msg": "Student Zone: Puchiye apna sawaal! 📚", "access": "FREE"}
    },
    "auto_approve": True
}

# --- 📊 AUTO-QUIZ SYSTEM ---
async def auto_poll(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    questions = [
        {"q": "India ki capital?", "opt": ["Delhi", "Mumbai"], "ans": 0},
        {"q": "Sana Khan topic yaad hai?", "opt": ["Haan", "Nahi"], "ans": 0} #
    ]
    p = random.choice(questions)
    await context.bot.send_poll(chat_id=chat_id, question=f"📚 Quiz: {p['q']}", options=p['opt'], correct_option_id=p['ans'], type="quiz")

# --- 🚀 COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    is_prem = (u_id == OWNER_ID or u_id in PREMIUM_USERS)
    
    kb = []
    # 1. Admin Control Button (Sirf aapko dikhega)
    if u_id == OWNER_ID:
        kb.append([InlineKeyboardButton("🔱 MASTER CONTROL PANEL", callback_data="admin_panel")])
    
    # 2. Dynamic Buttons (Jo aap Telegram se banayenge)
    for name, data in DB["buttons"].items():
        if data['access'] == "FREE" or (data['access'] == "PREMIUM" and is_prem):
            kb.append([InlineKeyboardButton(name, callback_data=f"btn_{name}")])

    # 3. Payment Button (Sirf normal users ke liye)
    if not is_prem:
        kb.append([InlineKeyboardButton("💎 UNLOCK PREMIUM", callback_data="buy_prem")])

    msg = f"Pranam King {OWNER_USERNAME}! 🔱" if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🛡️ TELEGRAM BUTTON CONTROL (God Access) ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    u_id = query.from_user.id
    await query.answer()

    if query.data == "admin_panel" and u_id == OWNER_ID:
        kb = [
            [InlineKeyboardButton("➕ Add Button", callback_data="add_btn"), InlineKeyboardButton("🗑️ Del Button", callback_data="rem_btn")],
            [InlineKeyboardButton("💎 Add VIP User", callback_data="add_vip"), InlineKeyboardButton("📢 Broadcast", callback_data="bc")],
            [InlineKeyboardButton("⚡ Speed Boost", callback_data="speed")]
        ]
        await query.message.reply_text("🛠️ **GOD-CONTROL PANEL**\n\nMaalik, kya badalna hai?", reply_markup=InlineKeyboardMarkup(kb))
    
    elif query.data == "buy_prem":
        await query.message.reply_text(f"💳 **Payment UPI:** `{UPI_ID}`\n\nScreenshot bhejo, main turant activate kar dungi! ✨")
    
    elif query.data.startswith("btn_"):
        btn_name = query.data.split("_")[1]
        await query.message.reply_text(DB["buttons"][btn_name]["msg"])

# --- 🤖 ZERO-CODE FEATURE INJECTOR ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    # 1. Telegram se Button Banana: `AddBtn:Naam:Message:FREE/PREMIUM`
    if u_id == OWNER_ID and text.startswith("AddBtn:"):
        _, name, msg, access = text.split(":")
        DB["buttons"][name] = {"msg": msg, "access": access}
        return await update.message.reply_text(f"✅ Button '{name}' taiyar hai!")

    # 2. Telegram se VIP banana: `MakeVIP:UserID`
    if u_id == OWNER_ID and text.startswith("MakeVIP:"):
        v_id = int(text.split(":")[1])
        PREMIUM_USERS.add(v_id)
        return await update.message.reply_text(f"✅ User {v_id} ab Premium hai!")

    # 3. Turbo AI Chat (100x Speed)
    if update.effective_chat.type == "private" or context.bot.username in text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        sys_p = "You are Misbu Supreme. Fast, flirty, and a master teacher. Solve everything instantly."
        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": text}])
        await update.message.reply_text(res)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
    
    # Conflict aur Slowness fix
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__': main()
    
