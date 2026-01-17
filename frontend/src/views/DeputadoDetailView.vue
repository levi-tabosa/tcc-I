<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Breadcrumb -->
      <div class="bg-muted/30 border-b border-border">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <router-link to="/deputados" class="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground">
            <ChevronLeft class="h-4 w-4" />
            Voltar para lista
          </router-link>
        </div>
      </div>

      <template v-if="deputado">
        <!-- Profile -->
        <section class="py-8 bg-gradient-to-br from-primary/5 via-background to-accent/5">
          <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col lg:flex-row gap-8">
              <!-- Profile card -->
              <BaseCard class="lg:w-80 flex-shrink-0">
                <div class="text-center">
                  <div class="h-32 w-32 mx-auto rounded-full border-4 border-primary/20 overflow-hidden bg-primary/10 flex items-center justify-center">
                    <img
                      :src="deputado.foto"
                      :alt="deputado.nome"
                      class="w-full h-full object-cover"
                      @error="($event.target as HTMLImageElement).src = '/placeholder-user.jpg'"
                    />
                  </div>

                  <h1 class="mt-4 text-xl font-bold text-foreground">{{ deputado.nome }}</h1>

                  <div class="mt-2 flex items-center justify-center gap-2">
                    <BaseBadge variant="outline">{{ deputado.partido }}</BaseBadge>
                    <BaseBadge variant="outline">{{ deputado.estado }}</BaseBadge>
                  </div>

                  <BaseBadge :class="getBlocoColor(deputado.blocoIdeologico)" class="mt-3">
                    Bloco: {{ deputado.blocoIdeologico.charAt(0).toUpperCase() + deputado.blocoIdeologico.slice(1) }}
                  </BaseBadge>

                  <div class="mt-6 space-y-3 text-sm text-left">
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Mail class="h-4 w-4 text-primary" />
                      <span class="truncate">{{ deputado.email }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Phone class="h-4 w-4 text-primary" />
                      <span>{{ deputado.telefone }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <MapPin class="h-4 w-4 text-primary" />
                      <span>Brasília - DF</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Building class="h-4 w-4 text-primary" />
                      <span>Gabinete {{ 100 + deputado.id }}</span>
                    </div>
                  </div>
                </div>
              </BaseCard>

              <!-- Stats cards -->
              <div class="flex-1 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <BaseCard>
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Gastos Totais</p>
                    <BaseBadge variant="secondary">Cota</BaseBadge>
                  </div>
                  <p class="mt-2 text-3xl font-bold text-foreground">R$ {{ (deputado.gastoTotal / 1000).toFixed(0) }}K</p>
                  <p class="mt-1 text-xs text-muted-foreground">Ranking: #{{ Math.floor(Math.random() * 100) + 1 }}º</p>
                </BaseCard>

                <BaseCard>
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Emendas</p>
                    <BaseBadge variant="secondary">2024</BaseBadge>
                  </div>
                  <p class="mt-2 text-3xl font-bold text-foreground">R$ {{ (deputado.emendasTotal / 1000000).toFixed(1) }}M</p>
                  <p class="mt-1 text-xs text-muted-foreground">{{ Math.floor(Math.random() * 10) + 1 }} emendas</p>
                </BaseCard>

                <BaseCard :class="deputado.auxilioMoradia ? 'border-chart-2' : ''">
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Auxílio Moradia</p>
                    <AlertTriangle v-if="deputado.auxilioMoradia" class="h-4 w-4 text-chart-2" />
                    <CheckCircle v-else class="h-4 w-4 text-primary" />
                  </div>
                  <template v-if="deputado.auxilioMoradia">
                    <p class="mt-2 text-3xl font-bold text-chart-2">R$ {{ deputado.valorAuxilio.toLocaleString() }}</p>
                    <p class="mt-1 text-xs text-muted-foreground">por mês</p>
                  </template>
                  <template v-else>
                    <p class="mt-2 text-xl font-medium text-primary">Não recebe</p>
                    <p class="mt-1 text-xs text-muted-foreground">Usa imóvel funcional</p>
                  </template>
                </BaseCard>

                <BaseCard class="sm:col-span-2 lg:col-span-3">
                  <h3 class="font-semibold text-foreground mb-4">Principais Gastos por Categoria</h3>
                  <div class="space-y-3">
                    <div v-for="item in gastosCategorias" :key="item.categoria">
                      <div class="flex items-center justify-between text-sm mb-1">
                        <span class="text-muted-foreground">{{ item.categoria }}</span>
                        <span class="font-medium text-foreground">R$ {{ (item.valor / 1000).toFixed(0) }}K</span>
                      </div>
                      <div class="h-2 bg-muted rounded-full overflow-hidden">
                        <div
                          class="h-full bg-primary rounded-full"
                          :style="{ width: `${item.percentage}%` }"
                        />
                      </div>
                    </div>
                  </div>
                </BaseCard>
              </div>
            </div>
          </div>
        </section>
      </template>

      <div v-else class="flex-1 flex items-center justify-center">
        <p class="text-muted-foreground">Deputado não encontrado.</p>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronLeft, Mail, Phone, MapPin, Building, AlertTriangle, CheckCircle } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { deputados } from '@/data/mock-data'

const route = useRoute()

const deputado = computed(() => {
  const id = Number(route.params.id)
  return deputados.find(d => d.id === id)
})

const gastosCategorias = computed(() => {
  if (!deputado.value) return []
  const total = deputado.value.gastoTotal
  return [
    { categoria: "Divulgação de Atividade", valor: total * 0.35, percentage: 35 },
    { categoria: "Passagens Aéreas", valor: total * 0.25, percentage: 25 },
    { categoria: "Combustíveis", valor: total * 0.15, percentage: 15 },
    { categoria: "Telefonia", valor: total * 0.1, percentage: 10 },
    { categoria: "Outros", valor: total * 0.15, percentage: 15 },
  ]
})

const getBlocoColor = (bloco: string) => {
  switch (bloco) {
    case 'direita': return 'bg-chart-3/10 text-chart-3 border-chart-3'
    case 'esquerda': return 'bg-chart-4/10 text-chart-4 border-chart-4'
    default: return 'bg-chart-2/10 text-chart-2 border-chart-2'
  }
}
</script>
