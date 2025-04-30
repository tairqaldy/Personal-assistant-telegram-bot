# 🤖 Tair Telegram Assistant Bot

An intelligent Telegram bot assistant designed to communicate like Tair, answer questions, forward important or urgent messages, and help users with information. Built with `python-telegram-bot`, OpenAI GPT-4-turbo, and includes features like logging, moderation, and structured admin control.

---

## 📦 Features

- GPT-4-turbo powered AI replies (based on your persona)
- Predefined smart responses to common questions
- Structured handling of:
  - ❗ Urgent messages
  - 📩 Contact requests
- Admin-only commands:
  - `/logs` — View recent message logs
  - `/block <user_id>` — Block spammers
  - `/unblock <user_id>` — Unblock users
- Persistent logs in `logs.csv`
- Blocked users stored in `blocked_users.txt`
- Clean menu with reply keyboard interface

---

## ⚙️ Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/your-repo/tair-telegram-bot.git
cd tair-telegram-bot
```

### 2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_api_key
OWNER_PROMPT="You are Tair's assistant and speak just like him. Answer questions warmly, helpfully, and intelligently..."
ADMIN_CHAT_ID=-100xxxxxxxxxx         # Telegram group ID for forwarding
OWNER_USER_ID=123456789              # Your numeric Telegram user ID
```

To find your user ID: run `/myid` in a temporary command or use @userinfobot.

### 5. Run the bot

```bash
python botV5.2.py
```

---

## 🎮 Usage Guide

- Users are greeted with a friendly reply keyboard.
- They can press:
  - 🧠 *What can the bot do?* — Lists bot abilities
  - 📞 *Contact Tair* — Initiates structured contact flow
  - ❗ *Urgent message* — Initiates structured urgency flow
  - ❓ *Help* — Shows available commands

- Admin (you) can run:
  - `/logs` — shows the last 10 log entries from `logs.csv`
  - `/block <user_id>` — restricts user from using bot
  - `/unblock <user_id>` — allows user back in

---

## 🧠 Future Ideas & Extensions

- **Google Sheets export** for logs
- **CSV file download** directly from Telegram
- **Analytics dashboard** (user activity, FAQ coverage, etc.)
- **Voice-to-text queries** using Whisper/OpenAI audio models
- **Telegram channel FAQ bot mode**
- **Multilingual support** (Kazakh, Russian, English)
- **Custom modules** for:
  - IELTS/SAT tips
  - Programming expert
  - AI tools
  - University application support

---

## 📁 Project Structure

```
tair-telegram-bot/
├── .env
├── logs.csv
├── blocked_users.txt
├── requirements.txt
├── botV5.py
├── get_chat_id_bot.py
└── README.md
```

---

## 🔐 Security Notice

- Never upload `.env` to GitHub!
- Always `.gitignore` logs and credentials
- Store secrets in environment or CI/CD if deploying

---

## 🤝 Credits

Made by Tair Kaldybayev with ❤️  
GPT-4 integration powered by [OpenAI](https://platform.openai.com)  
Telegram bot built with [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot)

---

## 🪄 License

MIT License — free to use, build, or extend