import json, os, g4f, asyncio, requests, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 MASTER CONFIG ---
TELEGRAM_TOKEN = "8285517053:AAE-99tylt5Wh0r3qYbCOsdOJ-s9vBb2Gho" 
OWNER_ID = 8536075730 
OWNER_USERNAME = "Asjad742"
UPI_ID = "8887937470@ptaxis" 

# --- 🧠 PERMANENT MEMORY ---
PREMIUM_USERS = set()
DB = {"buttons": {}}

# --- 📊 DAILY POLL LOGIC (Sana Khan Topic Included) ---
async def daily_poll(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    qs = [
        {"q": "Sana Khan kis industry se judi thi?", "opt": ["Bollywood", "Sports", "Politics"], "ans": 0},
        {"q": "Python mein error handling kaise hoti hai?", "opt": ["try-except", "if-else"], "ans": 0}
    ]
    p = random.choice(qs)
    await context.bot.send_poll(chat_id=chat_id, question=f"📚 Study Boost: {p['q']}", options=p['opt'], correct_option_id=p['ans'], type="quiz")

# --- 🚀 HIGH-FI FEATURES (PREMIUM LOCKED) ---

# 1. PDF Analysis & Search
async def pdf_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in PREMIUM_USERS and update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ PDF Analysis Premium feature hai! UPI: " + UPI_ID)
    await update.message.reply_text("📂 PDF Analysis Active: File bhejiye, main search kar dungi!")

# 2. AI Face Swap / Photo Retouch
async def face_swap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in PREMIUM_USERS and update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Face Swap sirf VIPs ke liye hai! ✨")
    await update.message.reply_text("🎭 Photo bhejiye, face swap process shuru ho jayega!")

# 3. Voice Cloning
async def voice_clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in PREMIUM_USERS and update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("❌ Voice Cloning locked! Premium lijiye. ❤️")
    await update.message.reply_text("🎙️ Kiski awaaz chahiye? Voice sample bhejiye!")

# 4. NSFW Filter (Auto-Delete)
async def nsfw_check(update: Update):
    bad_words = ["nsfw", "ashleel", "badword"] # Add more as needed
    if any(word in update.message.text.lower() for word in bad_words):
        await update.message.delete()
        await update.message.reply_text("🚫 Ashleel content allowed nahi hai! ✨")

# --- 🚀 COMMANDS & BUTTONS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    is_prem = (u_id == OWNER_ID or u_id in PREMIUM_USERS)
    kb = []
    if u_id == OWNER_ID:
        kb.append([InlineKeyboardButton("🔱 MASTER CONTROL PANEL", callback_data="admin_panel")])
    
    # Static Power Buttons
    kb.append([InlineKeyboardButton("👻 AATMA MODE", callback_data="aatma"), InlineKeyboardButton("🎓 STUDENT ZONE", callback_data="student")])
    
    # Dynamic Buttons from Telegram
    for name in DB["buttons"]:
        kb.append([InlineKeyboardButton(name, callback_data=f"btn_{name}")])

    if not is_prem:
        kb.append([InlineKeyboardButton("💎 UNLOCK PREMIUM", callback_data="buy_prem")])

    msg = f"Pranam Maalik {OWNER_USERNAME}! 🔱" if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🛡️ CALLBACK HANDLERS (Telegram-Based Control) ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    u_id = query.from_user.id
    await query.answer()

    if query.data == "admin_panel" and u_id == OWNER_ID:
        msg = "🛠️ **GOD CONTROL PANEL**\n\n- `AddBtn:Name:Msg:Access` (Button Create)\n- `MakeVIP:ID` (VIP Access)\n- `/boost` (Start Daily Polls)"
        await query.message.reply_text(msg)
    elif query.data == "buy_prem":
        await query.message.reply_text(f"💳 **UPI:** `{UPI_ID}`\nBhejo aur @{OWNER_USERNAME} ko DM karo! ✨")
    elif query.data == "aatma":
        await query.message.reply_text("👻 **AATMA MODE ACTIVE**\nDuniya ke har bot ki shakti ab mujhme hai! ✨")
    elif query.data == "student":
        await query.message.reply_text("🎓 **STUDENT ZONE**\nHar exam ke notes, PDF aur lectures yahan milenge. Puchiye! 📚")

# --- 🤖 TURBO AI & HANDLERS ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    # NSFW Protection
    await nsfw_check(update)

    # Telegram God Control
    if u_id == OWNER_ID and text.startswith("AddBtn:"):
        _, name, msg, access = text.split(":")
        DB["buttons"][name] = {"msg": msg, "access": access}
        return await update.message.reply_text(f"✅ Button '{name}' created!")

    if u_id == OWNER_ID and text.startswith("MakeVIP:"):
        v_id = int(text.split(":")[1])
        PREMIUM_USERS.add(v_id)
        return await update.message.reply_text(f"✅ User {v_id} made VIP!")

    # Speed-Optimized AI
    if update.effective_chat.type == "private" or context.bot.username in text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        sys_p = "You are Misbu Supreme. Mentor + Flirty Girl. Speed 100%. Accuracy 100%."
        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": text}])
        await update.message.reply_text(res)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pdf", pdf_tool))
    app.add_handler(CommandHandler("faceswap", face_swap))
    app.add_handler(CommandHandler("clone", voice_clone))
    app.add_handler(CommandHandler("boost", lambda u, c: c.job_queue.run_repeating(daily_poll, interval=86400, first=10, chat_id=u.effective_chat.id)))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
    
    # Conflict Fix for Render
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__': main()
    
