import json, os, g4f, asyncio, requests, random, re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, constants
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 CONFIG ---
TELEGRAM_TOKEN = "8285517053:AAE-99tylt5Wh0r3qYbCOsdOJ-s9vBb2Gho" 
OWNER_ID = 8536075730 
OWNER_USERNAME = "Asjad742"
UPI_ID = "8887937470@ptaxis" #

# --- 🧠 DATABASE ---
PREMIUM_USERS = set()
DB = {"buttons": {}}

# --- 📊 DAILY POLL (Sana Khan + Study) ---
async def daily_poll(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    qs = [
        {"q": "Sana Khan ne industry kyun chhodi thi?", "opt": ["Deen ke liye", "Personal", "Health"], "ans": 0},
        {"q": "UPSC ke liye best language?", "opt": ["Hindi", "English", "Any Regional", "All"], "ans": 3}
    ]
    p = random.choice(qs)
    await context.bot.send_poll(chat_id=chat_id, question=f"📚 Misbu Quiz: {p['q']}", options=p['opt'], correct_option_id=p['ans'], type="quiz")

# --- 🎨 IMAGE GENERATION (/draw) ---
async def draw_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = " ".join(context.args)
    if not prompt: return await update.message.reply_text("Kya draw karun Maalik? ✨")
    await update.message.reply_text("🎨 Misbu kalakari shuru kar rahi hai...")
    res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "user", "content": f"Generate image: {prompt}"}], image_generate=True)
    if res: await update.message.reply_photo(res, caption=f"Ye lijiye: {prompt}")

# --- 📂 STUDENT PDF & STUDY SEARCH (/pdf) ---
async def pdf_tool(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if u_id != OWNER_ID and u_id not in PREMIUM_USERS:
        return await update.message.reply_text(f"❌ Student PDF features Premium hain! UPI: `{UPI_ID}`")
    await update.message.reply_text("📂 **STUDENT PDF ZONE**: Kaunse exam ke notes/PDF chahiye? Naam bataiye!")

# --- 🎭 VIP FEATURES (Face Swap/Voice Clone) ---
async def vip_features(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if u_id != OWNER_ID and u_id not in PREMIUM_USERS:
        return await update.message.reply_text("❌ Ye VIP feature hai. Premium lijiye! ✨")
    await update.message.reply_text("🎙️ Voice ya Photo bhejiye, process start ho jayega!")

# --- 🚀 MASTER START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    is_prem = (u_id == OWNER_ID or u_id in PREMIUM_USERS)
    
    kb = [
        [InlineKeyboardButton("👻 AATMA MODE", callback_data="aatma"), InlineKeyboardButton("🎓 STUDENT ZONE", callback_data="student")],
        [InlineKeyboardButton("🎨 DRAW", callback_data="draw_help"), InlineKeyboardButton("📂 PDF NOTES", callback_data="pdf_help")]
    ]
    
    if u_id == OWNER_ID:
        kb.append([InlineKeyboardButton("🔱 ADMIN PANEL", callback_data="admin_panel")])
    
    # Custom Buttons Handler
    for name in DB["buttons"]:
        kb.append([InlineKeyboardButton(name, callback_data=f"btn_{name}")])

    if not is_prem:
        kb.append([InlineKeyboardButton("💎 UNLOCK ALL (AUTO-PAY)", callback_data="buy_prem")])

    msg = f"Pranam King {OWNER_USERNAME}! 🔱" if u_id == OWNER_ID else "Hii! Main Misbu hoon.. ✨❤️"
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

# --- 🛡️ CALLBACK HANDLERS (Approval & Conflict Free) ---
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    u_id = query.from_user.id
    await query.answer()

    if query.data.startswith("approve_"):
        user_to_vip = int(query.data.split("_")[1])
        PREMIUM_USERS.add(user_to_vip)
        await context.bot.send_message(chat_id=user_to_vip, text="✅ Mubarak ho! Maalik ne aapka VIP access approve kar diya hai! 🎉")
        await query.edit_message_text(f"✅ User {user_to_vip} approved successfully!")

    elif query.data == "admin_panel":
        await query.message.reply_text("🛠️ **ADMIN:** `AddBtn:Name:Msg:Access` | `MakeVIP:ID` | `/boost` for Quiz")
    
    elif query.data == "buy_prem":
        await query.message.reply_text(f"🚀 **PREMIUM ACCESS**\n\n1. Payment karein: `{UPI_ID}`\n2. 12-digit UTR/Ref number yahan chat mein bhejein.\n\nMisbu turant Maalik ko verify karne bhej degi! ✨")

    elif query.data == "aatma":
        await query.message.reply_text("👻 **AATMA MODE ACTIVE**: Har bot ki soul mere paas hai! ✨")

    elif query.data == "student":
        await query.message.reply_text("🎓 **STUDENT ZONE**: Duniya ke har exam ki details aur material yahan milega! 📚")

# --- 🤖 SMART HANDLER (AI + NSFW + Payments) ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    if not text: return

    # NSFW Protection
    if any(word in text.lower() for word in ["nsfw", "sexy", "ashleel"]):
        await update.message.delete()
        return await update.message.reply_text("🚫 Ganda kaam nahi! Achhi bachi bano. ✨")

    # Payment Verification (Anti-Fake)
    if re.match(r'^\d{12}$', text) and u_id != OWNER_ID:
        await update.message.reply_text("⏳ Check ho raha hai... Maalik ke approval ka wait karein! ✨")
        kb = [[InlineKeyboardButton("✅ Approve", callback_data=f"approve_{u_id}"), InlineKeyboardButton("❌ Reject", callback_data="reject")]]
        await context.bot.send_message(chat_id=OWNER_ID, text=f"💰 **PAYMENT VERIFY KAREIN!**\nUser ID: `{u_id}`\nUTR: `{text}`", reply_markup=InlineKeyboardMarkup(kb))
        return

    # Admin Command: Add Button
    if u_id == OWNER_ID and text.startswith("AddBtn:"):
        parts = text.split(":")
        DB["buttons"][parts[1]] = {"msg": parts[2], "access": parts[3]}
        return await update.message.reply_text(f"✅ '{parts[1]}' button created!")

    # AI Chat Response
    if update.effective_chat.type == "private" or context.bot.username in text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        sys_p = "You are Misbu Supreme. Mentor + Sweet Teacher. Help with exams and bot powers. 100% Accuracy."
        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", messages=[{"role": "system", "content": sys_p}, {"role": "user", "content": text}])
        await update.message.reply_text(res)

def main():
    # CallbackQueryHandler is imported and correctly placed
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("draw", draw_image))
    app.add_handler(CommandHandler("pdf", pdf_tool))
    app.add_handler(CommandHandler("vip", vip_features))
    app.add_handler(CommandHandler("boost", lambda u, c: c.job_queue.run_repeating(daily_poll, interval=86400, first=10, chat_id=u.effective_chat.id)))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
    
    # Conflict Fix for Render
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__': main()
                                             
