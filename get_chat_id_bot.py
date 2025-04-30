import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    print(f"Chat Title: {chat.title}")
    print(f"Chat ID: {chat.id}")
    await update.message.reply_text(f"✅ Chat ID найден: `{chat.id}`", parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, get_chat_id))
    print("🤖 Бот для получения chat_id запущен")
    app.run_polling()