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
          class="w-full px-4 py-3 rounded-full border border-gray-300 bg-background text-foreground placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:shadow-md transition-shadow"
        />
      </div>

      <!-- Search by senador -->
      <div class="relative flex-1">
        <input
          type="text"
          placeholder="Buscar por senador que votou..."
          :value="store.projetosLegislativosFilters.senador"
          @input="onSenadorInput"
          class="w-full px-4 py-3 rounded-full border border-gray-300 bg-background text-foreground placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:shadow-md transition-shadow"
        />
      </div>

      <!-- Tipo -->
      <select
        :value="store.projetosLegislativosFilters.siglaTipo"
        @change="store.setProjetosLegislativosFilter('siglaTipo', ($event.target as HTMLSelectElement).value)"
        class="w-full sm:w-auto px-4 py-3 sm:py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      >
        <option value="">Todos os tipos</option>
        <option v-for="tipo in store.tiposUnicosProjetosLegislativos" :key="tipo" :value="tipo">
          {{ tipo }}
        </option>
      </select>

      <!-- Ano -->
      <select
        :value="store.projetosLegislativosFilters.ano"
        @change="store.setProjetosLegislativosFilter('ano', ($event.target as HTMLSelectElement).value)"
        class="w-full sm:w-auto px-4 py-3 sm:py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      >
        <option value="">Todos os anos</option>
        <option v-for="ano in store.anosUnicosProjetosLegislativos" :key="ano" :value="ano">
          {{ ano }}
        </option>
      </select>

      <!-- Legislatura -->
      <select
        :value="store.legislatura"
        @change="store.setLegislatura(Number(($event.target as HTMLSelectElement).value))"
        class="w-full sm:w-auto px-4 py-3 sm:py-2 rounded-lg border border-purple-600/30 bg-purple-50 font-semibold text-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
      >
        <option v-for="leg in store.legislaturasDisponiveis" :key="leg" :value="leg">{{ formatLegislatura(leg) }}</option>
      </select>
    </div>

    <div v-if="hasActiveFilters" class="flex items-center gap-2">
      <span class="text-sm text-muted-foreground">Filtros ativos:</span>
      <button
        @click="store.resetProjetosLegislativosFilters()"
        class="text-sm text-primary hover:underline"
      >
        Limpar todos
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useSenadoStore } from '@/stores/senado'

const store = useSenadoStore()

let searchTimeout: ReturnType<typeof setTimeout> | null = null
let senadorTimeout: ReturnType<typeof setTimeout> | null = null

const onSearchInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    store.setProjetosLegislativosFilter('search', value)
  }, 500)
}

const onSenadorInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value
  if (senadorTimeout) clearTimeout(senadorTimeout)
  senadorTimeout = setTimeout(() => {
    store.setProjetosLegislativosFilter('senador', value)
  }, 500)
}

const hasActiveFilters = computed(() => {
  return store.projetosLegislativosFilters.search || store.projetosLegislativosFilters.siglaTipo || store.projetosLegislativosFilters.ano || store.projetosLegislativosFilters.senador
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
