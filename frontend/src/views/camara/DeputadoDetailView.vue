<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Breadcrumb -->
      <div class="bg-muted/30 border-b border-border">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4">
          <router-link to="/camara/deputados" class="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground">
            <ChevronLeft class="h-4 w-4" />
            Voltar para lista
          </router-link>
        </div>
      </div>

      <div v-if="store.loadingDetail" class="flex-1 min-h-[400px]">
        <section class="py-8">
          <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col lg:flex-row gap-8">
              <div class="lg:w-80 flex-shrink-0">
                <div class="card-default p-6 text-center">
                  <div class="skeleton-circle h-32 w-32 mx-auto"></div>
                  <div class="skeleton-text w-48 mx-auto mt-4"></div>
                  <div class="flex justify-center gap-2 mt-3">
                    <div class="skeleton-text w-16"></div>
                    <div class="skeleton-text w-12"></div>
                  </div>
                  <div class="space-y-3 mt-6">
                    <div class="skeleton-text w-full"></div>
                    <div class="skeleton-text w-3/4"></div>
                    <div class="skeleton-text w-2/3"></div>
                  </div>
                </div>
              </div>
              <div class="flex-1 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <div v-for="i in 3" :key="i" class="card-default p-6">
                  <div class="skeleton-text-sm w-24 mb-2"></div>
                  <div class="skeleton-text w-32 h-8"></div>
                  <div class="skeleton-text-sm w-40 mt-2"></div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      <div v-else-if="store.error" class="flex-1 flex items-center justify-center min-h-[400px]">
        <p class="text-destructive">{{ store.error }}</p>
      </div>

      <template v-else-if="store.currentDeputado">
        <!-- Profile -->
        <section class="py-8 bg-gradient-to-br from-primary/5 via-background to-accent/5">
          <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col lg:flex-row gap-8">
              <!-- Profile card -->
              <BaseCard class="lg:w-80 flex-shrink-0">
                <div class="text-center">
                  <div class="h-32 w-32 mx-auto rounded-full border-4 border-primary/20 overflow-hidden bg-primary/10 flex items-center justify-center">
                    <img
                      :src="store.currentDeputado.foto"
                      :alt="store.currentDeputado.nome_civil"
                      class="w-full h-full object-cover"
                      @error="($event.target as HTMLImageElement).src = '/placeholder-user.jpg'"
                    />
                  </div>

                  <h1 class="mt-4 text-xl font-bold text-foreground">{{ store.currentDeputado.nome_civil }}</h1>

                  <div class="mt-2 flex flex-wrap items-center justify-center gap-2">
                    <BaseBadge variant="outline">{{ store.currentDeputado.sigla_partido }}</BaseBadge>
                    <BaseBadge v-if="store.currentDeputado.uf_nascimento" variant="outline">{{ store.currentDeputado.uf_nascimento }}</BaseBadge>
                  </div>

                  <div class="mt-6 space-y-3 text-sm text-left">
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Mail class="h-4 w-4 text-primary" />
                      <span class="truncate">{{ store.currentDeputado.email || 'Indisponível' }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Calendar class="h-4 w-4 text-primary" />
                      <span>{{ store.currentDeputado.data_nascimento ? formatDate(store.currentDeputado.data_nascimento) : 'Indisponível' }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <GraduationCap class="h-4 w-4 text-primary" />
                      <span>{{ store.currentDeputado.escolaridade || 'Indisponível' }}</span>
                    </div>
                    <!-- CPF masked -->
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <User class="h-4 w-4 text-primary" />
                      <span>{{ store.currentDeputado.cpf ? `***.${store.currentDeputado.cpf.slice(3, 6)}.***-**` : 'Indisponível' }}</span>
                    </div>
                  </div>
                </div>
              </BaseCard>

              <!-- Stats cards -->
              <div class="flex-1 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <BaseCard>
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Gastos Totais</p>
                    <BaseBadge variant="secondary">Mandato</BaseBadge>
                  </div>
                  <p v-if="totalGastos > 0" class="mt-2 text-3xl font-bold text-foreground">R$ {{ (totalGastos / 1000).toFixed(0) }}K</p>
                  <p v-else class="mt-2 text-xl font-bold text-muted-foreground">Dados Indisponíveis</p>
                  <p class="mt-1 text-xs text-muted-foreground">Soma de todas despesas registradas</p>
                </BaseCard>

                 <!-- Placeholder for stats not currently in API -->
                <BaseCard class="opacity-70">
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Emendas</p>
                    <BaseBadge variant="outline">Breve</BaseBadge>
                  </div>
                  <p class="mt-2 text-xl font-bold text-muted-foreground">Dados Indisponíveis</p>
                  <p class="mt-1 text-xs text-muted-foreground italic">Informação não integrada ao portal</p>
                </BaseCard>

                <BaseCard class="sm:col-span-2 lg:col-span-3">
                  <h3 class="font-semibold text-foreground mb-4">Principais Gastos por Categoria</h3>
                  <div class="space-y-3">
                    <div v-if="gastosCategorias.length === 0" class="py-6 text-center text-muted-foreground italic">
                      Dados Indisponíveis
                    </div>
                    <div v-for="item in gastosCategorias" :key="item.categoria">
                      <div class="flex items-center justify-between text-sm mb-1">
                        <span class="text-muted-foreground">{{ item.categoria }}</span>
                        <span class="font-medium text-foreground">R$ {{ (item.valor / 1000).toFixed(0) }}K</span>
                      </div>
                      <div class="progress-bar">
                        <div
                          class="progress-fill"
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
        
        <!-- Expenses Table Section -->
        <section class="py-8">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <h3 class="text-xl font-bold text-foreground mb-4">Histórico de Despesas</h3>
                <BaseCard variant="elevated" class="p-0 overflow-hidden">
                    <div class="overflow-x-auto max-h-[600px] relative">
                        <table class="table-professional w-full border-collapse">
                            <thead class="sticky top-0 z-10 bg-card border-b shadow-sm">
                                <tr>
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b">Data</th>
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b">Descrição</th>
                                    <th class="bg-card py-4 px-4 text-right font-bold text-xs uppercase tracking-wider text-muted-foreground border-b">Valor</th>
                                    <th class="bg-card py-4 px-4 text-center font-bold text-xs uppercase tracking-wider text-muted-foreground border-b">Doc</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-border bg-card">
                                <tr v-for="(despesa, index) in store.currentDespesas.slice(0, 50)" :key="index" class="hover:bg-muted/50 transition-colors">
                                    <td class="whitespace-nowrap">{{ despesa.mes }}/{{ despesa.ano }}</td>
                                    <td class="truncate max-w-xs">{{ despesa.tipo_despesa }}</td>
                                    <td class="text-right whitespace-nowrap font-medium">R$ {{ despesa.valor.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</td>
                                    <td class="text-center">
                                        <a v-if="despesa.url_documento" :href="despesa.url_documento" target="_blank" class="text-primary hover:text-primary-700 transition-colors" title="Ver documento">
                                            <FileText class="h-4 w-4 mx-auto" />
                                        </a>
                                        <span v-else class="text-muted-foreground">--</span>
                                    </td>
                                </tr>
                                <tr v-if="store.currentDespesas.length === 0">
                                    <td colspan="4" class="py-12 text-center text-muted-foreground italic">Dados Indisponíveis</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </BaseCard>
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
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronLeft, Mail, Calendar, GraduationCap, User, FileText } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { useDeputadosStore } from '@/stores/deputados'

const route = useRoute()
const store = useDeputadosStore()

const loadData = () => {
    const id = Number(route.params.id)
    if (id) {
        store.fetchDeputado(id)
    }
}

onMounted(() => {
    loadData()
})

watch(() => route.params.id, () => {
    loadData()
})

const formatDate = (dateString: string) => {
    if (!dateString) return '--'
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR')
}

const totalGastos = computed(() => {
    return store.totalDespesas
})

const gastosCategorias = computed(() => {
    const total = totalGastos.value
    if (total === 0 || !store.currentCategorias || store.currentCategorias.length === 0) return []

    return store.currentCategorias
        .map(c => ({
            categoria: c.categoria,
            valor: c.valor,
            percentage: (c.valor / total) * 100
        }))
        .slice(0, 5) // Top 5
})

watch(() => store.currentDeputado, (newVal) => {
    if (newVal) {
        document.title = `${newVal.nome_civil} - Câmara | Fiscaliza Brasil`
    }
}, { immediate: true })

</script>
