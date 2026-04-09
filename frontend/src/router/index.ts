import { createRouter, createWebHistory } from "vue-router"
import HomeView from "@/views/HomeView.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
      meta: { title: "Página Inicial" },
    },

    // ========== CÂMARA DOS DEPUTADOS ==========
    {
      path: "/camara/deputados",
      name: "deputados",
      component: () => import("@/views/camara/ListaView.vue"),
      meta: { title: "Deputados" },
    },
    {
      path: "/camara/deputados/:id",
      name: "deputado-detail",
      component: () => import("@/views/camara/DetalheView.vue"),
      meta: { title: "Detalhes do Deputado" },
    },
    {
      path: "/camara/despesas",
      name: "despesas-camara",
      component: () => import("@/views/camara/DespesasView.vue"),
      meta: { title: "Despesas da Câmara" },
    },
    {
      path: "/camara/emendas",
      name: "emendas-camara",
      component: () => import("@/views/camara/EmendasView.vue"),
      meta: { title: "Emendas da Câmara" },
    },
    {
      path: "/camara/comissoes",
      name: "comissoes-camara",
      component: () => import("@/views/camara/ComissoesView.vue"),
      meta: { title: "Comissões da Câmara" },
    },

    {
      path: "/camara/projetos-legislativos",
      name: "projetos-legislativos-camara",
      component: () => import("@/views/camara/ProjetosLegislativosView.vue"),
      meta: { title: "Projetos Legislativos" },
    },
    {
      path: "/camara/comparar",
      name: "comparar-deputados",
      component: () => import("@/views/camara/ComparacaoView.vue"),
      meta: { title: "Comparar Deputados" },
    },

    // ========== SENADO FEDERAL ==========
    {
      path: "/senado/senadores",
      name: "senadores",
      component: () => import("@/views/senado/ListaView.vue"),
      meta: { title: "Senadores" },
    },
    {
      path: "/senado/senadores/:id",
      name: "senador-detail",
      component: () => import("@/views/senado/DetalheView.vue"),
      meta: { title: "Detalhes do Senador" },
    },
    {
      path: "/senado/despesas",
      name: "despesas-senado",
      component: () => import("@/views/senado/DespesasView.vue"),
      meta: { title: "Despesas do Senado" },
    },
    {
      path: "/senado/emendas",
      name: "emendas-senado",
      component: () => import("@/views/senado/EmendasView.vue"),
      meta: { title: "Emendas do Senado" },
    },
    {
      path: "/senado/projetos-legislativos",
      name: "projetos-legislativos-senado",
      component: () => import("@/views/senado/ProjetosLegislativosView.vue"),
      meta: { title: "Projetos do Senado" },
    },
    {
      path: "/senado/comissoes",
      name: "comissoes-senado",
      component: () => import("@/views/senado/ComissoesView.vue"),
      meta: { title: "Comissões do Senado" },
    },

    {
      path: "/senado/comparar",
      name: "comparar-senadores",
      component: () => import("@/views/senado/ComparacaoView.vue"),
      meta: { title: "Comparar Senadores" },
    },

    // ========== OUTRAS PÁGINAS ==========
    {
      path: "/metodologia",
      name: "metodologia",
      component: () => import("@/views/MetodologiaView.vue"),
      meta: { title: "Metodologia" },
    },
    {
      path: "/rankings",
      redirect: "/camara/comissoes",
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

router.afterEach((to) => {
  const baseTitle = 'Fiscaliza Brasil'
  const pageTitle = to.meta.title as string
  
  if (pageTitle) {
    document.title = `${pageTitle} | ${baseTitle}`
  } else if (!document.title.includes(baseTitle)) {
    document.title = baseTitle
  }
})

export default router
