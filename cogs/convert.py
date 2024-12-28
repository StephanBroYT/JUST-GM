import disnake
from disnake.ext import commands
from methods.methods import process_image, process_mem_image, log
# import io
# from PIL import Image
import logging

logger = logging.getLogger(__name__)


class ImageConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, disnake.DMChannel) and message.attachments:

            attachment = message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith("image"):

                await self.ask_conversion_type(attachment, message)

    async def ask_conversion_type(self, attachment, message):
        try:

            msg = await message.reply(
                "Выберите тип:",
                components=[
                    disnake.ui.ActionRow(
                        disnake.ui.Button(
                            style=disnake.ButtonStyle.primary, label="Обычный"
                        )
                    ),
                    disnake.ui.ActionRow(
                        disnake.ui.Button(
                            style=disnake.ButtonStyle.secondary, label="Мем"
                        )
                    ),
                ],
            )

            interaction = await self.bot.wait_for(
                "button_click", check=lambda i: i.user == message.author
            )

            if interaction.component.label == "Обычный":
                img = await process_image(attachment)
                await log(self.bot, message, img)

                img.seek(0)

                await msg.edit(
                    f"Ваша гифка <@{message.author.id}>:",
                    file=disnake.File(img, filename="JustGM.gif"),
                    components=[],
                )
            elif interaction.component.label == "Мем":
                img = await process_mem_image(attachment)
                await log(self.bot, message, img)

                img.seek(0)

                await msg.edit(
                    f"Ваша гифка <@{message.author.id}>:",
                    file=disnake.File(img, filename="JustGM.gif"),
                    components=[],
                )
        except Exception as e:
            await message.reply(f"Ошибка: {e}")
            logger.error(f"Error convert: {e}")

    async def cog_load(self):
        logger.info("%s loaded", __name__)


def setup(bot):
    bot.add_cog(ImageConverter(bot))
