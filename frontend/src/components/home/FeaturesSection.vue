<template>
  <section class="py-16 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Explore os Dados</h2>
        <p class="mt-2 text-muted-foreground max-w-2xl mx-auto">
          Navegue por diferentes categorias de informações sobre a atuação dos parlamentares
        </p>
      </div>

      <!-- Duas Casas Legislativas -->
      <div class="grid gap-8 lg:grid-cols-2 max-w-6xl mx-auto">
        
        <!-- Câmara dos Deputados -->
        <BaseCard class="relative overflow-hidden">
          <template #header>
            <div class="flex items-center gap-3 mb-4">
              <div class="p-3 rounded-xl bg-primary/10">
                <Building2 class="h-6 w-6 text-primary" />
              </div>
              <div>
                <h3 class="text-xl font-bold text-foreground">Câmara dos Deputados</h3>
                <p class="text-sm text-muted-foreground">513 Deputados Federais</p>
              </div>
            </div>
          </template>
          
          <div class="grid gap-3">
            <router-link
              v-for="item in camaraItems"
              :key="item.href"
              :to="item.href"
              class="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-muted/50 transition-colors group"
            >
              <div class="flex items-center gap-3">
                <div :class="`p-2 rounded-lg ${item.bgColor}`">
                  <component :is="item.icon" :class="`h-4 w-4 ${item.color}`" />
                </div>
                <div>
                  <p class="font-medium text-foreground">{{ item.title }}</p>
                  <p class="text-xs text-muted-foreground">{{ item.description }}</p>
                </div>
              </div>
              <ArrowRight class="h-4 w-4 text-muted-foreground group-hover:text-primary group-hover:translate-x-1 transition-all" />
            </router-link>
          </div>
        </BaseCard>

        <!-- Senado Federal -->
        <BaseCard class="relative overflow-hidden">
          <template #header>
            <div class="flex items-center gap-3 mb-4">
              <div class="p-3 rounded-xl bg-purple-500/10">
                <Landmark class="h-6 w-6 text-purple-500" />
              </div>
              <div>
                <h3 class="text-xl font-bold text-foreground">Senado Federal</h3>
                <p class="text-sm text-muted-foreground">81 Senadores</p>
              </div>
            </div>
          </template>
          
          <div class="grid gap-3">
            <router-link
              v-for="item in senadoItems"
              :key="item.href"
              :to="item.href"
              class="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-muted/50 transition-colors group"
            >
              <div class="flex items-center gap-3">
                <div :class="`p-2 rounded-lg ${item.bgColor}`">
                  <component :is="item.icon" :class="`h-4 w-4 ${item.color}`" />
                </div>
                <div>
                  <p class="font-medium text-foreground">{{ item.title }}</p>
                  <p class="text-xs text-muted-foreground">{{ item.description }}</p>
                </div>
              </div>
              <ArrowRight class="h-4 w-4 text-muted-foreground group-hover:text-purple-500 group-hover:translate-x-1 transition-all" />
            </router-link>
          </div>
          
          <!-- Badge Em Breve -->
          <div class="absolute top-4 right-4">
            <span class="px-2 py-1 text-xs font-medium bg-purple-500/10 text-purple-500 rounded-full">
              Em breve
            </span>
          </div>
        </BaseCard>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Users, Receipt, Landmark, Building2, ArrowRight } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'

const camaraItems = [
  {
    title: "Deputados",
    description: "Perfis de todos os deputados federais",
    icon: Users,
    href: "/camara/deputados",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    title: "Despesas",
    description: "Gastos da cota parlamentar",
    icon: Receipt,
    href: "/camara/despesas",
    color: "text-chart-2",
    bgColor: "bg-chart-2/10",
  },
  {
    title: "Emendas",
    description: "Emendas parlamentares",
    icon: Landmark,
    href: "/camara/emendas",
    color: "text-accent",
    bgColor: "bg-accent/10",
  },
]

const senadoItems = [
  {
    title: "Senadores",
    description: "Perfis dos senadores da República",
    icon: Users,
    href: "/senado/senadores",
    color: "text-purple-500",
    bgColor: "bg-purple-500/10",
  },
  {
    title: "Despesas",
    description: "Gastos do Senado Federal",
    icon: Receipt,
    href: "/senado/despesas",
    color: "text-purple-400",
    bgColor: "bg-purple-400/10",
  },
  {
    title: "Emendas",
    description: "Emendas dos senadores",
    icon: Landmark,
    href: "/senado/emendas",
    color: "text-purple-600",
    bgColor: "bg-purple-600/10",
  },
]
</script>
