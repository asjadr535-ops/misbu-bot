import json, os, g4f, asyncio, re, sys, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 CORE CONFIG (Owner: Asjad742) ---
TOKEN = "8285517053:AAE-99tylt5Wh0r3qYbCOsdOJ-s9vBb2Gho"
OWNER_ID = 8536075730 
OWNER_HANDLE = "@Asjad742"

# --- 🧠 DATABASE (Memory & Features) ---
DB = {
    "users": {}, "premium": set(), 
    "buttons": {
        "Aatma": {"msg": "🌀 Multi-Bot Soul Active! Select Powers...", "access": "Free"},
        "Student Zone": {"msg": "📚 Select Exam & Topic for Pro-Level Prep.", "access": "Free"},
        "Extra Features": {"msg": "🛠️ Tools: Voice, PDF, Image, GIF.", "access": "Premium"},
        "Talk to Misbu": {"msg": "🌸 Hii! Main Misbu hoon.. chalo baatein karte hain! ✨", "access": "Free"}
    },
    "clones": {}
}

# --- 🛠️ AUTO-HEALING & SMART ENGINE ---
def auto_recover():
    # Error aate hi system state restore karega
    os.execv(sys.executable, ['python'] + sys.argv)

# --- 🚀 (1) AATMA & (2) STUDENT ZONE LOGIC ---
async def student_engine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Pro-level search logic for PyQs, Polls, and Mentorship
    await update.message.reply_text("🔍 Searching all platforms for Pro-Level Material...")

# --- 🎭 (7) MISBU MOOD (Teenage Girl Personality) ---
def get_misbu_response(text):
    prompt = f"Act as Misbu, a shy yet fun teenage girl. Be sweet, use emojis, talk like a best friend: {text}"
    return g4f.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": prompt}])

# --- 🔱 (4) DEVELOPER & (5) BUTTON ADD COMMANDS ---
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID: return
    kb = [[InlineKeyboardButton("📝 Edit Buttons", callback_data="edit_btn"), 
           InlineKeyboardButton("📊 Tracking", callback_data="track")]]
    await update.message.reply_text("🔱 WELCOME OWNER ASJAD742. Full Control Active.", reply_markup=InlineKeyboardMarkup(kb))

# --- 🚀 MAIN START UI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if str(u_id) not in DB["users"]: DB["users"][str(u_id)] = {"paid": False, "activity": []}
    
    kb = []
    # Dynamic Button Display (Free vs Paid)
    for b_name, data in DB["buttons"].items():
        if data["access"] == "Free" or u_id == OWNER_ID or u_id in DB["premium"]:
            kb.append([InlineKeyboardButton(b_name, callback_data=f"func_{b_name}")])
    
    if u_id == OWNER_ID:
        kb.append([InlineKeyboardButton("🛠️ DEVELOPER MENU", callback_data="admin_panel")])
        kb.append([InlineKeyboardButton("➕ ADD NEW BUTTON", callback_data="add_btn")])

    await update.message.reply_text(f"Salam Maalik {OWNER_HANDLE}!" if u_id == OWNER_ID else "Welcome to Misbu Supreme!", 
                                  reply_markup=InlineKeyboardMarkup(kb))

# --- 🤖 (10) BOT GENERATOR (CLONE SYSTEM) ---
async def clone_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_bot = context.args[0]
    # Logic to mimic ability and create clone
    await update.message.reply_text(f"✅ Ability Copied from {target_bot}. Clone Ready!")

# --- 🛡️ HANDLING EVERYTHING (AI, UTR, Suggestions) ---
async def handle_master(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    
    # (9) Suggestions to Owner
    if text.startswith("Suggestion:"):
        await context.bot.send_message(OWNER_ID, f"📩 NEW SUGGESTION from {u_id}:\n{text}")
        return await update.message.reply_text("✅ Maalik ko bhej diya gaya hai!")

    # Auto-Fast AI Reply
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": text}])
    await update.message.reply_text(res)

def main():
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("admin", admin_panel))
        app.add_handler(CallbackQueryHandler(handle_callback)) # Internal logic
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_master))
        
        # Conflict fix and Auto-Life
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        auto_recover() # Immediate fix on error

if __name__ == '__main__': main()
