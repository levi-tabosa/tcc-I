<template>
  <div class="page-wrapper">
    <main class="main-content">
      
      <!-- Header com Busca -->
      <section class="header-section">
        <div class="container">
          <div class="header-content">
            <h1 class="page-title">Parlamentares</h1>
            <p class="page-subtitle">Consulte a lista completa de deputados em exercício</p>
            
            <!-- Barra de Busca -->
            <div class="search-container">
              <div class="search-box">
                <Search class="search-icon" />
                <input 
                  v-model="termoBusca" 
                  type="text" 
                  placeholder="Busque por nome, partido ou estado..." 
                  class="search-input"
                >
                <button v-if="termoBusca" @click="termoBusca = ''" class="clear-btn">
                  <X class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Lista de Cards -->
      <section class="list-section">
        <div class="container">
          
          <!-- Loading -->
          <div v-if="loading" class="text-center py-12">
            <div class="loading-spinner mx-auto mb-4"></div>
            <p class="text-gray-500">Carregando lista de parlamentares...</p>
          </div>

          <!-- Erro -->
          <div v-else-if="deputados.length === 0" class="text-center py-12">
            <UserX class="w-12 h-12 mx-auto text-gray-300 mb-4" />
            <h3 class="text-lg font-semibold text-gray-700">Nenhum dado disponível</h3>
            <p class="text-gray-500">Verifique se a API está respondendo ou abra o console (F12)</p>
          </div>

          <!-- Sem Resultados de Busca -->
          <div v-else-if="deputadosFiltrados.length === 0" class="text-center py-12">
            <UserX class="w-12 h-12 mx-auto text-gray-300 mb-4" />
            <h3 class="text-lg font-semibold text-gray-700">Nenhum parlamentar encontrado</h3>
            <p class="text-gray-500">Tente buscar por outro termo.</p>
          </div>

          <!-- Grid de Deputados -->
          <div v-else>
            <div class="grid-deputados">
              <div 
                v-for="deputado in deputadosPaginados" 
                :key="deputado.id" 
                class="deputado-card"
              >
                <!-- Cabeçalho do Card (Foto e Partido) -->
                <div class="card-header">
                  <div class="partido-badge">{{ deputado.sigla_partido }}</div>
                  <div class="estado-badge">{{ deputado.uf }}</div>
                  <img 
                    :src="`https://www.camara.leg.br/internet/deputado/bandep/${deputado.id}.jpg`" 
                    @error="$event.target.src = 'https://via.placeholder.com/200x200?text=Foto'"
                    :alt="deputado.nome_civil"
                    class="deputado-foto"
                  />
                </div>

                <!-- Corpo do Card -->
                <div class="card-body">
                  <h3 class="deputado-nome" :title="deputado.nome_civil">
                    {{ formatarNome(deputado.nome_civil) }}
                  </h3>
                  <p class="deputado-full-name">{{ deputado.nome_civil }}</p>
                  
                  <router-link :to="`/deputados/${deputado.id}`" class="btn-perfil">
                    Ver Perfil
                    <ArrowRight class="w-4 h-4" />
                  </router-link>
                </div>
              </div>
            </div>

            <!-- Paginação -->
            <div class="pagination-container" v-if="totalPages > 1">
              <button 
                @click="paginaAtual--" 
                :disabled="paginaAtual === 1"
                class="page-btn"
              >
                <ChevronLeft class="w-5 h-5" />
              </button>
              
              <span class="page-info">
                Página {{ paginaAtual }} de {{ totalPages }}
              </span>
              
              <button 
                @click="paginaAtual++" 
                :disabled="paginaAtual === totalPages"
                class="page-btn"
              >
                <ChevronRight class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </section>

    </main>
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AppFooter from '@/components/AppFooter.vue'
import { Search, ArrowRight, ChevronLeft, ChevronRight } from 'lucide-vue-next'

// Estado
const deputados = ref([])
const loading = ref(true)
const termoBusca = ref('')
const paginaAtual = ref(1)
const itensPorPagina = 12

const apiUrl = import.meta.env.VITE_BACKEND_URL 

// Fetch dos Dados
const fetchDeputados = async () => {
  loading.value = true
  console.log('Iniciando busca de deputados...')
  
  try {
    const response = await fetch(`${apiUrl}/api/deputados/`)
    console.log('Status da resposta:', response.status)
    
    if (!response.ok) {
      throw new Error(`Erro ao buscar: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('Dados recebidos:', data)
    console.log('Total de deputados:', data.length)
    
    deputados.value = data
  } catch (error) {
    console.error("Erro ao buscar deputados:", error)
  } finally {
    loading.value = false
    console.log('Loading finalizado. Total de deputados:', deputados.value.length)
  }
}

// Lógica de Filtragem (Computed)
const deputadosFiltrados = computed(() => {
  if (!termoBusca.value) return deputados.value

  const termo = termoBusca.value.toLowerCase()
  return deputados.value.filter(d => 
    d.nome_civil.toLowerCase().includes(termo) || 
    d.sigla_partido.toLowerCase().includes(termo) ||
    d.uf.toLowerCase().includes(termo)
  )
})

// Lógica de Paginação (Computed)
const totalPages = computed(() => {
  const total = Math.ceil(deputadosFiltrados.value.length / itensPorPagina)
  console.log('Total de páginas:', total, 'Total filtrados:', deputadosFiltrados.value.length)
  return total
})

const deputadosPaginados = computed(() => {
  const inicio = (paginaAtual.value - 1) * itensPorPagina
  const fim = inicio + itensPorPagina
  const paginados = deputadosFiltrados.value.slice(inicio, fim)
  console.log(`Mostrando ${paginados.length} deputados (${inicio + 1} a ${fim})`)
  return paginados
})

// Utilitários
const formatarNome = (nomeCompleto) => {
  // Pega apenas o primeiro e último nome para o título principal (opcional)
  const partes = nomeCompleto.split(' ')
  if (partes.length > 2) {
    return `${partes[0]} ${partes[partes.length - 1]}`
  }
  return nomeCompleto
}

// Resetar página ao buscar
watch(termoBusca, () => {
  paginaAtual.value = 1
})

// Log imediato para verificar se o componente carregou
console.log('Componente Parlamentares montado!')

onMounted(() => {
  console.log('onMounted executado - chamando fetchDeputados')
  fetchDeputados()
})
</script>

<style scoped>
/* Estrutura Base */
.page-wrapper {
  min-height: 100vh;
  background: var(--bg-secondary);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.main-content {
  flex: 1;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

/* Header Section */
.header-section {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
  padding: 4rem 0 2rem;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  letter-spacing: -0.025em;
}

.page-subtitle {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

/* Search Box Styles */
.search-container {
  max-width: 600px;
  margin: 0 auto;
}

.search-box {
  position: relative;
  background: var(--surface-primary);
  border-radius: 9999px;
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border: 1px solid var(--border-primary);
  transition: all 0.2s;
}

.search-box:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.search-icon {
  color: var(--text-tertiary);
  width: 1.25rem;
  height: 1.25rem;
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  color: var(--text-primary);
  background: transparent;
}

.clear-btn {
  color: var(--text-tertiary);
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 50%;
  background: transparent;
  border: none;
}
.clear-btn:hover {
  background: var(--bg-secondary);
  color: var(--text-secondary);
}

/* Grid de Deputados */
.grid-deputados {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 2rem;
  padding: 2rem 0;
}

.deputado-card {
  background: var(--surface-primary);
  border-radius: 1rem;
  overflow: hidden;
  border: 1px solid var(--border-primary);
  transition: transform 0.2s, box-shadow 0.2s;
}

.deputado-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary);
}

/* Header do Card com Foto */
.card-header {
  position: relative;
  height: 200px;
  background: var(--bg-secondary);
  display: flex;
  justify-content: center;
  align-items: flex-end;
  overflow: hidden;
}

.deputado-foto {
  height: 180px; /* Ajuste para a foto ficar "saindo" de baixo */
  width: auto;
  object-fit: cover;
  transition: transform 0.3s;
}

.deputado-card:hover .deputado-foto {
  transform: scale(1.05);
}

.partido-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--surface-primary);
  color: var(--text-primary);
  font-weight: 700;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-primary);
}

.estado-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: var(--color-primary);
  color: white;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
}

/* Corpo do Card */
.card-body {
  padding: 1.5rem;
  text-align: center;
}

.deputado-nome {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.deputado-full-name {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-perfil {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 0.75rem;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  font-weight: 600;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-perfil:hover {
  background: var(--color-primary);
  color: white;
}

/* Paginação */
.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-bottom: 4rem;
}

.page-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  background: var(--surface-primary);
  border: 1px solid var(--border-primary);
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-primary);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-btn:not(:disabled):hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: rgba(59, 130, 246, 0.05);
}

.page-info {
  font-weight: 500;
  color: var(--text-secondary);
}

/* Loading Spinner */
.loading-spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid var(--border-primary);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.text-center {
  text-align: center;
}

.py-12 {
  padding-top: 3rem;
  padding-bottom: 3rem;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.mb-4 {
  margin-bottom: 1rem;
}

.text-gray-500 {
  color: var(--text-secondary);
}

.text-gray-300 {
  color: var(--text-tertiary);
}

.text-lg {
  font-size: 1.125rem;
}

.font-semibold {
  font-weight: 600;
}

.text-gray-700 {
  color: var(--text-primary);
}

.w-12 {
  width: 3rem;
}

.h-12 {
  height: 3rem;
}

.w-4 {
  width: 1rem;
}

.h-4 {
  height: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>