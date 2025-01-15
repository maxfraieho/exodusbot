#!/bin/bash

# Назва віртуального середовища
VENV_NAME="venv"

# Перевіряємо, чи вже існує віртуальне середовище
if [ ! -d "$VENV_NAME" ]; then
    echo "Створюємо віртуальне середовище..."
    python3 -m venv $VENV_NAME
else
    echo "Віртуальне середовище вже існує. Пропускаємо створення."
fi

# Активуємо віртуальне середовище
echo "Активуємо віртуальне середовище..."
source $VENV_NAME/bin/activate

# Оновлюємо pip до останньої версії
echo "Оновлюємо pip до останньої версії..."
pip install --upgrade pip

# Встановлюємо залежності з файлу requirements.txt
echo "Встановлюємо залежності з файлу requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Файл requirements.txt не знайдено! Будь ласка, перевірте наявність файлу."
    deactivate
    exit 1
fi

# Запускаємо сервер (Uvicorn) для локального тестування
echo "Запускаємо сервер Uvicorn на локальному хості..."
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Деактивуємо віртуальне середовище (опціонально, якщо потрібно після виконання)
echo "Завершуємо роботу..."
deactivate