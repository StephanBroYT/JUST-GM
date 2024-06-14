from disnake.ext import commands
import disnake
import os
import io
import imageio

from PIL import Image
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
    print(f"Logged in as {bot.user}")

bot.load_extension("cogs.fun")
bot.load_extension("cogs.convert")


bot.run("MTIzNzgxNzQ3Njk2ODg3ODExMQ.GKvn0T.jtWXMm-JHD-MDIdtbyY3xt1VvwV6EaZLOT7hY8")
