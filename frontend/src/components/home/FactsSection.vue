<template>
  <section class="py-16">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <h2 class="text-2xl font-bold text-foreground mb-6">Destaques</h2>

      <div class="grid gap-4 md:grid-cols-3">
        <div
          v-for="(fact, index) in facts"
          :key="index"
          class="rounded-lg border border-border bg-card p-5"
        >
          <h3 class="font-semibold text-foreground text-sm">{{ fact.title }}</h3>
          <p class="mt-2 text-sm text-muted-foreground">{{ fact.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const facts = [
  {
    title: "113 deputados recebem auxílio-moradia",
    description: "R$ 4.253 por mês cada, mesmo possuindo imóvel próprio em Brasília",
  },
  {
    title: "Bloco de direita gasta 2x mais",
    description: "R$ 309 milhões contra R$ 149 milhões do bloco de esquerda",
  },
  {
    title: "TAM é a empresa que mais recebe",
    description: "R$ 59 milhões em passagens aéreas de deputados",
  },
]
</script>
