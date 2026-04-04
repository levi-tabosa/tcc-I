<template>
  <div class="mb-6 space-y-4">
    <div class="flex flex-col sm:flex-row gap-3">
      <!-- Search -->
      <div class="relative flex-1">
        <Search class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        <input
          type="text"
          placeholder="Buscar senador..."
          :value="store.filters.search"
          @input="store.setFilter('search', ($event.target as HTMLInputElement).value)"
          class="input-base pl-11 pr-4 py-3 rounded-full"
        />
      </div>

      <!-- Partido -->
      <div class="relative">
        <select
          :value="store.filters.partido"
          @change="store.setFilter('partido', ($event.target as HTMLSelectElement).value)"
          class="input-base px-4 py-2.5 pr-10 rounded-full appearance-none cursor-pointer w-full sm:w-auto sm:min-w-[180px]"
        >
          <option value="">Todos os partidos</option>
          <option v-for="partido in store.partidosUnicos" :key="partido" :value="partido">
            {{ partido }}
          </option>
        </select>
        <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
      </div>

      <!-- Estado -->
      <div class="relative">
        <select
          :value="store.filters.estado"
          @change="store.setFilter('estado', ($event.target as HTMLSelectElement).value)"
          class="input-base px-4 py-2.5 pr-10 rounded-full appearance-none cursor-pointer w-full sm:w-auto sm:min-w-[180px]"
        >
          <option value="">Todos os estados</option>
          <option v-for="estado in store.estadosUnicos" :key="estado" :value="estado">
            {{ estado }}
          </option>
        </select>
        <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
      </div>

      <!-- Legislatura -->
      <div class="relative">
        <select
          :value="store.legislatura"
          @change="store.setLegislatura(Number(($event.target as HTMLSelectElement).value))"
          class="input-base px-4 py-2.5 pr-10 rounded-full appearance-none cursor-pointer w-full sm:w-auto sm:min-w-[140px] border-neutral-300 bg-neutral-50 font-semibold text-neutral-800"
        >
          <option :value="0">Todas as legislaturas</option>
          <option v-for="leg in store.legislaturasDisponiveis" :key="leg" :value="leg">{{ formatLegislatura(leg) }}</option>
        </select>
        <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-neutral-500 pointer-events-none" />
      </div>
    </div>

    <div v-if="hasActiveFilters" class="flex items-center gap-2">
      <span class="text-sm text-muted-foreground">Filtros ativos:</span>
      <button
        @click="store.resetFilters()"
        class="text-sm text-purple-600 hover:text-purple-700 hover:underline font-medium transition-colors"
      >
        Limpar todos
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Search, ChevronDown } from 'lucide-vue-next'
import { useSenadoStore } from '@/stores/senado'

const store = useSenadoStore()

const hasActiveFilters = computed(() => {
  return store.filters.search || store.filters.partido || store.filters.estado
})

const formatLegislatura = (legis: number) => {
  if (legis === 0) return 'Todas as legislaturas'
  const startYear = 2023 - (57 - legis) * 4
  const endYear = startYear + 4
  return `${legis}ª (${startYear}-${endYear})`
}
</script>
