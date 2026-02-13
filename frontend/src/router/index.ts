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

    // ========== CÂMARA DOS DEPUTADOS ==========
    {
      path: "/camara/deputados",
      name: "deputados",
      component: () => import("@/views/camara/DeputadosView.vue"),
    },
    {
      path: "/camara/deputados/:id",
      name: "deputado-detail",
      component: () => import("@/views/camara/DeputadoDetailView.vue"),
    },
    {
      path: "/camara/despesas",
      name: "despesas-camara",
      component: () => import("@/views/camara/DespesasCamaraView.vue"),
    },
    {
      path: "/camara/emendas",
      name: "emendas-camara",
      component: () => import("@/views/camara/EmendasCamaraView.vue"),
    },
    {
      path: "/camara/empresas",
      name: "empresas-camara",
      component: () => import("@/views/camara/EmpresasView.vue"),
    },
    {
      path: "/camara/proposicoes",
      name: "proposicoes-camara",
      component: () => import("@/views/camara/ProposicoesCamaraView.vue"),
    },

    // ========== SENADO FEDERAL ==========
    {
      path: "/senado/senadores",
      name: "senadores",
      component: () => import("@/views/senado/SenadoresView.vue"),
    },
    {
      path: "/senado/despesas",
      name: "despesas-senado",
      component: () => import("@/views/senado/DespesasSenadoView.vue"),
    },
    {
      path: "/senado/emendas",
      name: "emendas-senado",
      component: () => import("@/views/senado/EmendasSenadoView.vue"),
    },

    // ========== OUTRAS PÁGINAS ==========
    {
      path: "/metodologia",
      name: "metodologia",
      component: () => import("@/views/MetodologiaView.vue"),
    },
    {
      path: "/rankings",
      redirect: "/camara/empresas",
    },

    // ========== REDIRECTS (compatibilidade) ==========
    {
      path: "/deputados",
      redirect: "/camara/deputados",
    },
    {
      path: "/deputados/:id",
      redirect: to => `/camara/deputados/${to.params.id}`,
    },
    {
      path: "/despesas",
      redirect: "/camara/despesas",
    },
    {
      path: "/emendas",
      redirect: "/camara/emendas",
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
