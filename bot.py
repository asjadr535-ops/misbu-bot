import json, os, g4f, asyncio, random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 CONFIG (ULTIMATE POWER) ---
TELEGRAM_TOKEN = "8285517053:AAHbUrKM398ezjLovmpV9kSde05u7s-QQCc" #
OWNER_ID = 8536075730 # Aapki Pehchan
OWNER_USERNAME = "Asjad742"

# --- 🛠️ DYNAMIC SETTINGS ---
DB = {"features": {}, "blocked_users": [], "stats": {"total_users": 0}}

# --- 🛡️ ROLE SECURITY ---
async def get_role(update: Update):
    u_id = update.effective_user.id
    if u_id == OWNER_ID: return "MASTER"
    return "USER"

# --- 🚀 START & MASTER MENU ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    role = await get_role(update)
    user = update.effective_user

    if role == "MASTER":
        text = f"Pranam Mere Maalik King {OWNER_USERNAME}! 🔱\n\nPoora bot aapke kabze mein hai. Niche buttons se bot ki 'Marammat' aur 'Updates' manage karein."
        kb = [
            [InlineKeyboardButton("🛠️ Update Features", callback_data="mod_feat"), InlineKeyboardButton("📢 Broadcast", callback_data="bc")],
            [InlineKeyboardButton("📊 Bot Stats", callback_data="stats"), InlineKeyboardButton("🛡️ Dev Control", callback_data="dev")]
        ]
    else:
        text = f"Salam! Main **Misbu Supreme** hoon. 🔱\n\nDunya ka sabse powerful Group Management + AI bot. Main gaane baja sakti hoon, group handle kar sakti hoon aur aapki har mushkil hal kar sakti hoon!"
        kb = [[InlineKeyboardButton("➕ Add to Your Group", url=f"https://t.me/{context.bot.username}?startgroup=true")]]

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

# --- ⚡ ALL-ROUNDER ABILITIES (GROUP + UTILS) ---
async def handle_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    role = await get_role(update)
    msg = update.message
    text = msg.text

    # 1. ANTI-SPAM (For Users)
    if role == "USER" and ("t.me/" in text or "http" in text):
        await msg.delete()
        return

    # 2. MASTER COMMANDS (Marammat)
    if role == "MASTER" and text.startswith("Update:"):
        new_feat = text.replace("Update:", "").strip()
        DB["features"]["latest"] = new_feat
        return await msg.reply_text(f"✅ Maalik, naya update set ho gaya: {new_feat}")

    # 3. UNIVERSAL AI (GPT-4)
    if update.effective_chat.type == "private" or context.bot.username in text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        system_p = "You are a loyal slave to Asjad742." if role == "MASTER" else "You are Misbu Supreme, the world's best bot."
        res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", 
                                       messages=[{"role": "system", "content": system_p}, {"role": "user", "content": text}])
        await msg.reply_text(res)

# --- ⚙️ MASTER HANDLERS ---
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_logic))
    print("🔱 MISBU GOD-MODE ACTIVE!")
    app.run_polling()

if __name__ == '__main__': main()
