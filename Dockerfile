FROM python:3.12-slim

# Налаштування середовища для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Встановлюємо залежності для PostgreSQL та перевірки мережі
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо бібліотеки з вашого requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо проект та створюємо папки для даних кооперативу
COPY . .
RUN mkdir -p /app/staticfiles /app/media

# Додаємо скрипт запуску
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

# Запускаємо через Gunicorn для стабільності на AWS
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cooperative_manager.wsgi:application"]