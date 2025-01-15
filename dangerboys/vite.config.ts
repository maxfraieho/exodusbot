import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";

export default defineConfig({
  plugins: [vue()],
  css: {
    postcss: {
      plugins: [tailwindcss, autoprefixer], // Підключаємо TailwindCSS та Autoprefixer
    },
  },
  server: {
    host: "0.0.0.0", // Дозволяє доступ ззовні контейнера
    port: 3000, // Задаємо порт для dev-сервера
    watch: {
      usePolling: true, // Необхідно для стабільної роботи hot-reload у Docker
    },
  },
  build: {
    outDir: "dist", // Директорія для згенерованих файлів
    emptyOutDir: true, // Очищає dist перед новою збіркою
  },
});