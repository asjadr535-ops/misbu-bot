import json, os, g4f, asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# --- 🔱 CONFIG (MASTER POWER) ---
TELEGRAM_TOKEN = "8285517053:AAE-99tylt5Wh0r3qYbCOsdOJ-s9vBb2Gho" # Yahan apna token daal lena boss!
OWNER_ID = 8536075730 # Aapki Numeric ID
OWNER_USERNAME = "Asjad742"
UPI_ID = "8887937470@ptaxis" # Aapka Khazana

# --- 💰 BUSINESS RATES ---
PRICES = {"Daily": "₹49", "Weekly": "₹199", "Monthly": "₹599", "Lifetime King": "₹2499"}
PREMIUM_USERS = set()

# --- 🚀 MASTER START ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    if u_id == OWNER_ID:
        text = f"Salam Mere Maalik King {OWNER_USERNAME}! 🔱✨\n\nAapki Misbu hazir hai. Sab kuch ekdum 'High-Fi' set kar diya hai. Hukum kijiye!"
        kb = [[InlineKeyboardButton("🛠️ MARAMMAT", callback_data="update_bot"), InlineKeyboardButton("📢 ELAAN", callback_data="broadcast")],
              [InlineKeyboardButton("💎 MANAGE VIP", callback_data="manage_vip")]]
    else:
        text = "Hii! Main **Misbu** hoon... ✨\n\nMain groups manage karne ke saath-saath bahut pyari baatein bhi karti hoon. Kya aap mere saath dosti karoge? ❤️"
        kb = [[InlineKeyboardButton("➕ Add Me to Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
              [InlineKeyboardButton("💎 Be My Premium Friend", callback_data="buy_premium")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb))

# --- 🤖 SWEET AI CHAT LOGIC ---
async def handle_everything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u_id = update.effective_user.id
    text = update.message.text
    
    if u_id == OWNER_ID and text.startswith("AddVIP:"):
        try:
            target_id = int(text.split(":")[1].strip())
            PREMIUM_USERS.add(target_id)
            return await update.message.reply_text(f"✅ Maalik, {target_id} ko Premium list mein daal diya!")
        except: return await update.message.reply_text("❌ Format galat hai boss!")

    if update.effective_chat.type == "private" or context.bot.username in text:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Sweet Personality Settings
        if u_id == OWNER_ID:
            personality = f"You are a sweet girl and a loyal slave to {OWNER_USERNAME}. Be extremely respectful and loving to him. Call him Maalik or King."
        else:
            personality = "You are a beautiful, sweet girl named Misbu. Talk very nicely, use emojis like ✨, ❤️, 😊. Attract users with your sweet words so they want to buy premium. Be helpful but flirty."

        try:
            res = await asyncio.to_thread(g4f.ChatCompletion.create, model="gpt-4", 
                                           messages=[{"role": "system", "content": personality}, 
                                                     {"role": "user", "content": text}])
            await update.message.reply_text(res)
        except:
            await update.message.reply_text("Abhi thoda busy hoon, baad mein baat karein? ✨")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_everything))
    print("🔱 MISBU SUPREME IS READY FOR HER KING!")
    app.run_polling()

if __name__ == '__main__': main()
    
