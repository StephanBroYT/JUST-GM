from disnake.ext import commands
import disnake

from config import TOKEN
import logging

logging.basicConfig(level=logging.INFO)

intents = disnake.Intents.all()
intents.message_content = True

bot = commands.Bot(
    command_prefix = "/",
    intents = intents,
    activity = disnake.Game("Делаю гифки"),
    status = disnake.Status.do_not_disturb
)

@bot.event
async def on_ready():
    bot.load_extension("cogs.fun")
    bot.load_extension("cogs.convert")
    bot.load_extension("cogs.convert_command")
    print(f"Logged in as {bot.user}")




bot.run(TOKEN)
