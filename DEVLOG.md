# 📓 Developer Log — Tair Telegram Bot

This document tracks key development decisions, bugs, and solutions encountered while building and improving the Tair Assistant Bot.

---

## 📅 [Day 1] — Initial Setup

**✅ Tasks:**
- Installed `python-telegram-bot`, `openai`, and `python-dotenv`
- Initialized `.env` for sensitive credentials
- Basic bot responding to `/start` and echoing messages

**❗ Problem:** API call to OpenAI was outdated (`openai.ChatCompletion.create`)
**✅ Solution:** Upgraded to `openai>=1.0.0`, switched to:
```python
client.chat.completions.create(...)
```

---

## 📅 [Day 2] — Custom Persona & Predefined Answers

**✅ Tasks:**
- Added `OWNER_PROMPT` to .env to make GPT replies sound like Tair
- Defined `predefined_answers` inline
- Added contact keywords and fallback to GPT-4-turbo

**💡 Insight:** Keeping `predefined_answers` inside code avoids extra I/O

---

## 📅 [Day 3] — Logging & Blocking

**✅ Tasks:**
- Structured logs into `logs.csv`
- Created `blocked_users.txt`
- Created `/block` and `/unblock` admin-only commands

**❗ Problem:** Wanted to block by username, but only user_id is consistent
**✅ Solution:** Store user ID (numeric) in `blocked_users.txt`

---

## 📅 [Day 4] — Admin Group Integration

**✅ Tasks:**
- Created `ADMIN_CHAT_ID` field
- Forwarded urgent & contact requests to admin group
- Used Markdown formatting for messages

**📌 Note:** Markdown requires escaping special characters if dynamic content

---

## 📅 [Day 5] — Refactoring and Finalization

**✅ Tasks:**
- Split predefined responses clearly from AI logic
- Created detailed `README.md`
- Added `/logs` and debugging handler for `/myid`
- Made everything async-compatible and production-safe

---

## 🛠 Planned Improvements

- Google Sheets export of logs
- CSV download command for admin
- Auto-reply based on time (e.g. “Tair is likely asleep, leave a message”)
- User analytics: most common queries, response performance
- Voice message to text using OpenAI Whisper

---

## ✍️ Notes

Feel free to extend this devlog with:
- Bug reports
- Feature milestones
- Architecture sketches
- Refactoring decisions