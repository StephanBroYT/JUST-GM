import io
from PIL import Image
import disnake
from disnake.ext import commands

class ImageConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, disnake.DMChannel) and message.attachments:
            # Проверяем, что сообщение отправлено в личные сообщения и содержит вложения
            attachment = message.attachments[0]
            if attachment.content_type and attachment.content_type.startswith("image"):
                # Если вложение является изображением
                await self.ask_conversion_type(attachment, message)

    async def ask_conversion_type(self, attachment, message):
        try:
            # Отправляем сообщение с кнопками
            await message.reply(
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
                "button_click", check=lambda i: i.user == message.author
            )
            # Обрабатываем нажатие кнопки
            if interaction.component.label == "Обычный":
                await self.process_image(attachment, message)
            elif interaction.component.label == "Мем":
                await self.process_mem_image(attachment, message)
        except Exception as e:
            await message.reply(f"Ошибка: {e}")

    async def process_image(self, attachment, message):
        try:
            # Скачиваем изображение
            image_bytes = await attachment.read()
            # Создаем объект BytesIO для работы с байтами
            image_stream = io.BytesIO(image_bytes)
            # Читаем изображение с помощью Pillow в формате RGBA
            image = Image.open(image_stream).convert("RGBA")
            # Создаем gif изображение
            gif_bytes = io.BytesIO()
            image.save(gif_bytes, format="GIF", save_all=True, optimize=False)
            # Перемещаем указатель в начало файла для отправки
            gif_bytes.seek(0)
            # Отправляем gif в ответ на сообщение
            await message.reply(f"Ваша гифка <@{message.author.id}>:", file=disnake.File(gif_bytes, filename="converted.gif"), components=[])
            # Отправляем гифку в определенный канал Discord
            channel_log = self.bot.get_channel(
                1237789824530776065  # здесь айди канала куда будет отправляться сообщение
            )
            gif_bytes.seek(0)
            await channel_log.send(
                f"{message.author.name}, <@{message.author.id}> создал гифку:", file=disnake.File(gif_bytes, filename="JustGM.gif")
            )
        except Exception as e:
            await message.reply(f"Ошибка при конвертации изображения: {e}", components=[])

    async def process_mem_image(self, attachment, message):
        try:
            # Скачиваем изображение
            image_bytes = await attachment.read()
            # Создаем объект BytesIO для работы с байтами
            image_stream = io.BytesIO(image_bytes)
            # Открываем основное изображение с прозрачностью в формате RGBA
            main_image = Image.open(image_stream).convert("RGBA")
            # Получаем размеры основного изображения
            main_width, main_height = main_image.size
            # Открываем файл bro.png с прозрачностью в формате RGBA
            bro_image = Image.open("bro.png").convert("RGBA")
            # Изменяем размер "bro.png" таким образом, чтобы его ширина соответствовала ширине основного изображения
            bro_image_resized = bro_image.resize(
                (main_width, int(main_width / bro_image.width * bro_image.height))
            )
            # Наложение изображения bro на main
            main_image.paste(bro_image_resized, (0, 0), bro_image_resized)
            # Создаем gif изображение
            gif_bytes = io.BytesIO()
            main_image.save(gif_bytes, format="GIF", save_all=True, optimize=False)
            # Перемещаем указатель в начало файла для отправки
            gif_bytes.seek(0)
            # Отправляем gif в ответ на сообщение
            await message.reply(f"Ваша гифка {message.author.name}:", file=disnake.File(gif_bytes, filename="JustGM.gif"), components=[])
            # Отправляем гифку в определенный канал Discord
            channel_log = self.bot.get_channel(
                1237789824530776065  # здесь айди канала куда будет отправляться сообщение
            )
            gif_bytes.seek(0)
            await channel_log.send(
                f"{message.author.name}, <@{message.author.id}> создал гифку:", file=disnake.File(gif_bytes, filename="JustGM.gif")
            )
        except Exception as e:
            await message.reply(f"Ошибка при обработке изображения: {e}")

def setup(bot):
    bot.add_cog(ImageConverter(bot))
