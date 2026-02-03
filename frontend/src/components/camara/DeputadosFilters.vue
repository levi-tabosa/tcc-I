<template>
  <div class="mb-6 space-y-4">
    <div class="flex flex-col sm:flex-row gap-4">
      <!-- Search -->
      <div class="relative flex-1">
        <input
          type="text"
          placeholder="Buscar deputado..."
          :value="store.filters.search"
          @input="store.setFilter('search', ($event.target as HTMLInputElement).value)"
          class="w-full px-4 py-3 rounded-full border border-gray-300 bg-background text-foreground placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent hover:shadow-md transition-shadow"
        />
      </div>

      <!-- Partido -->
      <select
        :value="store.filters.partido"
        @change="store.setFilter('partido', ($event.target as HTMLSelectElement).value)"
        class="px-4 py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      >
        <option value="">Todos os partidos</option>
        <option v-for="partido in partidos" :key="partido.sigla" :value="partido.sigla">
          {{ partido.sigla }}
        </option>
      </select>

      <!-- Estado -->
      <select
        :value="store.filters.estado"
        @change="store.setFilter('estado', ($event.target as HTMLSelectElement).value)"
        class="px-4 py-2 rounded-lg border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring"
      >
        <option value="">Todos os estados</option>
        <option v-for="estado in estados" :key="estado.sigla" :value="estado.sigla">
          {{ estado.sigla }}
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
import { useDeputadosStore } from '@/stores/deputados'
import { partidos, estados } from '@/data/mock-data'

const store = useDeputadosStore()

const hasActiveFilters = computed(() => {
  return store.filters.search || store.filters.partido || store.filters.estado
})
</script>
