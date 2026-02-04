import os, asyncio, sys, threading, http.server, socketserver, random, json, time, subprocess

# --- 🔱 SELF-INSTALLER (Fixes 'ModuleNotFoundError' automatically) ---
def install_requirements():
    try:
        import g4f, telegram, typing_extensions
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot[job-queue]", "g4f", "typing-extensions", "requests", "nest-asyncio"])

install_requirements()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 OWNER CONFIG ---
# Tip: Token ko hamesha Render Dashboard mein set karein, yahan nahi
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8285517053:AAE3UQdQ96I9nCcY5Xx5j6C5LJMERbTlTwo")
OWNER_ID = 8536075730 
OWNER_HANDLE = "@Asjad742"

# --- 🌐 RENDER PORT & CRON-JOB FIX (For 100% Success) ---
def run_fake_server():
    port = int(os.environ.get("PORT", 8080))
    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Cron-job ko ye message milega toh wo SUCCESS dikhayega
            self.wfile.write(b"Misbu is Alive and Superfast! 🚀")

    try:
        with socketserver.TCPServer(("", port), MyHandler) as httpd:
            print(f"🔱 Server started on port {port}")
            httpd.serve_forever()
    except Exception as e:
        print(f"⚠️ Server error: {e}")

# --- 🧠 SUPREME DATABASE ---
DB = {
    "users": {}, "premium": set(),
    "buttons": {
        "🌀 Aatma": "Soul Mode: Sabhi bots ki power ek saath! Multiple selection active.",
        "📚 Student Zone": "Pro Prep: PYQs, Polls, PDFs & Study Mentor Mode (Feelings Chatting) active.",
        "🛠️ Extra Features": "Tools: Multi-lang V2T/T2V, PDF Analyser, Image/GIF/Emoji Generator.",
        "🌸 Talk to Misbu": "Misbu Mode: Sweet & Attractive Teenage Girl ✨ (Full Masti & Sweet Chatting)"
    }
}

# --- 🎭 (7) MISBU PERSONALITY (Language Locked) ---
async def misbu_ai(text, mode="normal"):
    # Strict prompt added to stop Chinese behavior
    prompt = f"System: Strict Rule - Talk ONLY in Hindi/English. Act as Misbu, a shy, sweet, attractive teenage girl. Best friend of {OWNER_HANDLE}. Input: {text}"
    if mode == "detail": prompt += " Give extremely detailed answers."
    try:
        import g4f
        return await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": prompt}])
    except: return "🌸 Aww Maalik, thoda network issue hai.. par main hoon na! ✨"

# --- 🚀 MASTER UI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if str(u_id) not in DB["users"]: DB["users"][str(u_id)] = {"status": "Free"}
    
    kb = [[InlineKeyboardButton(n, callback_data=f"feat_{n}")] for n in DB["buttons"]]
    kb.append([InlineKeyboardButton("📩 Suggestion", callback_data="feat_Suggestion")])
    
    if u_id == OWNER_ID:
        kb.extend([
            [InlineKeyboardButton("🔱 DEVELOPER CONTROL", callback_data="dev_menu")],
            [InlineKeyboardButton("🤖 BOT GENERATOR", callback_data="bot_gen")],
            [InlineKeyboardButton("📊 TRACKING", callback_data="track")]
        ])

    msg = f"Pranam Maalik {OWNER_HANDLE}! 🔱 Sabhi systems 100% zinda hain." if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🛡️ HANDLERS ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    u_id = query.from_user.id
    await query.answer()

    if query.data == "dev_menu" and u_id == OWNER_ID:
        await query.message.reply_text("🔱 Control: `Broadcast:msg`, `AddBtn:name:msg`, `SetPaid:uid`")
    elif query.data == "bot_gen" and u_id == OWNER_ID:
        await query.message.reply_text("🤖 Username likhein clone banane ke liye (Point 10):")
    elif query.data.startswith("feat_"):
        btn = query.data.split("_")[1]
        await query.message.reply_text(DB["buttons"].get(btn, "Processing with 100% Speed..."))

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    if text.lower().startswith("suggestion:"):
        await context.bot.send_message(OWNER_ID, f"📩 Suggestion: {text}")
        return await update.message.reply_text("✅ Maalik ko bhej diya!")

    if u_id == OWNER_ID and text.startswith("Broadcast:"):
        msg = text.replace("Broadcast:", "")
        for uid in DB["users"]:
            try: await context.bot.send_message(chat_id=int(uid), text=f"📢 {msg}")
            except: continue
        return await update.message.reply_text("✅ Sent!")

    mode = "detail" if "details" in text.lower() else "normal"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    res = await misbu_ai(text, mode)
    await update.message.reply_text(res)

def main():
    threading.Thread(target=run_fake_server, daemon=True).start()
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
        # drop_pending_updates=True ensures no lag or conflict
        app.run_polling(drop_pending_updates=True, close_loop=False)
    except Exception as e:
        # Self-repair: Restarts the bot on crash
        time.sleep(5)
        os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__': main()
