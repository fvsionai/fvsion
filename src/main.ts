import { createApp } from "vue";
import App from "./App.vue";
import "./style.css";
import router from "./router";
import { isDev, pinia } from "@/stores";
import { createHead } from "@vueuse/head";
import VWave from "v-wave";
import axios from "axios";
import VueAxios from "vue-axios";
import { plugin, defaultConfig } from "@formkit/vue";

const app = createApp(App);
const head = createHead();

app.use(router).use(pinia).use(head).use(VWave).use(plugin, defaultConfig);
app.use(VueAxios, axios).provide("axios", app.config.globalProperties.axios);

app.mount("#app").$nextTick(() => {
  postMessage({ payload: "removeLoading" }, "*");
});
