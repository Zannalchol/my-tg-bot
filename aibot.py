import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Configuration ---
TELEGRAM_TOKEN = '8637690135:AAF08M3tUCZTwBanKuBZaxV-Dp1-Ejw55oo'
GEMINI_API_KEY = 'AIzaSyD5D8utSniLkdBEK70F8AMFDdI8QObP_kE'
ADMIN_ID = 8617814640 

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

PAID_USERS = {8617814640}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is Online on Cloud! Send me any topic to write.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if user_id not in PAID_USERS:
        await update.message.reply_text("Please upgrade to Premium to use this Bot.")
        return

    await update.message.reply_chat_action("typing")
    try:
        response = model.generate_content(f"Write professional content about: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        
        await update.message.reply_text(f"❌ Gemini Error: {str(e)}")

def main():
    PORT = int(os.environ.get("PORT", 8000))
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print(f"Bot is starting on Port {PORT}...")
    
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
