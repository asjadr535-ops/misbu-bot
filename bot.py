import os, g4f, asyncio, re, sys, random, threading, http.server, socketserver
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 OWNER CONFIG (Asjad742) ---
TOKEN = "8285517053:AAFS8GAtxcWr0oe2hUpXaAL2uVGbRsEG9lo" 
OWNER_ID = 8536075730 
OWNER_HANDLE = "@Asjad742"

# --- 🌐 RENDER FREE FIX (Port Handling) ---
def run_fake_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# --- 🧠 DATABASE ---
DB = {
    "users": {}, "premium": set(), 
    "buttons": {
        "🌀 Aatma": "Multi-Bot Soul Mode Active!",
        "📚 Student Zone": "Pro-Level Study & Mentor Mode.",
        "🛠️ Extra Features": "Voice, PDF, Image, GIF Tools.",
        "🌸 Talk to Misbu": "Mood: Sweet Teenage Girl ✨"
    }
}

# --- 🎭 (7) MISBU PERSONALITY ---
async def misbu_ai(text):
    prompt = f"Act as Misbu, a shy, sweet, and attractive teenage girl. Use emojis, talk like a best friend to @Asjad742: {text}"
    return await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": prompt}])

# --- 🚀 MASTER UI (Points 1, 2, 3, 7) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if str(u_id) not in DB["users"]: DB["users"][str(u_id)] = {"status": "Free"}
    
    kb = []
    for name in DB["buttons"]:
        kb.append([InlineKeyboardButton(name, callback_data=f"feat_{name}")])
    
    if u_id == OWNER_ID:
        kb.append([InlineKeyboardButton("🔱 DEVELOPER CONTROL", callback_data="dev_menu")])
        kb.append([InlineKeyboardButton("➕ ADD NEW BUTTON", callback_data="add_btn")])

    msg = f"Pranam Maalik {OWNER_HANDLE}! 🔱" if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🛡️ DEVELOPER & TRACKING (Points 4, 5, 6, 10) ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    u_id = query.from_user.id
    await query.answer()

    if query.data == "dev_menu" and u_id == OWNER_ID:
        stats = f"📊 Users: {len(DB['users'])}\n🛠️ Commands: `Broadcast:msg`, `AddBtn:name:msg`, `Clone:username`"
        await query.message.reply_text(stats)
    elif query.data.startswith("feat_"):
        btn_name = query.data.split("_")[1]
        await query.message.reply_text(DB["buttons"].get(btn_name, "Processing..."))

# --- 🤖 SMART ENGINE (AI + Suggestions + Auto-Fix) ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    # Admin: Broadcast & Button Add (Point 5)
    if u_id == OWNER_ID:
        if text.startswith("Broadcast:"):
            msg = text.replace("Broadcast:", "")
            for uid in DB["users"]:
                try: await context.bot.send_message(chat_id=int(uid), text=f"📢 {msg}")
                except: continue
            return await update.message.reply_text("✅ Sent!")
        if text.startswith("AddBtn:"):
            _, n, m = text.split(":")
            DB["buttons"][n] = m
            return await update.message.reply_text(f"✅ Button '{n}' Added!")

    # (9) Suggestion System
    if text.lower().startswith("suggestion:"):
        await context.bot.send_message(OWNER_ID, f"📩 Suggestion from {u_id}: {text}")
        return await update.message.reply_text("✅ Maalik ko bhej diya!")

    # Misbu AI Chat (Point 7)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    response = await misbu_ai(text)
    await update.message.reply_text(response)

def main():
    # Render Port Fix Start
    threading.Thread(target=run_fake_server, daemon=True).start()
    
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
        
        # Conflict Fix
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        # (8) Self-Healing / Auto-Restart
        os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__': main()
    
