import os
import csv
import datetime
from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

# Загрузка переменных окружения
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_PROMPT = os.getenv("OWNER_PROMPT")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))  # chat_id группы TK assistant admin group

# GPT-4-turbo клиент
client = OpenAI(api_key=OPENAI_API_KEY)

# Файлы
BLOCKED_USERS_FILE = "blocked_users.txt"
LOG_FILE = "logs.csv"

# ConversationHandler этапы
AWAITING_URGENT_MSG, AWAITING_CONTACT_MSG = range(2)

# Клавиатура
def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🧠 Что умеет бот"), KeyboardButton("📞 Связаться с Tair’ом")],
            [KeyboardButton("❗ Срочное сообщение"), KeyboardButton("❓ Помощь")]
        ],
        resize_keyboard=True
    )

# Ответы и ключевые слова
predefined_answers = {
    "привет": "Привет! Рад тебя видеть 🙂",
    "что ты умеешь": "Я могу ответить на вопросы, подсказать по Programmint/IELTS/AI, направить к Tair’у и многое другое."
}
contact_keywords = ["таир", "поговорить", "созвон", "консультация", "контакт", "лично"]

# Проверка на блок
def is_blocked(user_id):
    if not os.path.exists(BLOCKED_USERS_FILE):
        return False
    with open(BLOCKED_USERS_FILE, "r") as f:
        return str(user_id) in f.read()

# Логирование
def log_message(user_id, username, message, reply):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), user_id, username, message, reply])

# AI-ответ
async def answer_with_ai(question: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": OWNER_PROMPT},
            {"role": "user", "content": question}
        ],
        max_tokens=2048
    )
    return chat_completion.choices[0].message.content.strip()

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Я — Tair Bot.\nЧем могу помочь?", reply_markup=get_main_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Доступные команды:\n/start — Главное меню\n❗ Срочное сообщение\n📞 Связаться с Tair’ом",
        reply_markup=get_main_keyboard()
    )

# Обработка кнопок
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.message.from_user

    if is_blocked(user.id):
        await update.message.reply_text("⛔️ Вы были ограничены в доступе к этому боту.")
        return

    if text == "🧠 что умеет бот":
        await update.message.reply_text(
            "Я помощник Tair-а. Могу подсказать по SAT, IELTS, AI, поступлению и связаться с ним при необходимости.",
            reply_markup=get_main_keyboard()
        )
    elif text == "📞 связаться с tair’ом":
        await update.message.reply_text("Опиши, пожалуйста, кратко цель обращения, и я передам Tair'у ⬇️")
        return AWAITING_CONTACT_MSG
    elif text == "❗ срочное сообщение":
        await update.message.reply_text("Опиши срочно и ясно, в чём вопрос или проблема — я передам Tair’у ⚠️")
        return AWAITING_URGENT_MSG
    elif text == "❓ помощь":
        await help_command(update, context)
    else:
        await general_message(update, context)

# Приём срочного сообщения
async def receive_urgent_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    msg = f"🚨 *СРОЧНОЕ СООБЩЕНИЕ* от @{user.username or user.id}:\n\n{text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode="Markdown")
    await update.message.reply_text("Передал Tair'у. Он постарается ответить как можно скорее 🙌", reply_markup=get_main_keyboard())
    return ConversationHandler.END

# Приём запроса на связь
async def receive_contact_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    msg = f"📩 *ЗАПРОС СВЯЗИ* от @{user.username or user.id}:\n\n{text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode="Markdown")
    await update.message.reply_text("Передал! Tair напишет тебе, как только сможет ✉️", reply_markup=get_main_keyboard())
    return ConversationHandler.END

# Обычные сообщения
async def general_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = user.username or "без username"

    if is_blocked(user.id):
        await update.message.reply_text("⛔️ Вы были ограничены в доступе к этому боту.")
        return

    for key in predefined_answers:
        if key in text.lower():
            reply = predefined_answers[key]
            await update.message.reply_text(reply, reply_markup=get_main_keyboard())
            log_message(user.id, username, text, reply)
            return

    for word in contact_keywords:
        if word in text.lower():
            await update.message.reply_text("Хочешь, я передам Tair'у твоё сообщение? Напиши его, и я доставлю ✉️", reply_markup=get_main_keyboard())
            return

    try:
        ai_reply = await answer_with_ai(text)
        await update.message.reply_text(ai_reply, reply_markup=get_main_keyboard())
        log_message(user.id, username, text, ai_reply)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

# Конфигурация
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons)],
        states={
            AWAITING_URGENT_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_urgent_msg)],
            AWAITING_CONTACT_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_contact_msg)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv_handler)

    print("🤖 Бот V5 запущен")
    app.run_polling()
