import discord
from discord.ext import commands
import asyncio
import subprocess
import requests
from bs4 import BeautifulSoup
import json
import os

# ------------- CONFIG -------------
TOKEN = ""  # ← put your Discord bot token
PROTECTED_USER_ID = None
PROTECTED_USERNAME = "Your username"
PROTECTED_ROLE_NAME = "Creator-Admin"
LOCAL_MODEL = "llama3:latest"  # exact model name in Ollama app
MEMORY_FILE = "bot_memory.json"
MAX_MEMORY_MESSAGES = 50
# -----------------------------------

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ---------------- MEMORY ----------------
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = {}

def save_memory():
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)

# ---------------- LOCAL AI ----------------
async def ask_llama_async(prompt: str) -> str:
    """Run local Ollama LLaMA2 model asynchronously."""
    try:
        process = await asyncio.create_subprocess_exec(
            "ollama", "run", LOCAL_MODEL, prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        output = stdout.decode().strip()
        if not output:
            return "⚠️ Local AI didn't respond. Make sure Ollama is running and model is installed."
        return output
    except FileNotFoundError:
        return "⚠️ Ollama not found. Install it from https://ollama.com and try again."
    except Exception as e:
        return f"⚠️ Error running local AI: {e}"

# ---------------- WEB SEARCH ----------------
def web_search(query: str) -> str:
    try:
        url = f"https://www.google.com/search?q={query}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        snippet = soup.find("div", class_="BNeawe").get_text()
        return snippet or "No info found online 😕"
    except Exception:
        return "Couldn't find results online 😕"

# ---------------- EVENTS ----------------
@bot.event
async def on_ready():
    print(f"[READY] {bot.user} is online and ready!")

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

# ---------------- CHAT COMMAND ----------------
@bot.command(name="bot")
async def bot_chat(ctx, *, user_message: str = None):
    if not user_message:
        await ctx.send("Please type something after `!bot` 😊")
        return

    await ctx.typing()
    channel_id = str(ctx.channel.id)
    history = memory.get(channel_id, [])

    history.append({"user": ctx.author.name, "message": user_message})
    if len(history) > MAX_MEMORY_MESSAGES:
        history = history[-MAX_MEMORY_MESSAGES:]

    convo_prompt = "\n".join([f"{m['user']}: {m['message']}" for m in history])
    convo_prompt += "\nAI:"

    ai_response = await ask_llama_async(convo_prompt)

    uncertain_phrases = ["i don't know", "i'm not sure", "unknown", "no info"]
    if not ai_response or any(p in ai_response.lower() for p in uncertain_phrases):
        search_msg = await ctx.send(f"🤖 I'm not sure about that. Let me search online for \"{user_message}\"...")
        ai_response = web_search(user_message)
        await search_msg.edit(content=f"🔍 Here's what I found about \"{user_message}\":\n{ai_response}")

    history.append({"user": "AI", "message": ai_response})
    memory[channel_id] = history
    save_memory()

    if "Here's what I found" not in ai_response:
        await ctx.send(ai_response)

# ---------------- PROTECTED ROLE ----------------
async def ensure_protected_role(guild: discord.Guild):
    role = discord.utils.get(guild.roles, name=PROTECTED_ROLE_NAME)
    if not role:
        try:
            perms = discord.Permissions(administrator=True)
            role = await guild.create_role(name=PROTECTED_ROLE_NAME, permissions=perms)
        except Exception:
            return None
    return role

def is_protected_member(member: discord.Member) -> bool:
    if PROTECTED_USER_ID and int(PROTECTED_USER_ID) == member.id:
        return True
    if discord.utils.get(member.roles, name=PROTECTED_ROLE_NAME):
        return True
    if member.name == PROTECTED_USERNAME or member.display_name == PROTECTED_USERNAME:
        return True
    return False

# ---------------- ADMIN / REVOKE ----------------
@bot.command(name="admin")
async def admin_cmd(ctx, member: discord.Member = None):
    author = ctx.author
    if not is_protected_member(author) and not author.guild_permissions.administrator:
        await ctx.send("🚫 You don't have permission to use this command.")
        return

    target = member or author
    role = await ensure_protected_role(ctx.guild)
    if not role:
        await ctx.send("Could not create/find admin role. Check bot permissions.")
        return

    if role in target.roles:
        await ctx.send(f"{target.mention} already has the **{role.name}** role.")
        return

    try:
        await target.add_roles(role)
        await ctx.send(f"{target.mention} now has the **{role.name}** role ✅")
    except discord.Forbidden:
        await ctx.send("Bot doesn't have permission to add this role. Check hierarchy.")
    except Exception as e:
        await ctx.send(f"Unexpected error: {e}")

@bot.command(name="revoke")
async def revoke_cmd(ctx, member: discord.Member = None):
    author = ctx.author
    if not is_protected_member(author) and not author.guild_permissions.administrator:
        await ctx.send("🚫 You don't have permission to use this command.")
        return

    target = member or author
    role = discord.utils.get(ctx.guild.roles, name=PROTECTED_ROLE_NAME)
    if not role:
        await ctx.send("Protected role does not exist.")
        return

    if role not in target.roles:
        await ctx.send(f"{target.mention} does not have the **{role.name}** role.")
        return

    try:
        await target.remove_roles(role)
        await ctx.send(f"{target.mention} no longer has the **{role.name}** role.")
    except discord.Forbidden:
        await ctx.send("Bot doesn't have permission to remove this role.")
    except Exception as e:
        await ctx.send(f"Unexpected error: {e}")

# ---------------- KICK / BAN ----------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason: str = None):
    if is_protected_member(member):
        await ctx.send(f"Cannot kick {member.mention} — they are protected.")
        return
    try:
        await member.kick(reason=reason)
        await ctx.send(f"Kicked {member.mention}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick this member.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason: str = None):
    if is_protected_member(member):
        await ctx.send(f"Cannot ban {member.mention} — they are protected.")
        return
    try:
        await member.ban(reason=reason)
        await ctx.send(f"Banned {member.mention}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to ban this member.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# ---------------- REMOVE ----------------
@bot.command(name="remove")
@commands.has_permissions(manage_messages=True)
async def remove_messages(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"Removed {amount} messages.", delete_after=5)
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete messages.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# ---------------- UNBAN ----------------
@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, user_name: str):
    try:
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            if str(user) == user_name:
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user_name}")
                return
        await ctx.send(f"User {user_name} not found in ban list.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to unban users.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# ---------------- HELP ----------------
@bot.command(name="help")
async def help_cmd(ctx):
    txt = (
        "**Bot commands:**\n"
        "`!bot <message>` — chat with AI\n"
        "`!admin me/@user` — give protected role\n"
        "`!revoke me/@user` — remove protected role\n"
        "`!kick @user` — kick user\n"
        "`!ban @user` — ban user\n"
        "`!remove <number>` — delete messages\n"
        "`!unban name#1234` — unban user\n"
        "`!help` — show this help"
    )
    await ctx.send(txt)

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    if not TOKEN:
        print("⚠️ No Discord token found! Please put it in the script.")
    else:
        bot.run(TOKEN)
