<template>
  <div class="min-h-screen bg-background">
    <AppHeader />
    <div class="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
      <div class="space-y-8">
        <div class="text-center">
          <h1 class="text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            Metodologia
          </h1>
          <p class="mt-4 text-lg text-muted-foreground">
            Entenda como coletamos e analisamos os dados da transparência pública
          </p>
        </div>

        <div class="prose prose-lg mx-auto mt-12 space-y-8">
          <section class="bg-card rounded-lg p-6 border border-border">
            <h2 class="text-2xl font-bold text-foreground mb-4">Fonte dos Dados</h2>
            <p class="text-muted-foreground leading-relaxed">
              Todos os dados apresentados são obtidos através da API oficial da Câmara dos Deputados
              e do Portal da Transparência do Governo Federal. As informações são atualizadas
              periodicamente para garantir a precisão e confiabilidade dos dados.
            </p>
          </section>

          <section class="bg-card rounded-lg p-6 border border-border">
            <h2 class="text-2xl font-bold text-foreground mb-4">Análise de Despesas</h2>
            <p class="text-muted-foreground leading-relaxed">
              As despesas são categorizadas de acordo com a classificação oficial da Câmara dos
              Deputados. Realizamos análises estatísticas para identificar padrões de gastos,
              valores médios por categoria e comparações entre deputados e partidos.
            </p>
          </section>

          <section class="bg-card rounded-lg p-6 border border-border">
            <h2 class="text-2xl font-bold text-foreground mb-4">Emendas Parlamentares</h2>
            <p class="text-muted-foreground leading-relaxed">
              Os dados de emendas parlamentares incluem tanto emendas individuais quanto de bancada.
              Cada emenda é classificada por área de aplicação, município beneficiado e status de
              execução. As informações são consolidadas do Sistema Integrado de Planejamento e
              Orçamento (SIOP).
            </p>
          </section>

          <section class="bg-card rounded-lg p-6 border border-border">
            <h2 class="text-2xl font-bold text-foreground mb-4">Rankings e Estatísticas</h2>
            <p class="text-muted-foreground leading-relaxed">
              Os rankings são calculados com base em métricas objetivas como total de gastos,
              presença em sessões, proposições apresentadas e votações. Utilizamos normalização
              estatística para permitir comparações justas entre deputados de diferentes estados
              e partidos.
            </p>
          </section>

          <section class="bg-card rounded-lg p-6 border border-border">
            <h2 class="text-2xl font-bold text-foreground mb-4">Periodicidade de Atualização</h2>
            <p class="text-muted-foreground leading-relaxed">
              Os dados são atualizados automaticamente a cada 24 horas. Em períodos de alta
              atividade legislativa, como durante votações importantes, a atualização pode
              ocorrer com maior frequência.
            </p>
          </section>

          <section class="bg-card rounded-lg p-6 border border-border">
            <h2 class="text-2xl font-bold text-foreground mb-4">Código Aberto</h2>
            <p class="text-muted-foreground leading-relaxed">
              Este projeto é de código aberto e está disponível para auditoria pública.
              Acreditamos na transparência não apenas dos dados governamentais, mas também
              das ferramentas que utilizamos para analisá-los.
            </p>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import AppHeader from '@/components/layout/AppHeader.vue'

// Nenhuma lógica necessária por enquanto
</script>
