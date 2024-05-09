from disnake.ext import commands
import disnake
import os
import io
import imageio
import numpy as np
from PIL import Image
import logging


logging.basicConfig(level=logging.INFO)


# class ImgGif(commands.Bot):

#     @classmethod
#     def create(cls) -> "ImgGif":
#         """Create and return an instance of a Bot."""
#         _intents = disnake.Intents.none()
#         _intents.members = True
#         _intents.bans = True
#         _intents.dm_messages = True  # ????
#         _intents.guilds = True

#         return cls(
#             owner_ids=[973169875419795488, 986355526948515870],
#             intents=_intents,
#             command_prefix=commands.when_mentioned,
#             allowed_mentions=disnake.AllowedMentions(everyone=False),
#             activity=disnake.Game(name="Делаю гифки"),
#         )

#     async def on_ready(self):
#         print(f"Logged in as {self.user}")
# bot = ImgGif.create()


bot = commands.Bot(
    command_prefix="/",
    intents=disnake.Intents.all(),
    activity=disnake.Game(name="Делаю гифки"),
    owner_ids=[973169875419795488, 986355526948515870],
)


# 12321


@bot.slash_command(name="съебал", description="Команда выключает бота")
async def check_permissions(interaction):
    if (
        interaction.author.id == 973169875419795488
        or interaction.author.id == 986355526948515870
    ):
        await interaction.response.send_message(
            embed=disnake.Embed(
                description="Сеанс завершён...", colour=disnake.Color.green()
            )
        )
        await bot.close()
    else:
        await interaction.response.send_message(
            embed=disnake.Embed(description="Нет прав.", colour=disnake.Color.red())
        )


@bot.slash_command(name="пинг", description="Проверка не сдох ли бот")
async def ping(interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(
        embed=disnake.Embed(
            description=f"Пинг {latency}ms", colour=disnake.Color.green()
        )
    )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


async def on_message(message):
    if message.author == bot.user:
        return
    print(message.content)
    if isinstance(message.channel, disnake.DMChannel) and message.attachments:
        # Проверяем, что сообщение отправлено в личные сообщения и содержит вложения
        attachment = message.attachments[0]
        if attachment.content_type.startswith("image"):
            # Если вложение является изображением
            await ask_conversion_type(attachment, message)

    await bot.process_commands(message)


async def ask_conversion_type(attachment, message):
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
                    disnake.ui.Button(style=disnake.ButtonStyle.secondary, label="Мем")
                ),
            ],
        )

        # Ожидаем нажатия кнопки
        interaction = await bot.wait_for(
            "button_click", check=lambda i: i.user == message.author
        )

        # Обрабатываем нажатие кнопки
        if interaction.component.label == "Обычный":
            await process_image(attachment, message)
        elif interaction.component.label == "Мем":
            await process_mem_image(attachment, message)

    except Exception as e:
        await message.reply(f"Ошибка: {e}")


async def process_image(attachment, message):
    try:
        # Скачиваем изображение
        image_bytes = await attachment.read()
        # Создаем объект BytesIO для работы с байтами
        image_stream = io.BytesIO(image_bytes)

        # Читаем изображение с помощью imageio
        images = [imageio.imread(image_stream)]

        # Создаем gif изображение
        gif_bytes = io.BytesIO()
        imageio.mimsave(gif_bytes, images, format="GIF", duration=1.0)

        # Перемещаем указатель в начало файла для отправки
        gif_bytes.seek(0)

        # Отправляем gif в ответ на сообщение
        await message.reply(file=disnake.File(gif_bytes, filename="converted.gif"))

        # Отправляем гифку в определенный канал Discord
        channel_log = bot.get_channel(
            1237789824530776065
        )  # здесь айди канала куда будет отправляться сообщение
        user_display_name = message.author.display_name
        soderg = f"{user_display_name} создал гифку:"
        gif_bytes.seek(0)
        await channel_log.send(
            soderg, file=disnake.File(gif_bytes, filename="converted.gif")
        )

    except Exception as e:
        await message.reply(f"Ошибка при конвертации изображения: {e}")


async def process_mem_image(attachment, message):
    try:
        # Скачиваем изображение
        image_bytes = await attachment.read()
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
        await message.reply(file=disnake.File(gif_bytes, filename="converted.gif"))

        # Отправляем гифку в определенный канал Discord
        channel_log = bot.get_channel(
            1237789824530776065
        )  # здесь айди канала куда будет отправляться сообщение
        user_display_name = message.author.display_name
        soderg = f"{user_display_name} создал гифку:"
        gif_bytes.seek(0)
        await channel_log.send(
            soderg, file=disnake.File(gif_bytes, filename="converted.gif")
        )

    except Exception as e:
        await message.reply(f"Ошибка при обработке изображения: {e}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("")
