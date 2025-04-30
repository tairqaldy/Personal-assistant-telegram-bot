import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram import ReplyKeyboardMarkup

# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_PROMPT = os.getenv("OWNER_PROMPT")

# Инициализация OpenAI клиента
client = OpenAI(api_key=OPENAI_API_KEY)

# Загрузка предопределённых ответов (можно расширить позже)
predefined_answers = {
    "привет": "Привет! Чем могу помочь?",
    "как тебя зовут": "Я Tair Kaldybayev Bot 🙂",
    "что ты умеешь": "Я могу отвечать на вопросы, направлять к Tair'у и помогать с информацией."
}

# Нормализация текста
def normalize(text):
    return text.lower().strip()

# Ответ через OpenAI
async def answer_with_ai(question: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": OWNER_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return chat_completion.choices[0].message.content.strip()

# Обработка входящих сообщений
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
        await update.message.reply_text(f"⚠️ Ошибка при ответе: {e}")

# Команда /contact
async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 Контакты Tair:\n\n"
        "Telegram: @tairqaldy\n"
        "Email: taircaldy.yt@gmail.com\n"
        "Телефон: +7707..."
    )
    await update.message.reply_text(text)

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 Команды бота:\n"
        "/contact — Мои контакты\n"
        "/services — Что я делаю\n"
        "/book — Как записаться\n"
        "/help — Список команд"
    )
    await update.message.reply_text(text)

# Команда /services
async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🛠 Чем я могу помочь:\n"
        "- Ответы на частые вопросы\n"
        "- Направление по нужной теме\n"
        "- Связь со мной при необходимости"
    )
    await update.message.reply_text(text)

# Команда /book
async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📆 Чтобы записаться:\n"
        "Напиши в Telegram 👉 @tairqaldy\n"
        "Или нажми здесь: https://t.me/tairqaldy"
    )
    await update.message.reply_text(text)

# Запуск приложения
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Подключаем команды
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CommandHandler("book", book_command))

    # Подключаем обработку обычных сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    print("🤖 Бот запущен и готов отвечать!")
    app.run_polling()
