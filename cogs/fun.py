import asyncio
import logging
from random import choice, randint

import disnake
from disnake import StageInstance
from disnake.ext import commands

logger = logging.getLogger(__name__)

komaru_gifs = [
    "https://imgur.com/tEe8LUQ",
    "https://imgur.com/icAkSwJ",
    "https://imgur.com/5pdZQMi",
    "https://imgur.com/0lyhEU9",
    "https://imgur.com/DCM8efc",
    "https://imgur.com/XHT4waQ",
    "https://imgur.com/POba4V6",
    "https://imgur.com/gQiVu37",
    "https://imgur.com/XLdLrCk",
    "https://imgur.com/2wMYSdB",
    "https://imgur.com/1VEkzot",
    "https://imgur.com/cIR7R6y",
    "https://imgur.com/0ifZu2i",
    "https://imgur.com/2uVYRVb",
    "https://imgur.com/vFI6446",
    "https://imgur.com/HICWYkN",
    "https://imgur.com/1wty42Q",
    "https://imgur.com/azs4YV8",
    "https://imgur.com/SdDkRJA",
    "https://imgur.com/JdDlCPm",
]

mention_gifs = [
    "https://tenor.com/view/cat-gif-26541280",
    "https://tenor.com/view/%D0%BA%D0%BE%D0%BC%D0%B0%D1%80%D1%83-gif-2755370182360042640",
]

class Fun(commands.Cog):
    def __init__(self, bot: disnake.ext.commands.Bot):
        self.bot = bot

    # @commands.command("самоуничтожение")
    # async def selfdestruction_command(self, ctx: commands.Context):
    #     await ctx.message.reply("https://imgur.com/8t9M1K9", mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.content == self.bot.user.mention:
            try:
                await message.channel.send(content=choice(mention_gifs))
                if message.author.id in self.bot.owner_ids:
                    await message.add_reaction("☠️")
                else:
                    await message.add_reaction("😡")
            except disnake.Forbidden:
                pass
            except disnake.HTTPException:
                pass
        elif self.bot.user.id in [user.id for user in message.mentions]:
            async with message.channel.typing():
                await asyncio.sleep(1)

        if "комар" in (message.content or "").lower():  # and randint(1, 10) == 1:
            await message.channel.send(content=choice(komaru_gifs))
        
        if "Say UwU" in message.content:
            try:
                await message.add_reaction("📸")
                await message.add_reaction("🤡")
            except disnake.Forbidden:
                pass
            except disnake.HTTPException:
                pass

    @commands.Cog.listener()
    async def on_stage_instance_create(self, stage_instance: StageInstance):
        stage: disnake.StageChannel = stage_instance.channel
        voice_client: disnake.VoiceProtocol = await stage.connect()
        await asyncio.sleep(600)
        await voice_client.disconnect(force=True)

    async def cog_load(self):
        logger.info("%s loaded", __name__)


def setup(client):
    """
    Internal disnake setup function
    """
    client.add_cog(Fun(client))
