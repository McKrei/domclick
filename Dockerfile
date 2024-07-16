# Используем официальный образ Python в качестве базового
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения в рабочую директорию
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY real_estate_data.csv real_estate_data.csv

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт для доступа к приложению
EXPOSE 8050

# Устанавливаем команду запуска по умолчанию
CMD ["python", "app.py"]
