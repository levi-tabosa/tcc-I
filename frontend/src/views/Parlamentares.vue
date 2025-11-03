<template>
  <div class="min-h-screen bg-background">
    <AppHeader />
    <div class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-foreground mb-2">Parlamentares</h1>
  <p class="text-muted-foreground">Explore dados de {{ mockData.parlamentares.length }} parlamentares</p>
      </div>

      <!-- Filters and Search -->
      <div class="card mb-6">
        <div class="card-content pt-6">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <!-- Search -->
            <div class="relative md:col-span-2">
              <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Buscar por nome..."
                v-model="searchTerm"
                class="input pl-9"
              />
            </div>

            <!-- Party Filter -->
            <select v-model="partidoFilter" class="select">
              <option v-for="partido in mockData.partidos" :key="partido" :value="partido">
                {{ partido }}
              </option>
            </select>

            <!-- State Filter -->
            <select v-model="estadoFilter" class="select">
              <option v-for="estado in mockData.estados" :key="estado" :value="estado">
                {{ estado }}
              </option>
            </select>
          </div>

          <!-- Sort Options -->
          <div class="flex flex-wrap gap-2 mt-4">
            <span class="text-sm text-muted-foreground self-center">Ordenar por:</span>
            <button
              :class="getBtnClass('nome')"
              @click="toggleSort('nome')"
            >
              Nome
              <TrendingUp v-if="sortField === 'nome' && sortOrder === 'asc'" class="ml-1 h-3 w-3" />
              <TrendingDown v-if="sortField === 'nome' && sortOrder === 'desc'" class="ml-1 h-3 w-3" />
            </button>
            <button
              :class="getBtnClass('gastoTotal')"
              @click="toggleSort('gastoTotal')"
            >
              Gastos
              <TrendingUp v-if="sortField === 'gastoTotal' && sortOrder === 'asc'" class="ml-1 h-3 w-3" />
              <TrendingDown v-if="sortField === 'gastoTotal' && sortOrder === 'desc'" class="ml-1 h-3 w-3" />
            </button>
            <button
              :class="getBtnClass('presenca')"
              @click="toggleSort('presenca')"
            >
              Presença
              <TrendingUp v-if="sortField === 'presenca' && sortOrder === 'asc'" class="ml-1 h-3 w-3" />
              <TrendingDown v-if="sortField === 'presenca' && sortOrder === 'desc'" class="ml-1 h-3 w-3" />
            </button>
            <button
              :class="getBtnClass('fidelidadePartidaria')"
              @click="toggleSort('fidelidadePartidaria')"
            >
              Fidelidade
              <TrendingUp v-if="sortField === 'fidelidadePartidaria' && sortOrder === 'asc'" class="ml-1 h-3 w-3" />
              <TrendingDown v-if="sortField === 'fidelidadePartidaria' && sortOrder === 'desc'" class="ml-1 h-3 w-3" />
            </button>
          </div>
        </div>
      </div>

      <!-- comparação removida -->

      <!-- Results Count -->
      <div class="mb-4">
        <p class="text-sm text-muted-foreground">
          Mostrando {{ filteredAndSorted.length }} de {{ mockData.parlamentares.length }} parlamentares
        </p>
      </div>

      <!-- Parliamentarians Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div 
          v-for="parlamentar in filteredAndSorted" 
          :key="parlamentar.id" 
          class="card hover:shadow-lg transition-shadow"
        >
          <div class="card-content pt-6">
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1">
                <RouterLink
                  :to="'/perfil/' + parlamentar.id"
                  class="text-lg font-semibold text-foreground hover:text-primary transition-colors"
                >
                  {{ parlamentar.nome }}
                </RouterLink>
                <p class="text-sm text-muted-foreground">{{ parlamentar.cargo }}</p>
              </div>
              <!-- seleção para comparação removida -->
            </div>

            <div class="flex gap-2 mb-4">
              <span class="badge badge-secondary">{{ parlamentar.partido }}</span>
              <span class="badge badge-outline">{{ parlamentar.estado }}</span>
            </div>

            <div class="space-y-3">
              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-muted-foreground">Gastos Totais</span>
                  <span class="font-semibold">{{ formatCurrency(parlamentar.gastoTotal) }}</span>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-muted-foreground">Presença</span>
                  <span class="font-semibold">{{ parlamentar.presenca }}%</span>
                </div>
                <div class="w-full bg-secondary rounded-full h-2">
                  <div
                    class="bg-primary rounded-full h-2 transition-all"
                    :style="{ width: parlamentar.presenca + '%' }"
                  ></div>
                </div>
              </div>

              <div>
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-muted-foreground">Fidelidade Partidária</span>
                  <span class="font-semibold">{{ parlamentar.fidelidadePartidaria }}%</span>
                </div>
                <div class="w-full bg-secondary rounded-full h-2">
                  <div
                    class="bg-chart-2 rounded-full h-2 transition-all"
                    :style="{ width: parlamentar.fidelidadePartidaria + '%' }"
                  ></div>
                </div>
              </div>
            </div>

            <RouterLink 
              :to="'/perfil/' + parlamentar.id" 
              class="btn btn-outline w-full mt-4"
            >
              Ver Perfil Completo
            </RouterLink>
          </div>
        </div>
      </div>

      <div v-if="filteredAndSorted.length === 0" class="card">
        <div class="card-content pt-6 text-center py-12">
          <p class="text-muted-foreground">Nenhum parlamentar encontrado com os filtros selecionados.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Search, TrendingUp, TrendingDown } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import { useMockData } from '../composables/useMockData'

type SortField = 'nome' | 'gastoTotal' | 'presenca' | 'fidelidadePartidaria'
type SortOrder = 'asc' | 'desc'

const mockData = useMockData()

const searchTerm = ref('')
const partidoFilter = ref('Todos')
const estadoFilter = ref('Todos')
const sortField = ref<SortField>('nome')
const sortOrder = ref<SortOrder>('asc')
/* comparação removida: seleção para comparar parlamentares */

const filteredAndSorted = computed(() => {
  let result = [...mockData.parlamentares.value]

  // Filter by search term
  if (searchTerm.value) {
    result = result.filter((p) => 
      p.nome.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  }

  // Filter by party
  if (partidoFilter.value !== 'Todos') {
    result = result.filter((p) => p.partido === partidoFilter.value)
  }

  // Filter by state
  if (estadoFilter.value !== 'Todos') {
    result = result.filter((p) => p.estado === estadoFilter.value)
  }

  // Sort
  result.sort((a, b) => {
    let comparison = 0

    if (sortField.value === 'nome') {
      comparison = a.nome.localeCompare(b.nome)
    } else {
      comparison = a[sortField.value] - b[sortField.value]
    }

    return sortOrder.value === 'asc' ? comparison : -comparison
  })

  return result
})

const getBtnClass = (field: SortField) => {
  return ['btn', sortField.value === field ? 'btn-primary' : 'btn-outline']
}

const toggleSort = (field: SortField) => {
  if (sortField.value === field) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortField.value = field
    sortOrder.value = 'desc'
  }
}

// Funções de comparação removidas (feature descartada)

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
  }).format(value)
}
</script>

<style scoped>
.bg-background {
  background-color: var(--color-white);
}

.text-foreground {
  color: var(--color-gray-900);
}

.text-muted-foreground {
  color: var(--color-gray-600);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.card {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-sm);
}

.card-content {
  padding: 1.5rem;
}

.card:hover {
  box-shadow: var(--shadow-lg);
}

.border-primary {
  border-color: var(--color-primary);
}

.input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-gray-300);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  transition: border-color 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-gray-300);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background: var(--color-white);
  cursor: pointer;
}

.select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: 1px solid transparent;
  justify-content: center;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-white);
}

.btn-primary:hover {
  background: var(--color-primary-dark);
}

.btn-outline {
  border-color: var(--color-gray-300);
  color: var(--color-gray-700);
  background: var(--color-white);
}

.btn-outline:hover {
  background: var(--color-gray-50);
  border-color: var(--color-gray-400);
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.75rem;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.badge {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-secondary {
  background: var(--color-gray-100);
  color: var(--color-gray-800);
}

.badge-outline {
  border: 1px solid var(--color-gray-300);
  color: var(--color-gray-700);
  background: transparent;
}

.checkbox {
  width: 1rem;
  height: 1rem;
  border: 1px solid var(--color-gray-300);
  border-radius: 0.25rem;
  cursor: pointer;
}

.checkbox:checked {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.checkbox:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.bg-secondary {
  background: var(--color-gray-200);
}

.bg-primary {
  background: var(--color-primary);
}

.bg-chart-2 {
  background: var(--color-success);
}

.text-primary {
  color: var(--color-primary);
}

/* Grid utilities */
.grid {
  display: grid;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

.gap-2 {
  gap: 0.5rem;
}

.gap-4 {
  gap: 1rem;
}

.space-y-3 > * + * {
  margin-top: 0.75rem;
}

/* Responsive utilities */
@media (min-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  
  .md\:grid-cols-4 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
  
  .md\:col-span-2 {
    grid-column: span 2 / span 2;
  }
}

@media (min-width: 1024px) {
  .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

/* Flex utilities */
.flex {
  display: flex;
}

.flex-1 {
  flex: 1 1 0%;
}

.flex-wrap {
  flex-wrap: wrap;
}

.items-center {
  align-items: center;
}

.items-start {
  align-items: flex-start;
}

.justify-between {
  justify-content: space-between;
}

.self-center {
  align-self: center;
}

/* Spacing utilities */
.mb-1 {
  margin-bottom: 0.25rem;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.mb-4 {
  margin-bottom: 1rem;
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.mb-8 {
  margin-bottom: 2rem;
}

.mt-4 {
  margin-top: 1rem;
}

.ml-1 {
  margin-left: 0.25rem;
}

.pt-6 {
  padding-top: 1.5rem;
}

.py-8 {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.py-12 {
  padding-top: 3rem;
  padding-bottom: 3rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.pl-9 {
  padding-left: 2.25rem;
}

/* Size utilities */
.w-full {
  width: 100%;
}

.h-2 {
  height: 0.5rem;
}

.h-3 {
  height: 0.75rem;
}

.h-4 {
  height: 1rem;
}

.h-5 {
  height: 1.25rem;
}

/* Text utilities */
.text-sm {
  font-size: 0.875rem;
  line-height: 1.25rem;
}

.text-lg {
  font-size: 1.125rem;
  line-height: 1.75rem;
}

.text-4xl {
  font-size: 2.25rem;
  line-height: 2.5rem;
}

.font-medium {
  font-weight: 500;
}

.font-semibold {
  font-weight: 600;
}

.font-bold {
  font-weight: 700;
}

.text-center {
  text-align: center;
}

/* Position utilities */
.relative {
  position: relative;
}

.absolute {
  position: absolute;
}

.left-3 {
  left: 0.75rem;
}

.top-1\/2 {
  top: 50%;
}

.-translate-y-1\/2 {
  transform: translateY(-50%);
}

/* Border utilities */
.rounded-full {
  border-radius: 9999px;
}

/* Transition utilities */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-shadow {
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.min-h-screen {
  min-height: 100vh;
}
</style>
