import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";

console.log(import.meta.env);

const router = createRouter({
  history: import.meta.env.PROD ? createWebHashHistory() : createWebHistory(),
  routes: [
    {
      path: "/",
      component: () => import("@/views/HomeView.vue"),
    },
    {
      path: "/img2img/",
      component: () => import("@/views/Img2ImgView.vue"),
    },
  ],
});

export default router;
