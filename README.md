Discord-bot2.0

A Discord bot powered by a local LLaMA3 AI model (via Ollama) that can chat, perform calculations, search online, and manage server roles.

Features

Chat with AI using !bot <message>

Admin commands (!admin, !revoke)

Kick, ban, unban users

Remove messages (!remove <number>)

Stores chat memory in bot_memory.json

Web search fallback for uncertain AI responses (under development ⚠️)

Works with a local LLaMA3 model (faster with GPU)

Requirements

Python 3.11 or newer, and the following Python libraries:

pip install discord.py
pip install requests
pip install beautifulsoup4


Other requirements:

Ollama
 installed with the llama3:latest model

Discord account and a server where you have permissions to add bots

Recommended System Configuration

To run LLaMA3 smoothly, especially with GPU acceleration:

Component	Recommended
CPU	Quad-core Intel i5 / AMD Ryzen 5 or better
RAM	16 GB or more
GPU	NVIDIA RTX 3060 / 4060 / 5070 or higher with 12GB+ VRAM (for faster AI inference)
Storage	SSD with at least 10 GB free
OS	Windows 10/11, macOS, or Linux

✅ The bot can run without a strong GPU, but AI responses will be slower. CPU-only mode is supported.

Installation

Clone this repository:

git clone https://github.com/iliko123456789/Discord-bot2.0.git
cd Discord-bot2.0


Install Python libraries:

pip install -r requirements.txt


(or install each manually using pip install discord.py requests beautifulsoup4)

Configure the bot:

Open bot.py

Replace TOKEN with your Discord bot token

Set your username for PROTECTED_USERNAME if you want special admin permissions

How to Create & Add the Bot to Your Discord Server
Step 1: Create a Bot in Discord Developer Portal

Go to Discord Developer Portal

Click New Application → give it a name → Create

Go to Bot → Click Add Bot → Confirm

Copy the bot token → put it in bot.py for TOKEN

Step 2: Add Bot to Your Server

Go to OAuth2 → URL Generator

Under Scopes, select bot

Under Bot Permissions, select the permissions your bot needs:

Administrator (optional, easier for testing)

Or select individually: Send Messages, Manage Roles, Kick Members, Ban Members, Manage Messages

Copy the generated URL and open it in your browser

Select your server → Authorize

Step 3: Run Your Bot
python bot.py


Your bot should come online in your Discord server

Use !help to see available commands

How It Works

The bot chats with AI via your local LLaMA3 model (Ollama)

Chat memory is stored in bot_memory.json

If AI is unsure, it can do a quick web search (under development)

Downloading and Setting Up LLaMA3
Option 1: Using Ollama (Recommended for Ease)

Install Ollama:

Visit Ollama Downloads
 and download the installer for your operating system.

Run the installer and follow the on-screen instructions.

Download the LLaMA3 Model:

Open a terminal or command prompt.

Run the following command to download the LLaMA3 model:

ollama run llama3


This command will download and run the LLaMA3 model locally.

Option 2: Using Meta's Official Method

Request Access:

Go to Meta's LLaMA Download Page
.

Fill out the required form to request access to the model.

Download the Model:

After approval, you'll receive an email with a download link.

Follow the instructions provided in the email to download the model.

Run the Model:

Once downloaded, you can run the model using the appropriate commands provided in the documentation.
