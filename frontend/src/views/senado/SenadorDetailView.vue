<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    <main class="flex-1">
      <!-- Breadcrumb -->
      <div class="bg-muted/30 border-b border-border">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <router-link to="/senado/senadores" class="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground">
            <ChevronLeft class="h-4 w-4" />
            Voltar para lista
          </router-link>

          <!-- Legislatura Selector -->
          <div class="flex items-center gap-3 bg-purple-50 px-3 py-1.5 rounded-full border border-purple-100">
            <span class="text-xs font-bold text-purple-600/60 uppercase tracking-wider">Visualizando:</span>
            <select
              :value="store.legislatura"
              @change="store.setLegislatura(Number(($event.target as HTMLSelectElement).value))"
              class="text-sm font-bold text-purple-700 bg-transparent border-none p-0 focus:ring-0 cursor-pointer"
            >
              <option :value="57">57ª Legislatura (2023-2027)</option>
              <option :value="56">56ª Legislatura (2019-2023)</option>
              <option :value="55">55ª Legislatura (2015-2019)</option>
            </select>
          </div>
        </div>
      </div>

      <BaseLoading v-if="store.loadingDetail" message="Carregando detalhes do senador..." full-page />

      <div v-else-if="store.error" class="flex-1 flex items-center justify-center min-h-[400px]">
        <p class="text-destructive">{{ store.error }}</p>
      </div>

      <template v-else-if="store.currentSenador">
        <!-- Profile -->
        <section class="py-8 bg-gradient-to-br from-purple-500/10 via-background to-accent/5">
          <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div class="flex flex-col lg:flex-row gap-8">
              <!-- Profile card -->
              <BaseCard class="lg:w-80 flex-shrink-0 border-purple-100">
                <div class="text-center">
                  <div class="h-32 w-32 mx-auto rounded-full border-4 border-purple-200 overflow-hidden bg-purple-50 flex items-center justify-center">
                    <img
                      :src="store.currentSenador.foto"
                      :alt="store.currentSenador.nome_civil"
                      class="w-full h-full object-cover"
                      @error="($event.target as HTMLImageElement).src = '/placeholder-user.svg'"
                    />
                  </div>

                  <h1 class="mt-4 text-xl font-bold text-foreground">{{ store.currentSenador.nome_civil }}</h1>

                  <div class="mt-2 flex flex-wrap items-center justify-center gap-2">
                    <BaseBadge variant="outline">{{ store.currentSenador.sigla_partido }}</BaseBadge>
                    <BaseBadge v-if="store.currentSenador.uf" variant="outline">{{ store.currentSenador.uf }}</BaseBadge>
                  </div>

                  <div class="mt-6 space-y-3 text-sm text-left">
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Mail class="h-4 w-4 text-purple-500" />
                      <span class="truncate">{{ store.currentSenador.email || 'Indisponível' }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <Calendar class="h-4 w-4 text-purple-500" />
                      <span>{{ store.currentSenador.data_nascimento ? formatDate(store.currentSenador.data_nascimento) : 'Indisponível' }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <GraduationCap class="h-4 w-4 text-purple-500" />
                      <span>{{ store.currentSenador.escolaridade || 'Indisponível' }}</span>
                    </div>
                    <div class="flex items-center gap-3 text-muted-foreground">
                      <User class="h-4 w-4 text-purple-500" />
                      <span>{{ store.currentSenador.cpf ? `***.${store.currentSenador.cpf.slice(3, 6)}.***-**` : 'Indisponível' }}</span>
                    </div>
                  </div>
                </div>
              </BaseCard>

              <!-- Stats cards -->
              <div class="flex-1 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                <BaseCard class="border-purple-100">
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Gastos Totais</p>
                    <BaseBadge variant="secondary" class="bg-purple-100 text-purple-800">Mandato</BaseBadge>
                  </div>
                  <p v-if="totalGastos > 0" class="mt-2 text-3xl font-bold text-foreground">R$ {{ (totalGastos / 1000).toFixed(0) }}K</p>
                  <p v-else class="mt-2 text-xl font-bold text-muted-foreground">0</p>
                  <p class="mt-1 text-xs text-muted-foreground">Soma de todas despesas registradas</p>
                </BaseCard>

                <BaseCard class="border-purple-100">
                  <div class="flex items-center justify-between">
                    <p class="text-sm text-muted-foreground">Emendas</p>
                    <BaseBadge variant="secondary" class="bg-purple-100 text-purple-800">Mandato</BaseBadge>
                  </div>
                  <p v-if="store.totalEmendas > 0" class="mt-2 text-3xl font-bold text-foreground">R$ {{ (store.totalEmendas / 1000000).toFixed(1) }}M</p>
                  <p v-else class="mt-2 text-xl font-bold text-muted-foreground">Dados Indisponíveis</p>
                  <p class="mt-1 text-xs text-muted-foreground text-purple-600/70">Soma das emendas pagas ao senador</p>
                </BaseCard>

                <BaseCard class="sm:col-span-2 lg:col-span-3 border-purple-100">
                  <h3 class="font-semibold text-foreground mb-4">Principais Gastos por Categoria</h3>
                  <div class="space-y-3">
                    <div v-if="gastosCategorias.length === 0" class="py-6 text-center text-muted-foreground italic">
                      Dados Indisponíveis ou Sem Gastos
                    </div>
                    <div v-for="item in gastosCategorias" :key="item.categoria">
                      <div class="flex items-center justify-between text-sm mb-1">
                        <span class="text-muted-foreground">{{ item.categoria }}</span>
                        <span class="font-medium text-foreground">R$ {{ (item.valor / 1000).toFixed(0) }}K</span>
                      </div>
                      <div class="progress-bar bg-purple-100">
                        <div
                          class="progress-fill bg-purple-500"
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
        
        <!-- Emendas Table Section -->
        <section class="py-8 bg-purple-50/30">
            <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
                <h3 class="text-xl font-bold text-foreground mb-4">Emendas Parlamentares</h3>
                <BaseCard variant="elevated" class="p-0 overflow-hidden border-purple-100 shadow-purple-900/5">
                    <div class="overflow-x-auto max-h-[600px] relative">
                        <table class="table-professional w-full border-collapse">
                            <thead class="sticky top-0 z-10 bg-card border-b border-purple-100 shadow-sm">
                                <tr>
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b border-purple-100">Ano/Tipo</th>
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b border-purple-100">Função</th>
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b border-purple-100">Localidade</th>
                                    <th class="bg-card py-4 px-4 text-right font-bold text-xs uppercase tracking-wider text-muted-foreground border-b border-purple-100">Valor Pago</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-purple-50 bg-card">
                                <tr v-for="(emenda, index) in store.currentEmendas" :key="index" class="hover:bg-purple-50/50 transition-colors">
                                    <td class="whitespace-nowrap">
                                        <div class="flex flex-col">
                                            <span class="font-medium text-purple-900">{{ emenda.ano }}</span>
                                            <span class="text-xs text-muted-foreground">{{ emenda.tipo }}</span>
                                        </div>
                                    </td>
                                    <td class="text-muted-foreground">{{ emenda.funcao }}</td>
                                    <td class="text-muted-foreground">{{ emenda.localidade }}</td>
                                    <td class="text-right whitespace-nowrap font-medium text-purple-600">R$ {{ emenda.valorPago.toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</td>
                                </tr>
                                <tr v-if="store.currentEmendas.length === 0">
                                    <td colspan="4" class="py-12 text-center text-muted-foreground italic">Dados Indisponíveis</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </BaseCard>
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
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b">Descrição / Categoria</th>
                                    <th class="bg-card py-4 px-4 text-left font-bold text-xs uppercase tracking-wider text-muted-foreground border-b hidden sm:table-cell">Fornecedor</th>
                                    <th class="bg-card py-4 px-4 text-right font-bold text-xs uppercase tracking-wider text-muted-foreground border-b">Valor</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-border bg-card">
                                <tr v-for="(despesa, index) in store.currentDespesas" :key="index" class="hover:bg-muted/50 transition-colors">
                                    <td class="whitespace-nowrap">{{ despesa.mes }}/{{ despesa.ano }}</td>
                                    <td class="truncate max-w-xs">{{ despesa.tipoDespesa || despesa.tipo_despesa }}</td>
                                    <td class="truncate max-w-xs hidden sm:table-cell">{{ despesa.fornecedor || '--' }}</td>
                                    <td class="text-right whitespace-nowrap font-medium">R$ {{ (despesa.valorReembolsado || despesa.valor || 0).toLocaleString('pt-BR', { minimumFractionDigits: 2 }) }}</td>
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
        <p class="text-muted-foreground">Senador não encontrado.</p>
      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronLeft, Mail, Calendar, User, GraduationCap } from 'lucide-vue-next'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseLoading from '@/components/ui/BaseLoading.vue'
import { useSenadoresStore } from '@/stores/senadores'

const route = useRoute()
const store = useSenadoresStore()

const loadData = () => {
    const id = Number(route.params.id)
    if (id) {
        store.fetchSenador(id)
    }
}

onMounted(() => {
    loadData()
})

watch(() => route.params.id, () => {
    loadData()
})

watch(() => store.legislatura, () => {
    loadData()
})

const formatDate = (dateString: string) => {
    if (!dateString) return '--'
    const date = new Date(dateString)
    return date.toLocaleDateString('pt-BR')
}

watch(() => store.currentSenador, (newVal) => {
    if (newVal) {
        document.title = `${newVal.nome_civil} - Senado | Fiscaliza Brasil`
    }
}, { immediate: true })

const totalGastos = computed(() => {
    return store.totalDespesas
})

const gastosCategorias = computed(() => {
    const total = totalGastos.value
    if (total === 0 || store.currentCategorias.length === 0) return []

    return store.currentCategorias
        .map(c => ({
            categoria: c.categoria,
            valor: c.valor,
            percentage: (c.valor / total) * 100
        }))
        .slice(0, 5) // Top 5
})

</script>
