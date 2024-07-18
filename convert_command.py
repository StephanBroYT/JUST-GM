import io
from PIL import Image
import imageio
import disnake
from disnake.ext import commands

class ImageConverterCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="gif", description="Создать гиф на сервере.")
    async def send_ticket_button(self, inter: disnake.ApplicationCommandInteraction, image_entr: disnake.Attachment):
        if inter.author == self.bot.user:
            return
        if inter.guild_id == 1083650721959919636:
            if inter.channel_id != 1263555318701625426:
                await inter.response.send_message(f'Команду можно использовать только в канале https://discord.com/channels/1083650721959919636/1263555318701625426 (только в дискорд сервере INLESS)', ephemeral=True)
                return
        
        if image_entr.content_type and image_entr.content_type.startswith("image"):
            # Если вложение является изображением
            await self.ask_conversion_type(image_entr, inter)
            
        
    async def ask_conversion_type(self, image_entr, inter):
        try:
            # Отправляем сообщение с кнопками
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
            # Ожидаем нажатия кнопки
            interaction = await self.bot.wait_for(
                "button_click", check=lambda i: i.user == inter.author
            )
            # Обрабатываем нажатие кнопки
            if interaction.component.label == "Обычный":
                await self.process_image(image_entr, inter)
            elif interaction.component.label == "Мем":
                await self.process_mem_image(image_entr, inter)
        except Exception as e:
            await inter.reply(f"Ошибка: {e}")

    async def process_image(self, image_entr, inter):
        try:
            # Скачиваем изображение
            image_bytes = await image_entr.read()
            # Создаем объект BytesIO для работы с байтами
            image_stream = io.BytesIO(image_bytes)
            # Читаем изображение с помощью imageio
            images = [imageio.imread(image_stream)]
            # Создаем gif изображение
            gif_bytes = io.BytesIO()
            imageio.mimsave(gif_bytes, images, format="GIF")
            # Перемещаем указатель в начало файла для отправки
            gif_bytes.seek(0)
            # Отправляем gif в ответ на сообщение
            await inter.edit_original_message(f"Ваша гифка <@{inter.author.id}>: ", file=disnake.File(gif_bytes, filename="converted.gif"), components=[])
            # Отправляем гифку в определенный канал Discord
            channel_log = self.bot.get_channel(
                1237789824530776065
            )  # здесь айди канала куда будет отправляться сообщение
            soderg = f"{inter.author.name} , <@{inter.author.id}> создал гифку:"
            gif_bytes.seek(0)
            await channel_log.send(
                soderg, file=disnake.File(gif_bytes, filename="JustGM.gif")
            )
        except Exception as e:
            await inter.edit_original_message(f"Ошибка при конвертации изображения: {e}", components=[])

    async def process_mem_image(self, image_entr, inter):
        try:
            # Скачиваем изображение
            image_bytes = await image_entr.read()
            # Создаем объект BytesIO для работы с байтами
            image_stream = io.BytesIO(image_bytes)
            # Открываем основное изображение с прозрачностью
            main_image = Image.open(image_stream).convert("RGBA")
            # Получаем размеры основного изображения
            main_width, main_height = main_image.size
            # Открываем файл bro.png с прозрачностью
            bro_image = Image.open("bro.png").convert("RGBA")
            # Изменяем размер "bro.png" таким образом, чтобы его ширина соответствовала ширине основного изображения
            bro_image_resized = bro_image.resize(
                (main_width, int(main_width / bro_image.width * bro_image.height))
            )
            # Наложение изображения bro на main
            main_image.paste(bro_image_resized, (0, 0), bro_image_resized)
            # Создаем gif изображение
            gif_bytes = io.BytesIO()
            main_image.save(gif_bytes, format="GIF")
            # Перемещаем указатель в начало файла для отправки
            gif_bytes.seek(0)
            # Отправляем gif в ответ на сообщение
            await inter.edit_original_message(f"Ваша гифка <@{inter.author.id}>: ",file=disnake.File(gif_bytes, filename="converted.gif"), components = [])
            # Отправляем гифку в определенный канал Discord
            channel_log = self.bot.get_channel(
                1237789824530776065
            )  # здесь айди канала куда будет отправляться сообщение
            soderg = f"{inter.author.name} , <@{inter.author.id}> создал гифку:"
            gif_bytes.seek(0)
            await channel_log.send(
                soderg, file=disnake.File(gif_bytes, filename="JustGM.gif")
            )
        except Exception as e:
            await inter.edit_original_message(f"Ошибка при обработке изображения: {e}", components=[])

def setup(bot):
    bot.add_cog(ImageConverterCommand(bot))
