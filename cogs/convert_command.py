# import io
# from PIL import Image
# import imageio
import disnake
from disnake.ext import commands
from config import INLESS_GUILD, INLESS_CHANNEL
from methods.methods import process_image, process_mem_image, log
import logging

logger = logging.getLogger(__name__)


class ImageConverterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="gif", description="Создать гиф на сервере.")
    async def gif(
        self,
        inter: disnake.ApplicationCommandInteraction,
        image_entr: disnake.Attachment,
    ):
        if inter.author == self.bot.user:
            return
        if inter.guild_id == INLESS_GUILD:
            if inter.channel_id != INLESS_CHANNEL:
                await inter.response.send_message(
                    f"Команду можно использовать только в канале https://discord.com/channels/1083650721959919636/1263555318701625426 (только в дискорд сервере INLESS)",
                    ephemeral=True,
                )
                return

        if image_entr.content_type and image_entr.content_type.startswith("image"):
            # Если вложение является изображением
            await self.ask_conversion_type(image_entr, inter)

    async def ask_conversion_type(self, image_entr, inter):
        try:

            await inter.response.send_message(
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
                "button_click", check=lambda i: i.user == inter.author
            )

            if interaction.component.label == "Обычный":

                img = await process_image(image_entr)
                await log(self.bot, inter, img)

                img.seek(0)

                await inter.edit_original_message(
                    f"Ваша гифка <@{inter.author.id}>:",
                    file=disnake.File(img, filename="JustGM.gif"),
                    components=[],
                )
            elif interaction.component.label == "Мем":

                img = await process_mem_image(image_entr)
                await log(self.bot, inter, img)

                img.seek(0)

                await inter.edit_original_message(
                    f"Ваша гифка <@{inter.author.id}>:",
                    file=disnake.File(img, filename="JustGM.gif"),
                    components=[],
                )
        except Exception as e:
            await inter.edit_original_message(f"Ошибка: {e}", components=[])
            logger.error(f"Error convert_command: {e}")

    async def cog_load(self):
        logger.info("%s loaded", __name__)


def setup(bot):
    bot.add_cog(ImageConverterCommand(bot))
