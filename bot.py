import os, asyncio, sys, threading, http.server, socketserver, random, json, time, subprocess

# --- 🔱 SELF-INSTALLER ---
def install_requirements():
    try:
        import g4f, telegram, typing_extensions
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot[job-queue]", "g4f", "typing-extensions", "requests", "nest-asyncio"])

install_requirements()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 OWNER CONFIG ---
TOKEN = os.environ.get("TELEGRAM_TOKEN", "8285517053:AAE3UQdQ96I9nCcY5Xx5j6C5LJMERbTlTwo")
OWNER_ID = 8536075730 
OWNER_HANDLE = "@Asjad742"

# --- 🌐 RENDER SERVER (Emoji Removed to Fix SyntaxError) ---
def run_fake_server():
    port = int(os.environ.get("PORT", 8080))
    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Simple text to avoid 'ASCII literal' error
            self.wfile.write(b"Misbu is Alive and Superfast")

    try:
        with socketserver.TCPServer(("", port), MyHandler) as httpd:
            httpd.serve_forever()
    except:
        pass

# --- 🧠 SUPREME DATABASE ---
DB = {
    "users": {}, "premium": set(),
    "buttons": {
        "🌀 Aatma": "Soul Mode Active",
        "📚 Student Zone": "Study Mentor Mode Active",
        "🛠️ Extra Features": "Tools & Generator Active",
        "🌸 Talk to Misbu": "Sweet Chat Mode Active"
    }
}

# --- 🎭 (7) MISBU PERSONALITY (Strict Hindi/English Only) ---
async def misbu_ai(text, mode="normal"):
    # Fixed Chinese Issue: Added strict rule
    prompt = f"System: Strict Rule - Talk ONLY in Hindi or English. Never use Chinese. You are Misbu, {OWNER_HANDLE}'s best friend. Input: {text}"
    if mode == "detail": prompt += " Give extremely detailed answers."
    try:
        import g4f
        return await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": prompt}])
    except:
        return "🌸 Aww Maalik, thoda network issue hai.. par main hoon na!"

# --- 🚀 MASTER UI ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if str(u_id) not in DB["users"]: DB["users"][str(u_id)] = {"status": "Free"}
    kb = [[InlineKeyboardButton(n, callback_data=f"feat_{n}")] for n in DB["buttons"]]
    msg = f"Pranam Maalik {OWNER_HANDLE}! 🔱 System Live." if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🛡️ HANDLERS ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.startswith("feat_"):
        btn = query.data.split("_")[1]
        await query.message.reply_text(DB["buttons"].get(btn, "Processing..."))

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    mode = "detail" if "details" in update.message.text.lower() else "normal"
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    res = await misbu_ai(update.message.text, mode)
    await update.message.reply_text(res)

def main():
    threading.Thread(target=run_fake_server, daemon=True).start()
    try:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_callback))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
        # drop_pending_updates prevents lag
        app.run_polling(drop_pending_updates=True)
    except Exception:
        # Self-repair logic
        time.sleep(5)
        os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__': main()
        
