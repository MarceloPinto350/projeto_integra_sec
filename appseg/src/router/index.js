import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import TipoAplicacao from "@/views/TipoAplicacao.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
    {
        path: "/tiposaplicacao",
        name: "TipoAplicacao",
        component: TipoAplicacao,
      },
  ],
});

export default router;
