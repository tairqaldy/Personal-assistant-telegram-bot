import os
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

# Загрузка переменных из .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_PROMPT = os.getenv("OWNER_PROMPT")

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Предопределённые ответы
predefined_answers = {
    "привет": "Привет! Рад тебя видеть 🙂",
    "как дела": "Всё отлично, спасибо! Чем могу помочь?",
    "ты кто": "Я — AI помощник от имени Tair. Могу подсказать, направить или помочь!",
    "что ты умеешь": "Я могу ответить на вопросы, помочь с навигацией и связать тебя с Tair’ом при необходимости.",
    "можно поговорить с таиром": "Сейчас он может быть занят. Я передам твоё сообщение или можешь сам написать: @tairqaldy",
    "как связаться": "Связаться с Tair можно через Telegram: @tairqaldy или Email: taircaldy.yt@gmail.com"
}

# Ключевые слова для направления к Tair'у
contact_keywords = ["таир", "связаться", "поговорить", "консультация", "лично"]

# Главное меню
def get_main_keyboard():
    keyboard = [
        [KeyboardButton("🧠 Что умеет бот"), KeyboardButton("📞 Связаться с Tair’ом")],
        [KeyboardButton("❓ Помощь")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Привет! Я — Tair Bot.\n\n"
        "Я помогу тебе с быстрыми ответами, связью с Tair'ом и другими задачами.\n"
        "Просто нажми кнопку ниже 👇"
    )
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

# Ответ от OpenAI
async def answer_with_ai(question: str) -> str:
    chat_completion = client.chat.completions.create(
    model="gpt-4-turbo",  # 👈 перешли с gpt-3.5-turbo
    messages=[
        {"role": "system", "content": OWNER_PROMPT},
        {"role": "user", "content": question}
    ],
    max_tokens=2048  # можно увеличить до 2048+ при необходимости
    )
    return chat_completion.choices[0].message.content.strip()

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.lower().strip()

    # Обработка кнопок
    if user_msg == "🧠 что умеет бот":
        await update.message.reply_text(
            "Я могу:\n- Ответить на часто задаваемые вопросы\n- Помочь найти информацию\n- Передать сообщение Tair’у\n- Сориентировать по командам и функциям",
            reply_markup=get_main_keyboard()
        )
        return

    if user_msg == "📞 связаться с tair’ом":
        await update.message.reply_text(
            "📩 Напиши Tair'у напрямую в Telegram: @tairqaldy\n"
            "Или на email: taircaldy.yt@gmail.com",
            reply_markup=get_main_keyboard()
        )
        return

    if user_msg == "❓ помощь":
        await update.message.reply_text(
            "Ты можешь использовать команды:\n"
            "/start — главное меню\n"
            "/contact — контакты Tair’а\n"
            "/services — что умеет бот\n"
            "/book — как записаться\n"
            "/help — все команды",
            reply_markup=get_main_keyboard()
        )
        return

    # Предзаписанный ответ
    for key in predefined_answers:
        if key in user_msg:
            await update.message.reply_text(predefined_answers[key], reply_markup=get_main_keyboard())
            return

    # Проверка, не хочет ли пользователь связаться с Tair'ом
    for word in contact_keywords:
        if word in user_msg:
            await update.message.reply_text(
                "Если хочешь связаться с Tair’ом, можешь написать напрямую 👉 @tairqaldy\n"
                "Я также могу передать твоё сообщение, если хочешь.",
                reply_markup=get_main_keyboard()
            )
            return

    # Ответ от AI
    try:
        ai_reply = await answer_with_ai(user_msg)
        await update.message.reply_text(ai_reply, reply_markup=get_main_keyboard())
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}", reply_markup=get_main_keyboard())

# Команда /contact
async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Контакты Tair:\nTelegram: @tairqaldy\nEmail: taircaldy.yt@gmail.com\nТелефон: +7707...",
        reply_markup=get_main_keyboard()
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Доступные команды:\n"
        "/start — Главное меню\n"
        "/contact — Контакты\n"
        "/services — Что умеет бот\n"
        "/book — Как записаться\n"
        "/help — Все команды",
        reply_markup=get_main_keyboard()
    )

# Команда /services
async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 Бот может:\n- Отвечать на вопросы\n- Помогать найти нужную инфу\n- Направлять к Tair’у\n- Быть вашим AI-ассистентом",
        reply_markup=get_main_keyboard()
    )

# Команда /book
async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 Чтобы записаться:\n1. Напиши @tairqaldy в Telegram\n2. Или жми сюда: https://t.me/tairqaldy",
        reply_markup=get_main_keyboard()
    )

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    await update.message.reply_text(f"Chat ID: `{chat.id}`", parse_mode="Markdown")

# Запуск
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CommandHandler("book", book_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.GROUPS, get_chat_id))



    print("✅ Tair Bot запущен")
    app.run_polling()
