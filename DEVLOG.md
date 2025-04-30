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
- Refactoring decisions---

## 📅 [Day 6] — Git Security & Hook Protection

**✅ Tasks:**
- Added `.gitignore` to prevent committing `.env` and other secrets
- Learned that even if `.env` is ignored, it can still be committed if already staged

**❗ Problem:** `.env` was pushed even though it was in `.gitignore`

**✅ Solution:**
```bash
git rm --cached .env
```
- This removes it from Git’s index without deleting it locally

**🛡 Hook Protection:**
- Created a `pre-commit` script to prevent accidental commits of `.env` or keys like `OPENAI_API_KEY`
- Moved it to `.git/hooks/pre-commit`

**🧠 Learned:** On Windows, `chmod` isn't available — but Git hooks still work without it  
- Used PowerShell to move the hook:
```powershell
mv pre-commit .git/hooks/pre-commit
```
- Then manually changed line endings to `LF` via VS Code (important for Git Bash compatibility)

**💡 Tip:** Git Bash is recommended for hook scripts on Windows.---

## 🚀 Deployment & GitHub Publishing Checklist

### ✅ Before Pushing to GitHub

- [x] Add `.env` to `.gitignore`
- [x] Run `git rm --cached .env` to untrack secrets
- [x] Set up `.gitattributes` and `.git/hooks/pre-commit` to protect credentials
- [x] Test that `.env` no longer appears in `git ls-files`

---

### 🌐 GitHub Repository Setup

1. Create a **private GitHub repository** (public only if secrets are 100% excluded)
2. Push project:
```bash
git init
git remote add origin https://github.com/yourusername/tair-telegram-bot.git
git add .
git commit -m "🚀 Initial commit — ready for deployment"
git push -u origin main
```

3. Add a `README.md`, `LICENSE`, and `.gitignore` (already done ✅)
4. Protect `main` branch (GitHub settings → Branches → Protection rules)

---

### ☁️ Optional Hosting (24/7 Bot Running)

#### 1. **Railway.app (free tier)**
- Create new project → Deploy from GitHub
- Add environment variables:
  - `TELEGRAM_BOT_TOKEN`
  - `OPENAI_API_KEY`
  - `OWNER_PROMPT`, `ADMIN_CHAT_ID`, `OWNER_USER_ID`

#### 2. **Render.com**
- Add Python service → Connect GitHub → Deploy
- Set build command: `pip install -r requirements.txt`
- Run command: `python bot_v5_final_clean.py`

#### 3. **VPS with PM2 (Linux server)**
```bash
# Install dependencies and run
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pm2 start bot_v5_final_clean.py --interpreter=python3
pm2 save
pm2 startup
```

---

### ✅ Tips for Publishing as Open Source

- **Keep `.env` and logs private** (never push secrets)
- **Use MIT License** if you want others to freely use it
- **Enable Discussions/Issues** to collect ideas or feedback
- Add contributors or collaborators if working in a team

---

## 💡 You’re now ready to deploy your bot like a pro 😎