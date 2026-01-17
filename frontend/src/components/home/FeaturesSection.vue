<template>
  <section class="py-16 bg-muted/30">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Explore os Dados</h2>
        <p class="mt-2 text-muted-foreground max-w-2xl mx-auto">
          Navegue por diferentes categorias de informações sobre a atuação dos deputados federais
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <BaseCard
          v-for="(feature, index) in features"
          :key="feature.title"
          hover
          class="animate-fade-in-up"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <template #header>
            <div :class="`inline-flex p-3 rounded-xl ${feature.bgColor} w-fit mb-2`">
              <component :is="feature.icon" :class="`h-6 w-6 ${feature.color}`" />
            </div>
            <h3 class="text-lg font-semibold text-foreground">{{ feature.title }}</h3>
            <p class="text-sm text-muted-foreground">{{ feature.description }}</p>
          </template>
          <template #footer>
            <router-link :to="feature.href" class="inline-flex items-center text-primary hover:underline group">
              Explorar
              <ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
            </router-link>
          </template>
        </BaseCard>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Users, Receipt, Landmark, Building2, ArrowRight } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'

const features = [
  {
    title: "Perfis dos Deputados",
    description: "Acesse informações detalhadas de todos os 513 deputados federais, incluindo partido, estado e contatos.",
    icon: Users,
    href: "/deputados",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    title: "Gastos e Despesas",
    description: "Monitore os gastos da cota parlamentar por categoria, partido e bloco ideológico.",
    icon: Receipt,
    href: "/despesas",
    color: "text-chart-2",
    bgColor: "bg-chart-2/10",
  },
  {
    title: "Emendas Parlamentares",
    description: "Acompanhe a distribuição de emendas parlamentares por área e deputado.",
    icon: Landmark,
    href: "/emendas",
    color: "text-accent",
    bgColor: "bg-accent/10",
  },
  {
    title: "Análises Detalhadas",
    description: "Visualizações baseadas em dados reais processados",
    icon: Building2,
    href: "/rankings",
    color: "text-chart-4",
    bgColor: "bg-chart-4/10",
  },
]
</script>
