import { createApp } from "vue";
import App from "./App.vue";
import "./index.css";
import router from "./router"; // Импортируйте маршрутизатор
import { VueTelegramPlugin } from "vue-tg";

const app = createApp(App); // Создайте экземпляр приложения Vue
app.use(router);
app.use(VueTelegramPlugin);
app.provide("BASE_SITE", "https://vue3fastapi-yakvenalex.amvera.io");
app.mount("#app");
