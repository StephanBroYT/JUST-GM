from disnake.ext import commands
import disnake

from config import TOKEN
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt="%m/%d/%Y %I:%M:%S %p",
    handlers=[
        logging.FileHandler("./logs.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

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
    bot.load_extension("cogs.ai")
    logging.info(f"Logged in as {bot.user}")




bot.run(TOKEN)
logging.info("Bot stopped")