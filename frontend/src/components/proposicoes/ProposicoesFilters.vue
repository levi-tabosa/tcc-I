<template>
  <div class="mb-6 space-y-4">
    <div class="flex flex-col sm:flex-row gap-4">
      <!-- Search -->
      <div class="relative flex-1">
        <input
          type="text"
          placeholder="Buscar por ementa..."
          :value="store.filters.search"
          @input="onSearchInput"
          class="w-full px-4 py-3 rounded-full border border-gray-300 bg-background text-foreground placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:shadow-md transition-shadow"
        />
      </div>

      <!-- Tipo -->
      <select
        :value="store.filters.siglaTipo"
        @change="store.setFilter('siglaTipo', ($event.target as HTMLSelectElement).value)"
        class="px-4 py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      >
        <option value="">Todos os tipos</option>
        <option v-for="tipo in tiposProposicao" :key="tipo" :value="tipo">
          {{ tipo }}
        </option>
      </select>

      <!-- Ano -->
      <select
        :value="store.filters.ano"
        @change="store.setFilter('ano', ($event.target as HTMLSelectElement).value)"
        class="px-4 py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      >
        <option value="">Todos os anos</option>
        <option v-for="ano in anosDisponiveis" :key="ano" :value="ano">
          {{ ano }}
        </option>
      </select>
    </div>

    <div v-if="hasActiveFilters" class="flex items-center gap-2">
      <span class="text-sm text-muted-foreground">Filtros ativos:</span>
      <button
        @click="store.resetFilters()"
        class="text-sm text-primary hover:underline"
      >
        Limpar todos
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useProposicoesStore } from '@/stores/proposicoes'

const store = useProposicoesStore()

let searchTimeout: ReturnType<typeof setTimeout> | null = null

const onSearchInput = (event: Event) => {
  const value = (event.target as HTMLInputElement).value
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    store.setFilter('search', value)
  }, 500)
}

const tiposProposicao = [
  'PL', 'PLP', 'PEC', 'MPV', 'PDL', 'PRC', 'REQ', 'INC', 'RIC'
]

const anosDisponiveis = computed(() => {
  const currentYear = new Date().getFullYear()
  const anos = []
  for (let i = currentYear; i >= 2019; i--) {
    anos.push(i)
  }
  return anos
})

const hasActiveFilters = computed(() => {
  return store.filters.search || store.filters.siglaTipo || store.filters.ano
})
</script>
