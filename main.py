import discord
import os
from dotenv import load_dotenv
from colorama import Fore

intents = discord.Intents.all()

status = discord.Status.online
activity = discord.Game(name="Starting....")

bot = discord.Bot(
    intents=intents,
    debug_guilds=None,
    status=status,
    activity=activity
)

@bot.event
async def on_ready():
    print(Fore.GREEN + " ____ ____ ____ ____ ____ ____ ____ ____ ____ ____ ")
    print(Fore.GREEN + "||N |||i |||k |||o |||s |||# |||8 |||0 |||6 |||3 ||")
    print(Fore.GREEN + "||__|||__|||__|||__|||__|||__|||__|||__|||__|||__|| ")
    print(Fore.GREEN + "|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|")
    print(Fore.GREEN + Fore.LIGHTMAGENTA_EX + f"{bot.user} ist nun Online" + Fore.GREEN)



if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

load_dotenv()
bot.run(os.getenv("TOKEN"))
