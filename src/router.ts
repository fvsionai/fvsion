import { createRouter, createWebHistory } from "vue-router";
import { pinia } from "./stores";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: () => import("@/layouts/DashboardProseLayout.vue"),
      meta: {
        requiresNoAuth: true,
      },
      children: [
        {
          path: "/",
          name: "home",
          component: () => import("@/views/HomeView.vue"),
        },
        {
          path: "/about",
          name: "about",
          component: () => import("@/views/AboutView.vue"),
        },
        {
          path: "/support",
          name: "support",
          component: () => import("@/views/SupportView.vue"),
        },
        {
          path: "/privacy",
          name: "privacy",
          component: () => import("@/views/PrivacyView.vue"),
        },
        {
          path: "/terms",
          name: "terms",
          component: () => import("@/views/TermsView.vue"),
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
