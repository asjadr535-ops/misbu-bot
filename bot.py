import json, os, g4f, asyncio, requests, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 CONFIG (MASTER SETTINGS) ---
TELEGRAM_TOKEN = "8285517053:AAE-99tylt5Wh0r3qYbCOsdOJ-s9vBb2Gho" #
OWNER_ID = 8536075730 #
OWNER_USERNAME = "Asjad742"
UPI_ID = "8887937470@ptaxis" #
PREMIUM_USERS = set()

# --- 📊 DAILY POLL LOGIC (Study Boost) ---
async def send_daily_poll(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    questions = [
        {"q": "India ki financial capital kaunsi hai?", "opt": ["Delhi", "Mumbai", "Chennai", "Kolkata"], "ans": 1},
        {"q": "Python mein 'print' kya hai?", "opt": ["Variable", "Function", "Keyword", "Data Type"], "ans": 1},
        {"q": "Sana Khan kis industry se judi thi?", "opt": ["Sports", "Bollywood", "Politics", "Music"], "ans": 1} # [Personalized]
    ]
    p = random.choice(questions)
    await context.bot.send_poll(chat_id=chat_id, question=f"📚 Study Boost: {p['q']}", options=p['opt'], correct_option_id=p['ans'], type="quiz", is_anonymous=False)

# --- 🎨 IMAGE GENERATION ---
async def generate_image(prompt):
    try:
        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": f"Generate image: {prompt}"}], image_generate=True)
        return res
    except: return None

# --- 🚀 COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if u_id == OWNER_ID:
        text = f"Pranam Mere Maalik King {OWNER_USERNAME}! 🔱✨\n\nAb Misbu ke paas 'Student', 'Aatma', 'Draw' aur 'Polls' jaise saare weapon hain!"
        kb = [[InlineKeyboardButton("🛠️ MARAMMAT", callback_data="mod"), InlineKeyboardButton("📢 ELAAN", callback_data="bc")],
              [InlineKeyboardButton("👻 AATMA MODE", callback_data="aatma_mode"), InlineKeyboardButton("🎓 STUDENT ZONE", callback_data="student_zone")]]
    elif u_id in PREMIUM_USERS:
        text = "Salam Premium User! ✨\n\nAapke liye 'Student' aur 'Aatma' zone open hai. Enjoy kijiye!"
        kb = [[InlineKeyboardButton("👻 AATMA MODE", callback_data="aatma_mode"), InlineKeyboardButton("🎓 STUDENT ZONE", callback_data="student_zone")]]
    else:
        text = "Hii! Main **Misbu** hoon... ✨❤️\n\nMain aapki study aur group dono sambhaal lungi. Sabse best features ke liye Premium lijiye!"
        kb = [[InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
              [InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

async def draw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if not (u_id == OWNER_ID or u_id in PREMIUM_USERS):
        return await update.message.reply_text(f"Ouch! 🥺 Ye feature Premium walo ke liye hai. UPI: `{UPI_ID}`")
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("Kya draw karun baby? ✨")
    msg = await update.message.reply_text("Kuch special bana rahi hoon... 🎨")
    img = await generate_image(prompt)
    if img: await update.message.reply_photo(img, caption="Ye lijiye aapka tohfa! ❤️")

# --- 🛡️ CALLBACK HANDLERS ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "buy_premium":
        msg = f"🔱 **PREMIUM ACCESS** 🔱\n\n✅ Unlock Student Zone\n✅ Unlock Aatma Mode\n\n💳 UPI: `{UPI_ID}`\nBhejo aur @{OWNER_USERNAME} ko DM karo! ✨"
        await query.message.reply_text(msg)
    elif query.data == "aatma_mode":
        await query.message.reply_text("👻 **AATMA MODE ACTIVE**\nDuniya ke har bot ki shakti ab mujhme hai! ✨")
    elif query.data == "student_zone":
        await query.message.reply_text("🎓 **STUDENT ZONE**\nApne exam ka naam likho, main material dhundh laungi! 📚")

# --- 🤖 POWER LOGIC ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    if u_id == OWNER_ID and text.startswith("AddVIP:"):
        PREMIUM_USERS.add(int(text.split(":")[1].strip()))
        return await update.message.reply_text("✅ VIP Added!")
    
    if update.effective_chat.type == "private" or context.bot.username in text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        
        if u_id == OWNER_ID or u_id in PREMIUM_USERS:
            system_p = "You are Misbu Supreme. Provide study notes, exam tips, lecture links, and bot abilities perfectly."
        else:
            system_p = "You are a sweet flirty girl Misbu. Use emojis. If study/high-fi tools are asked, ask for premium."

        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "system", "content": system_p}, {"role": "user", "content": text}])
        await update.message.reply_text(res)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("draw", draw))
    app.add_handler(CommandHandler("boost", lambda u, c: c.job_queue.run_repeating(send_daily_poll, interval=86400, first=10, chat_id=u.effective_chat.id)))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
    app.run_polling()

if __name__ == '__main__': main()
    
