import os, g4f, asyncio, sys, threading, http.server, socketserver, random, json, time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 OWNER IDENTIFICATION (Point 8) ---
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8285517053:AAE3UQdQ96I9nCcY5Xx5j6C5LJMERbTlTwo")
OWNER_ID = 8536075730 
OWNER_HANDLE = "@Asjad742"

# --- 🌐 RENDER PORT BINDING (Fixes Port Error) ---
def run_fake_server():
    port = int(os.environ.get("PORT", 8080))
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

# --- 🧠 SUPREME DATABASE (Points 1-10) ---
DB = {
    "users": {}, "premium": set(),
    "buttons": {
        "🌀 Aatma": "Soul Mode: Multiple bot powers (Student/Admin) active! Select souls...",
        "📚 Student Zone": "Pro-Level Prep: PYQs, Polls, PDFs & Mentor Mode active.",
        "🛠️ Extra Features": "Tools: Multi-lang V2T/T2V, PDF Analyser, AI Image/GIF Generator.",
        "🌸 Talk to Misbu": "Misbu Mode: Sweet & Attractive Teenage Bestie ✨"
    }
}

# --- 🎭 (7) MISBU AI PERSONALITY ---
async def misbu_ai(text, mode="normal"):
    prompt = f"Act as Misbu, a sweet teenage girl, best friend of @Asjad742. Be attractive, shy & fast. Point 7: {text}"
    if mode == "detail": prompt += " Elaborate in detail."
    try:
        return await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": prompt}])
    except Exception: return "🌸 Ohho! Kuch repair kar rahi hoon.. par main hamesha aapki hoon! ✨"

# --- 🚀 MASTER INTERFACE ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if str(u_id) not in DB["users"]: DB["users"][str(u_id)] = {"status": "Free"}
    
    kb = [[InlineKeyboardButton(n, callback_data=f"feat_{n}")] for n in DB["buttons"]]
    kb.append([InlineKeyboardButton("📩 Suggestion", callback_data="feat_Suggestion")])
    
    if u_id == OWNER_ID:
        kb.extend([
            [InlineKeyboardButton("🔱 DEVELOPER CONTROL", callback_data="dev")],
            [InlineKeyboardButton("🤖 BOT GENERATOR", callback_data="bot_gen")],
            [InlineKeyboardButton("📊 TRACKING", callback_data="track")]
        ])

    msg = f"Pranam Maalik {OWNER_HANDLE}! 🔱 Sabhi systems active hain." if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🤖 (5, 8, 10) SMART ENGINE ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    # Point 9: Direct Suggestion
    if text.lower().startswith("suggestion:"):
        await context.bot.send_message(OWNER_ID, f"📩 From {u_id}: {text}")
        return await update.message.reply_text("✅ Maalik ko bhej diya!")

    # Admin Powers (Point 5)
    if u_id == OWNER_ID:
        if text.startswith("AddBtn:"):
            _, n, m = text.split(":")
            DB["buttons"][n] = m
            return await update.message.reply_text(f"✅ Naya Button '{n}' added!")
        if text.startswith("Broadcast:"):
            for uid in DB["users"]:
                try: await context.bot.send_message(chat_id=int(uid), text=text.replace("Broadcast:", "📢 "))
                except: continue
            return await update.message.reply_text("✅ Sent to all!")

    # Speed & AI (Point 8)
    mode = "detail" if "detail" in text.lower() else "normal"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    response = await misbu_ai(text, mode)
    await update.message.reply_text(response)

# --- 🔱 CORE REPAIR ENGINE (Point 8) ---
def main():
    threading.Thread(target=run_fake_server, daemon=True).start()
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_everything)) # Simplified for speed
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        os.execv(sys.executable, ['python'] + sys.argv) # Auto-Fix

if __name__ == '__main__': main()
        
