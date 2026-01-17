<template>
  <section class="py-16">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Destaques</h2>
        <p class="mt-2 text-muted-foreground">Fatos importantes sobre os gastos e atuação parlamentar</p>
      </div>

      <div class="grid gap-4 md:grid-cols-2">
        <div
          v-for="(fact, index) in facts"
          :key="index"
          :class="[
            'rounded-lg border bg-card p-6 animate-fade-in-up',
            typeStyles[fact.type]
          ]"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="flex gap-4">
            <component :is="fact.icon" :class="`h-6 w-6 flex-shrink-0 ${iconStyles[fact.type]}`" />
            <div>
              <h3 class="font-semibold text-foreground">{{ fact.title }}</h3>
              <p class="mt-1 text-sm text-muted-foreground">{{ fact.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { AlertTriangle, CheckCircle, Info, TrendingUp } from 'lucide-vue-next'

const facts = [
  {
    icon: AlertTriangle,
    title: "113 deputados recebem auxílio-moradia",
    description: "R$ 4.253 por mês cada, mesmo possuindo imóvel próprio em Brasília",
    type: "warning" as const,
  },
  {
    icon: TrendingUp,
    title: "Bloco de direita gasta 2x mais",
    description: "R$ 309 milhões contra R$ 149 milhões do bloco de esquerda",
    type: "info" as const,
  },
  {
    icon: Info,
    title: "TAM é a empresa que mais recebe",
    description: "R$ 59 milhões em passagens aéreas de deputados federais",
    type: "neutral" as const,
  },
  {
    icon: CheckCircle,
    title: "Saúde lidera em emendas",
    description: "25,8% das emendas são destinadas à área de saúde",
    type: "success" as const,
  },
]

const typeStyles: Record<string, string> = {
  warning: "border-l-4 border-l-chart-2 bg-chart-2/5",
  info: "border-l-4 border-l-accent bg-accent/5",
  neutral: "border-l-4 border-l-muted-foreground bg-muted/50",
  success: "border-l-4 border-l-primary bg-primary/5",
}

const iconStyles: Record<string, string> = {
  warning: "text-chart-2",
  info: "text-accent",
  neutral: "text-muted-foreground",
  success: "text-primary",
}
</script>
