# Використовуємо Node.js з підтримкою ARM64
FROM arm64v8/node:18-alpine

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо package.json та package-lock.json
COPY package*.json ./

# Встановлюємо залежності
RUN npm install

# Копіюємо проект
COPY . .

# Команда за замовчуванням (перезаписується в docker-compose)
CMD ["npm", "run", "serve"]