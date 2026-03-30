<template>
  <div class="mb-6 space-y-4">
    <div class="flex flex-col gap-4">
      <!-- Linha 1: Busca e Legislatura -->
      <div class="flex flex-col sm:flex-row gap-4">
        <!-- Search -->
        <div class="relative flex-1">
          <Search class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
          <input
            type="text"
            placeholder="Buscar senador..."
            :value="store.filters.search"
            @input="store.setFilter('search', ($event.target as HTMLInputElement).value)"
            class="input-base pl-12 pr-6 py-4 rounded-full border border-border bg-background text-foreground focus:ring-black/20 text-base w-full"
          />
        </div>

        <!-- Legislatura -->
        <div class="relative">
          <select
            :value="store.legislatura"
            @change="store.setLegislatura(Number(($event.target as HTMLSelectElement).value))"
            class="input-base px-6 py-3.5 pr-12 rounded-full appearance-none cursor-pointer w-full sm:w-auto sm:min-w-[220px] border border-foreground/20 bg-background font-semibold text-foreground focus:ring-black/20 text-sm"
          >
            <option :value="0">Todas as legislaturas</option>
            <option v-for="leg in store.legislaturasDisponiveis" :key="leg" :value="leg">{{ formatLegislatura(leg) }}</option>
          </select>
          <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-foreground/50 pointer-events-none" />
        </div>
      </div>

      <!-- Linha 2: Partido e Estado -->
      <div class="flex flex-col sm:flex-row gap-4">
        <!-- Partido -->
        <div class="relative flex-1 sm:flex-none">
          <select
            :value="store.filters.partido"
            @change="store.setFilter('partido', ($event.target as HTMLSelectElement).value)"
            class="input-base px-6 py-3.5 pr-12 rounded-full appearance-none cursor-pointer w-full sm:w-auto sm:min-w-[200px] border border-border bg-background text-foreground focus:ring-black/20 text-sm"
          >
            <option value="">Todos os partidos</option>
            <option v-for="partido in store.partidosUnicos" :key="partido" :value="partido">
              {{ partido }}
            </option>
          </select>
          <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        </div>

        <!-- Estado -->
        <div class="relative flex-1 sm:flex-none">
          <select
            :value="store.filters.estado"
            @change="store.setFilter('estado', ($event.target as HTMLSelectElement).value)"
            class="input-base px-6 py-3.5 pr-12 rounded-full appearance-none cursor-pointer w-full sm:w-auto sm:min-w-[200px] border border-border bg-background text-foreground focus:ring-black/20 text-sm"
          >
            <option value="">Todos os estados</option>
            <option v-for="estado in store.estadosUnicos" :key="estado" :value="estado">
              {{ estado }}
            </option>
          </select>
          <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
        </div>
      </div>
    </div>

    <div v-if="hasActiveFilters" class="flex items-center gap-2">
      <span class="text-sm text-muted-foreground">Filtros ativos:</span>
      <button
        @click="store.resetFilters()"
        class="text-sm text-foreground/60 hover:text-foreground hover:underline font-medium transition-colors"
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
  if (legis === 57) return '57ª (2023-2027)'
  if (legis === 56) return '56ª (2019-2023)'
  if (legis === 55) return '55ª (2015-2019)'
  if (legis === 54) return '54ª (2011-2015)'
  if (legis === 53) return '53ª (2007-2011)'
  return `${legis}ª`
}
</script>
