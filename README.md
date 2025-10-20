# Discord-bot2.0

A Discord bot powered by a local **LLaMA3 AI model** (via Ollama) that can chat, perform calculations, search online, and manage server roles.

---

## Features

- Chat with AI using `!bot <message>`
- Admin commands (`!admin`, `!revoke`)
- Kick, ban, unban users
- Remove messages (`!remove <number>`)
- Stores chat memory in `bot_memory.json`
- Web search fallback for uncertain AI responses (under development ⚠️)
- Works with a local LLaMA3 model (faster with GPU)

---

## Requirements

- **Python 3.11+**
- Discord account & server where you can add bots
- [Ollama](https://ollama.com/) installed with `llama3:latest` model

### Python Libraries

Install these with pip:

```bash
pip install discord.py
pip install requests
pip install beautifulsoup4
