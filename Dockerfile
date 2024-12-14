# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Обновляем pip
RUN pip install --upgrade pip

# Клонируем репозиторий
RUN git clone https://github.com/StephanBroYT/JUST-GM.git .

# Устанавливаем зависимости вручную
RUN pip install --no-cache-dir disnake
RUN pip install --no-cache-dir imageio
RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir pillow
RUN pip install --no-cache-dir pynacl


# Указываем переменную окружения для Python
ENV PYTHONUNBUFFERED=1
ENV TOKEN=ГОЙДА

# Указываем команду запуска бота
CMD ["python", "main.py"]