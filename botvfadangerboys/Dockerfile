# Обираємо офіційний lightweight-образ Python (версія 3.11) для архітектури ARM64 (Alpine Linux)
FROM arm64v8/python:3.11-alpine

# Встановлюємо змінні оточення для коректної роботи Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# (За потреби) Встановлюємо інструменти, які можуть знадобитися для компіляції пакетів
# Якщо у вашому проекті є пакети з нативною компіляцією (наприклад, some_package, що потребує gcc),
# розкоментуйте нижче та додайте необхідні залежності
# RUN apk update && apk add --no-cache gcc musl-dev

# Створюємо та переходимо в робочу директорію /app
WORKDIR /app

# Копіюємо файл залежностей у контейнер
COPY requirements.txt /app/requirements.txt

# Оновлюємо pip та встановлюємо залежності
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт у контейнер
COPY . /app

# Відкриваємо порт 8000 (документаційно)
EXPOSE 8000

# За замовчуванням запускаємо Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]