import { createRouter, createWebHistory } from "vue-router"
import HomeView from "@/views/HomeView.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/deputados",
      name: "deputados",
      component: () => import("@/views/DeputadosView.vue"),
    },
    {
      path: "/deputados/:id",
      name: "deputado-detail",
      component: () => import("@/views/DeputadoDetailView.vue"),
    },
    {
      path: "/despesas",
      name: "despesas",
      component: () => import("@/views/DespesasView.vue"),
    },
    {
      path: "/emendas",
      name: "emendas",
      component: () => import("@/views/EmendasView.vue"),
    },
    {
      path: "/metodologia",
      name: "metodologia",
      component: () => import("@/views/MetodologiaView.vue"),
    },
    {
      path: "/rankings",
      name: "rankings",
      component: () => import("@/views/RankingsView.vue"),
    },


  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
