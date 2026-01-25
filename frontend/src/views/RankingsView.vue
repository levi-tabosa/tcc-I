<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-chart-2/10 via-background to-primary/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Rankings de Empresas</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Conheça as empresas que mais recebem recursos da cota parlamentar. Transparência nos contratos e pagamentos.
          </p>
        </div>
      </section>

      <!-- Overview -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-4 sm:grid-cols-3">
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-primary/10">
                  <Building2 class="h-6 w-6 text-primary" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total de Empresas</p>
                  <p class="text-2xl font-bold text-foreground">12.847</p>
                </div>
              </div>
            </BaseCard>
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-chart-2/10">
                  <Banknote class="h-6 w-6 text-chart-2" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total Pago</p>
                  <p class="text-2xl font-bold text-foreground">R$ 497M</p>
                </div>
              </div>
            </BaseCard>
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-chart-3/10">
                  <TrendingUp class="h-6 w-6 text-chart-3" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total de Contratos</p>
                  <p class="text-2xl font-bold text-foreground">143.567</p>
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </section>

      <!-- Chart -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Top 10 Empresas por Valor Recebido</h2>
          <BaseCard>
            <div class="space-y-4">
              <div v-for="empresa in topEmpresas.slice(0, 10)" :key="empresa.id" class="flex items-center gap-4">
                <div class="w-32 text-sm font-medium text-foreground truncate">{{ empresa.nome.split(' ')[0] }}</div>
                <div class="flex-1 h-8 bg-muted rounded-lg overflow-hidden">
                  <div
                    class="h-full bg-primary rounded-lg flex items-center justify-end px-2"
                    :style="{ width: `${(empresa.valorTotal / 59000000) * 100}%` }"
                  >
                    <span class="text-xs text-primary-foreground font-medium">R$ {{ (empresa.valorTotal / 1000000).toFixed(0) }}M</span>
                  </div>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
      </section>

      <!-- Table -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 class="text-2xl font-bold text-foreground mb-6">Lista das 20 maiores Empresas</h2>
          <BaseCard>
            <div class="overflow-x-auto">
              <table class="w-full">
                <thead>
                  <tr class="border-b border-border">
                    <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">#</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">Empresa</th>
                    <th class="text-left py-3 px-4 text-sm font-medium text-muted-foreground">CNPJ</th>
                    <th class="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Valor Total</th>
                    <th class="text-right py-3 px-4 text-sm font-medium text-muted-foreground">Contratos</th>
                    <th class="text-right py-3 px-4 text-sm font-medium text-muted-foreground">% do Total</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(empresa, index) in topEmpresas"
                    :key="empresa.id"
                    class="border-b border-border hover:bg-muted/50 transition-colors"
                  >
                    <td class="py-3 px-4 text-sm text-muted-foreground">{{ index + 1 }}</td>
                    <td class="py-3 px-4">
                      <p class="text-sm font-medium text-foreground">{{ empresa.nome }}</p>
                      <p class="text-xs text-muted-foreground">{{ empresa.partidosPrincipais.join(', ') }}</p>
                    </td>
                    <td class="py-3 px-4 text-sm text-muted-foreground font-mono">{{ empresa.cnpj }}</td>
                    <td class="py-3 px-4 text-sm font-medium text-foreground text-right">R$ {{ (empresa.valorTotal / 1000000).toFixed(1) }}M</td>
                    <td class="py-3 px-4 text-sm text-muted-foreground text-right">{{ empresa.contratos.toLocaleString() }}</td>
                    <td class="py-3 px-4 text-sm text-muted-foreground text-right">{{ ((empresa.valorTotal / 497000000) * 100).toFixed(2) }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </BaseCard>
        </div>
      </section>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { Building2, Banknote, TrendingUp } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { topEmpresas } from '@/data/mock-data'
</script>
