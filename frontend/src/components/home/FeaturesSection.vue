<template>
  <section class="py-16 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <h2 class="text-2xl font-bold text-foreground mb-8">Explore os Dados</h2>

      <div class="grid gap-6 lg:grid-cols-2">
        <!-- Câmara dos Deputados -->
        <div class="bg-card rounded-lg border border-border p-6">
          <div class="flex items-center gap-3 mb-5">
            <Building2 class="h-5 w-5 text-primary" />
            <div>
              <h3 class="font-bold text-foreground">Câmara dos Deputados</h3>

            </div>
          </div>
          
          <div class="space-y-2">
            <router-link
              v-for="item in camaraItems"
              :key="item.href"
              :to="item.href"
              class="flex items-center justify-between p-3 rounded-md hover:bg-muted transition-colors"
            >
              <div class="flex items-center gap-3">
                <component :is="item.icon" class="h-4 w-4 text-muted-foreground" />
                <div>
                  <p class="text-sm font-medium text-foreground">{{ item.title }}</p>
                  <p class="text-xs text-muted-foreground">{{ item.description }}</p>
                </div>
              </div>
              <ArrowRight class="h-4 w-4 text-muted-foreground" />
            </router-link>
          </div>
        </div>

        <!-- Senado Federal -->
        <div class="bg-card rounded-lg border border-border p-6 relative">
          <div class="flex items-center gap-3 mb-5">
            <Landmark class="h-5 w-5 text-muted-foreground" />
            <div>
              <h3 class="font-bold text-foreground">Senado Federal</h3>
            </div>
          </div>
          
          <div class="space-y-2">
            <router-link
              v-for="item in senadoItems"
              :key="item.href"
              :to="item.href"
              class="flex items-center justify-between p-3 rounded-md hover:bg-muted transition-colors"
            >
              <div class="flex items-center gap-3">
                <component :is="item.icon" class="h-4 w-4 text-muted-foreground" />
                <div>
                  <p class="text-sm font-medium text-foreground">{{ item.title }}</p>
                  <p class="text-xs text-muted-foreground">{{ item.description }}</p>
                </div>
              </div>
              <ArrowRight class="h-4 w-4 text-muted-foreground" />
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { 
  Users, 
  Receipt, 
  Landmark, 
  Building2, 
  ArrowRight, 
  FileText, 
  GitCompare, 
  Store 
} from 'lucide-vue-next'
import { useSenadoresStore } from '@/stores/senadores'

const senadoresStore = useSenadoresStore()
onMounted(() => {
  senadoresStore.fetchEstatisticasGerais()
  senadoresStore.fetchEstatisticasSenadores()
})
const senadoresCount = computed(() => senadoresStore.senadorStats?.total_senadores ?? '--')

const camaraItems = [
  {
    title: "Deputados",
    description: "Perfis e atuação parlamentar",
    icon: Users,
    href: "/camara/deputados",
  },
  {
    title: "Despesas",
    description: "Gastos da cota parlamentar",
    icon: Receipt,
    href: "/camara/despesas",
  },
  {
    title: "Emendas",
    description: "Verbas destinadas pelos deputados",
    icon: Landmark,
    href: "/camara/emendas",
  },
  {
    title: "Projetos",
    description: "Projetos de lei e proposições",
    icon: FileText,
    href: "/camara/projetos-legislativos",
  },
  {
    title: "Comparar",
    description: "Compare atuação entre parlamentares",
    icon: GitCompare,
    href: "/camara/comparar",
  },
  {
    title: "Empresas",
    description: "Maiores fornecedores e recebedores",
    icon: Store,
    href: "/camara/empresas",
  },
]

const senadoItems = [
  {
    title: "Senadores",
    description: "Perfis e atuação no Senado",
    icon: Users,
    href: "/senado/senadores",
  },
  {
    title: "Despesas",
    description: "Gastos e reembolsos do Senado",
    icon: Receipt,
    href: "/senado/despesas",
  },
  {
    title: "Emendas",
    description: "Emendas dos senadores",
    icon: Landmark,
    href: "/senado/emendas",
  },
  {
    title: "Projetos",
    description: "Matérias e projetos legislativos",
    icon: FileText,
    href: "/senado/projetos-legislativos",
  },
  {
    title: "Comparar",
    description: "Análise comparativa de senadores",
    icon: GitCompare,
    href: "/senado/comparar",
  },
]
</script>
