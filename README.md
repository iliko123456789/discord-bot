# Discord-bot2.0

A powerful Discord bot powered by a **local LLaMA3 AI model** (via Ollama) that can chat, perform calculations, search online, and manage server roles.

---

## Features
- 💬 Chat with AI using `!bot <message>`
- 🛡️ Admin commands (`!admin`, `!revoke`)
- 👢 Kick, ban, and unban users
- 🧹 Remove messages with `!remove <number>`
- 🖥️ Works with a local LLaMA3 AI model (fast if using GPU)
- 💾 Stores chat memory in `bot_memory.json`
- 🌐 Web search fallback for uncertain AI responses *(under development ⚠️)*

---

## Installation

Make sure you have Python 3.10+ installed.

Install required Python libraries:

```bash
pip install discord.py
pip install requests
pip install beautifulsoup4
