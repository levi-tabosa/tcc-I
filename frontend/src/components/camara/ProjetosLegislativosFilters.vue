<template>
  <div class="mb-6 space-y-4">
    <div class="flex flex-col sm:flex-row gap-4">
      <!-- Search by ementa -->
      <div class="relative flex-1">
        <input
          type="text"
          placeholder="Buscar por ementa..."
          :value="store.projetosLegislativosFilters.search"
          @input="onSearchInput"
          class="w-full px-6 py-4 rounded-full border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-black/20 hover:shadow-md transition-shadow text-base"
        />
      </div>

      <!-- Search by deputado -->
      <div class="relative flex-1">
        <input
          type="text"
          placeholder="Buscar por deputado que votou..."
          :value="store.projetosLegislativosFilters.deputado"
          @input="onDeputadoInput"
          class="w-full px-6 py-4 rounded-full border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-black/20 hover:shadow-md transition-shadow text-base"
        />
      </div>

      <!-- Tipo -->
      <select
        :value="store.projetosLegislativosFilters.siglaTipo"
        @change="store.setProjetosLegislativosFilter('siglaTipo', ($event.target as HTMLSelectElement).value)"
        class="w-full sm:w-auto px-6 py-4 sm:py-3.5 rounded-full border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-black/20 text-sm"
      >
        <option value="">Todos os tipos</option>
        <option v-for="tipo in tiposProjetoLegislativo" :key="tipo" :value="tipo">
          {{ tipo }}
        </option>
      </select>

      <!-- Ano -->
      <select
        :value="store.projetosLegislativosFilters.ano"
        @change="store.setProjetosLegislativosFilter('ano', ($event.target as HTMLSelectElement).value)"
        class="w-full sm:w-auto px-6 py-4 sm:py-3.5 rounded-full border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-black/20 text-sm"
      >
        <option value="">Todos os anos</option>
        <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">
          {{ ano }}
        </option>
      </select>

      <!-- Legislatura -->
      <select
        :value="store.legislatura"
        @change="store.setLegislatura(Number(($event.target as HTMLSelectElement).value))"
        class="w-full sm:w-auto px-6 py-4 sm:py-3.5 rounded-full border border-foreground/20 bg-background font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-black/20 text-sm"
      >
        <option :value="0">Todas as legislaturas</option>
        <option v-for="leg in store.legislaturasDisponiveis" :key="leg" :value="leg">{{ formatLegislatura(leg) }}</option>
      </select>
    </div>

    <div v-if="hasActiveFilters" class="flex items-center gap-2">
      <span class="text-sm text-muted-foreground">Filtros ativos:</span>
      <button
        @click="store.resetProjetosLegislativosFilters()"
        class="text-sm text-foreground/60 hover:text-foreground hover:underline font-medium transition-colors"
      >
        Limpar todos
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCamaraStore } from '@/stores/camara'

const store = useCamaraStore()

let searchTimeout: ReturnType<typeof setTimeout> | null = null
let deputadoTimeout: ReturnType<typeof setTimeout> | null = null

const onSearchInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    store.setProjetosLegislativosFilter('search', value)
  }, 500)
}

const onDeputadoInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value
  if (deputadoTimeout) clearTimeout(deputadoTimeout)
  deputadoTimeout = setTimeout(() => {
    store.setProjetosLegislativosFilter('deputado', value)
  }, 500)
}

const tiposProjetoLegislativo = computed(() => store.tiposUnicosProjetosLegislativos)

const anosDisponiveis = computed(() => {
  const currentYear = new Date().getFullYear()
  const anos = []
  for (let i = currentYear; i >= 2019; i--) {
    anos.push(i)
  }
  return anos
})

const hasActiveFilters = computed(() => {
  return store.projetosLegislativosFilters.search || store.projetosLegislativosFilters.siglaTipo || store.projetosLegislativosFilters.ano || store.projetosLegislativosFilters.deputado
})

const formatLegislatura = (legis: number) => {
  if (legis === 57) return '57ª (2023-2027)'
  if (legis === 56) return '56ª (2019-2023)'
  if (legis === 55) return '55ª (2015-2019)'
  if (legis === 54) return '54ª (2011-2015)'
  if (legis === 53) return '53ª (2007-2011)'
  return `${legis}ª`
}
</script>
