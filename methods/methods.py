import io
from PIL import Image
import disnake
from disnake.ext import commands
from config import LOG_CHANNEL
import logging
from config import client

logger = logging.getLogger(__name__)


async def process_image(attachment):
    """
    ЧТО ЭТО ЗА 💀💀💀
    """
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

        return gif_bytes
    except Exception as e:
        print(f"Error process_image: {e}")
        logger.error(f"Error process_image: {e}")


async def process_mem_image(attachment):
    """
    ЧТО ЭТО ЗА 💀💀💀
    """
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
        return gif_bytes
    except Exception as e:
        print(f"Error process_mem_image: {e}")
        logger.error(f"Error process_mem_image: {e}")


async def log(bot, message, img):
    try:
        channel_log = bot.get_channel(LOG_CHANNEL)
        img.seek(0)

        await channel_log.send(
            f"<@{message.author.id}> ({message.author.name}) создал гифку:",
            file=disnake.File(img, filename="JustGM.gif"),
        )
    except Exception as e:
        print(f"Log error: {e}")
        logger.error(f"Log error: {e}")


async def ask(
    question: str,
    ai: str,
    role: str,
):
    global client

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                    # Set an optional system message. This sets the behavior of the
                    # assistant and can be used to provide specific instructions for
                    # how it should behave throughout the conversation.
                    {
                        "role": "system",
                        "content": role
                    },
                    # Set a user message for the assistant to respond to.
                    {
                        "role": "user",
                        "content": question,
                    }
                ],
            # model="llama3-8b-8192",
            # model="llama-3.3-70b-versatile",
            model=ai,


            stream=False,
        )

        logger.info(f"ROLE:{role}| QUESTION:{question}| API RESPONSE: {chat_completion}")
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f'AI ask error: {e}')
        return "Error"
