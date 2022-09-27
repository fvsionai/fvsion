import {
  createRouter,
  createWebHistory,
  createWebHashHistory,
} from "vue-router";

const router = createRouter({
  history: import.meta.env.IS_ELECTRON
    ? createWebHashHistory()
    : createWebHistory(),
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
    {
      path: "/",
      component: () => import("@/layouts/DashboardLayout.vue"),
      meta: {
        requiresNoAuth: true,
      },
      children: [
        {
          path: "/img2img",
          name: "img2img",
          component: () => import("@/views/Img2ImgView.vue"),
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
