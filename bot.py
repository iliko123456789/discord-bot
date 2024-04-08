import discord
from discord.ext import commands
import responses

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = ''
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True 
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event 
    async def on_ready():
        print(f'{bot.user} is now running!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f'{username} said: "{user_message}" ({channel})')

        if user_message.startswith('?'):
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

        await bot.process_commands(message)

    @bot.command()
    async def calc(ctx, operation: str, number1: float, number2: float):
        """Perform basic arithmetic operations."""
        try:
            if operation == "+" :
                result = number1 + number2
            elif operation == "-":
                result = number1 - number2
            elif operation == "*":
                result = number1 * number2
            elif operation == "/":
                if number2 != 0:
                    result = number1 / number2
                else:
                    result = "Error: Division by zero"
            else:
                result = "Invalid operation"

            await ctx.send(f'Result: {result}')
        except Exception as e:
            await ctx.send(f'An error occurred: {str(e)}')

    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'Kicked {member.name}')

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'Banned {member.name}')

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def delete(ctx, amount: int):
        await ctx.channel.purge(limit=amount + 1)

    bot.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()
