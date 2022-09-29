import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
  createMemoryHistory
} from "vue-router";
import HomeView from "@/views/HomeView.vue"

console.log(import.meta.env);

const router = createRouter({
  history: import.meta.env.PROD ? createWebHashHistory('/') : createWebHistory(),
  routes: [
    {
      path: "/",
      component: HomeView,
    }
  ],
});

export default router;
