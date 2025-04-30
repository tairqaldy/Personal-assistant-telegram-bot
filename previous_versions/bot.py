import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_PROMPT = os.getenv("OWNER_PROMPT")

# Инициализация OpenAI клиента
client = OpenAI(api_key=OPENAI_API_KEY)

# Загрузка предопределённых ответов
with open("predefined_answers.json", "r", encoding="utf-8") as f:
    predefined_answers = json.load(f)

# Нормализация текста
def normalize(text):
    return text.lower().strip()

# Функция ответа через OpenAI
async def answer_with_ai(question: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": OWNER_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return chat_completion.choices[0].message.content.strip()

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    norm_msg = normalize(user_msg)

    for key in predefined_answers:
        if key in norm_msg:
            await update.message.reply_text(predefined_answers[key])
            return

    try:
        ai_reply = await answer_with_ai(user_msg)
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text(f"Произошла ошибка: {e}")

# Команда /contact
async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_info = (
        "📞 Контакты Tair:\n"
        "Telegram: @tairqaldy\n"
        "Email: taircaldy.yt@gmail.com\n"
        "Телефон: +7707..."
    )
    await update.message.reply_text(contact_info)

# Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
