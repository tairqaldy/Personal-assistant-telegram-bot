#Final MVP Template for teleram AI assistant bot made by tairqaldy.
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

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_PROMPT = os.getenv("OWNER_PROMPT")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
OWNER_USER_ID = int(os.getenv("OWNER_USER_ID"))

# Init OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Constants
LOG_FILE = "logs.csv"
BLOCKED_USERS_FILE = "blocked_users.txt"
AWAITING_URGENT_MSG, AWAITING_CONTACT_MSG = range(2)

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("🧠 what can the bot do?"), KeyboardButton("📞 contact tair")],
            [KeyboardButton("❗ urgent message"), KeyboardButton("❓ help")]
        ],
        resize_keyboard=True
    )

# Predefined messages
predefined_answers = {
    "hello": "Hi! How can I help you today? 🙂",
    "how are you": "I'm doing great! How can I assist you?",
    "who are you": "I'm an AI assistant speaking on behalf of Tair.",
    "what can you do": "I can help with Programming/IELTS/AI or forward messages to Tair.",
    "can i talk to tair": "Tair might be busy. I can forward your message or you can DM: @tairqaldy",
    "how to contact": "Telegram: @tairqaldy | Email: taircaldy.yt@gmail.com",

    "Привет": "Привет! как я могу сегодня тебе помочь?",
    "привет": "Привет! как я могу сегодня тебе помочь?",
    "как твои дела": "У меня все замечательно! Как я могу помочь?",
    "как твои дела?": "У меня все отлично! Как я могу помочь?",
    "кто ты":"Я ИИ-помощник, выступающий от имени Таира",
    "что ты умеешь":"Я могу помочь с Программированием/IELTS/AI или переслать сообщения Таиру",
    "могу ли я поговорить с Таиром": "Таир может быть занят. Я могу переслать ваше сообщение или вы можете написать DM: @tairqaldy",
    "как связаться": "Telegram: @tairqaldy | Email: taircaldy.yt@gmail.com"
    
}
contact_keywords = ["tair", "consult", "contact", "call", "meet", "urgent", "talk to", "Таир", "таир", "консультация", "позваонить", "связаться", "встретиться", "срочно", "проговорить с"]

# Blocking
def is_blocked(user_id):
    if not os.path.exists(BLOCKED_USERS_FILE):
        return False
    with open(BLOCKED_USERS_FILE, "r") as f:
        return str(user_id) in f.read()

def block_user(user_id):
    with open(BLOCKED_USERS_FILE, "a") as f:
        f.write(f"{user_id}\n")

def unblock_user(user_id):
    if not os.path.exists(BLOCKED_USERS_FILE):
        return
    with open(BLOCKED_USERS_FILE, "r") as f:
        lines = f.readlines()
    with open(BLOCKED_USERS_FILE, "w") as f:
        for line in lines:
            if line.strip() != str(user_id):
                f.write(line)

# Logging
def log_message(user_id, username, message, reply):
    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now(), user_id, username, message, reply])

# AI response
async def answer_with_ai(question: str) -> str:
    chat_completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": OWNER_PROMPT},
            {"role": "user", "content": question}
        ],
        max_tokens=1048
    )
    return chat_completion.choices[0].message.content.strip()

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! I'm Tair Bot. How can I assist you?", reply_markup=get_main_keyboard())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 Commands:\n/start — Main menu\n❗ Urgent message\n📞 Contact Tair",
        reply_markup=get_main_keyboard()
    )

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 Tair's contacts:\nTelegram: @tairqaldy\nEmail: taircaldy.yt@gmail.com\nPhone: +7707...",
        reply_markup=get_main_keyboard()
    )

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 I can:\n- Answer common questions\n- Forward messages to Tair\n- Help with Programming, IELTS or AI implementation",
        reply_markup=get_main_keyboard()
    )

async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📅 To book:\nMessage @tairqaldy on Telegram or click: https://t.me/tairqaldy",
        reply_markup=get_main_keyboard()
    )

# Main menu buttons
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.message.from_user

    if is_blocked(user.id):
        await update.message.reply_text("⛔️ You are blocked.")
        return

    if text == "🧠 what can the bot do?":
        await update.message.reply_text("I can help with questions or contact Tair.", reply_markup=get_main_keyboard())
    elif text == "📞 contact tair":
        await update.message.reply_text("Describe briefly why you want to contact Tair ⬇️")
        return AWAITING_CONTACT_MSG
    elif text == "❗ urgent message":
        await update.message.reply_text("Tell me the issue. I’ll forward it to Tair ⚠️")
        return AWAITING_URGENT_MSG
    elif text == "❓ help":
        await help_command(update, context)
    else:
        await general_message(update, context)

# Contact/Urgent collection
async def receive_urgent_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = f"🚨 *URGENT* from @{user.username or user.id}:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode="Markdown")
    await update.message.reply_text("Sent to Tair ✅", reply_markup=get_main_keyboard())
    return ConversationHandler.END

async def receive_contact_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = f"📩 *CONTACT REQUEST* from @{user.username or user.id}:\n\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=msg, parse_mode="Markdown")
    await update.message.reply_text("Message sent to Tair ✅", reply_markup=get_main_keyboard())
    return ConversationHandler.END

# Main chat response
async def general_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = user.username or "anonymous"

    if is_blocked(user.id):
        await update.message.reply_text("⛔️ You are restricted from using this bot.")
        return

    for key in predefined_answers:
        if key in text.lower():
            reply = predefined_answers[key]
            await update.message.reply_text(reply, reply_markup=get_main_keyboard())
            log_message(user.id, username, text, reply)
            return

    for word in contact_keywords:
        if word in text.lower():
            await update.message.reply_text("Want me to forward your message to Tair?", reply_markup=get_main_keyboard())
            return

    try:
        ai_reply = await answer_with_ai(text)
        await update.message.reply_text(ai_reply, reply_markup=get_main_keyboard())
        log_message(user.id, username, text, ai_reply)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

# Admin commands
async def view_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_USER_ID:
        return await update.message.reply_text("⛔️ Unauthorized.")
    if not os.path.exists(LOG_FILE):
        return await update.message.reply_text("📁 No logs yet.")
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.readlines()[-10:]
    await update.message.reply_text("🗂 Last 10 logs:\n" + "".join(logs))

async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_USER_ID:
        return await update.message.reply_text("⛔️ Unauthorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /block <user_id>")
    block_user(context.args[0])
    await update.message.reply_text(f"✅ User {context.args[0]} blocked.")

async def unblock_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_USER_ID:
        return await update.message.reply_text("⛔️ Unauthorized.")
    if not context.args:
        return await update.message.reply_text("Usage: /unblock <user_id>")
    unblock_user(context.args[0])
    await update.message.reply_text(f"✅ User {context.args[0]} unblocked.")

# App config
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CommandHandler("book", book_command))
    app.add_handler(CommandHandler("logs", view_logs))
    app.add_handler(CommandHandler("block", block_command))
    app.add_handler(CommandHandler("unblock", unblock_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons)],
        states={
            AWAITING_URGENT_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_urgent_msg)],
            AWAITING_CONTACT_MSG: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_contact_msg)],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    app.add_handler(conv_handler)

    print("🤖 Tair Assistant Bot V5.2 running...")
    app.run_polling()
