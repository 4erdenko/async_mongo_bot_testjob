FROM python:3.11-alpine

# Устанавливаем зависимости
RUN apk add --no-cache mongodb-tools

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Комбинированная команда: сначала происходит импорт, затем запускается основной скрипт
CMD mongorestore --host mongo --db $DATABASE_NAME --collection $COLLECTION_NAME /app/database/resources/sample_collection.bson && python main.py
