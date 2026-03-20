import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# PowerShell logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Configuration ---
TELEGRAM_TOKEN = '8637690135:AAF08M3tUCZTwBanKuBZaxV-Dp1-Ejw55oo'
GEMINI_API_KEY = 'AIzaSyD5D8utSniLkdBEK70F8AMFDdI8QObP_kE'
ADMIN_ID = 8617814640 
KPAY_NUMBER = "09698937182"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

PAID_USERS = {8617814640}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send me any topic to write.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in PAID_USERS:
        await update.message.reply_text("Please upgrade to Premium first.")
        return

    await update.message.reply_chat_action("typing")
    try:
        response = model.generate_content(f"Write Burmese content: {update.message.text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"❌ Gemini API Error:\n{str(e)}\n\nHint: Check your VPN.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).connect_timeout(60).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is starting... Please try to send a message in Telegram.")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()