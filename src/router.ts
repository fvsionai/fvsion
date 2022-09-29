import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
 } from "vue-router";
import HomeView from "@/views/HomeView.vue"
import AboutView from "@/views/AboutView.vue"
import SupportView from "@/views/SupportView.vue"
import Img2ImgView from "@/views/Img2ImgView.vue"
import ProseLayout from "@/layouts/DashboardProseLayout.vue"
import Layout from "@/layouts/DashboardLayout.vue"

console.log(import.meta.env);

const router = createRouter({
  history: import.meta.env.PROD ? createWebHashHistory() : createWebHistory(),
  routes: [
    {
      path: "/",
      component: ProseLayout,
      meta: {
        requiresNoAuth: true,
      },
      children: [
        {
          path: "/",
          name: "home",
          component: HomeView,
        },
        {
          path: "/about",
          name: "about",
          component: AboutView,
        },
        {
          path: "/support",
          name: "support",
          component: SupportView,
        },
      ]
    },
    {
      path: "/",
      component: Layout,
      meta: {
        requiresNoAuth: true,
      },
      children: [
        {
          path: "/img2img",
          name: "img2img",
          component: Img2ImgView,
        },
      ],
    },
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

export default router;
