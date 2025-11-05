<template>
  <div class="mvp-home">
    <AppHeader />
    
    <main class="main">
      <!-- Hero Section MVP -->
      <section class="hero">
        <div class="hero-content">
          <h1>Transparência Parlamentar</h1>
          <p>Consulte gastos e dados dos deputados federais</p>

          <!-- Search simples -->
          <div class="search">
            <form @submit.prevent="handleSearch" class="search-form">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Buscar deputado..."
                class="search-input"
              />
              <button type="submit" class="search-btn">Buscar</button>
            </form>

            <!-- Sugestões simples -->
            <div v-if="searchQuery.length >= 3" class="suggestions">
              <div v-if="isSearching" class="suggestion-loading">Buscando...</div>
              <div v-else-if="searchResults.length > 0">
                <div 
                  v-for="deputado in searchResults" 
                  :key="deputado.id"
                  @click="selectSuggestion(deputado)"
                  class="suggestion"
                >
                  {{ deputado.nome_civil }} ({{ deputado.uf }})
                </div>
              </div>
              <div v-else class="suggestion-empty">Nenhum deputado encontrado</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Stats básicos -->
      <section class="stats">
        <div class="container">
          <h2>Indicadores</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <h3>Gastos Totais</h3>
              <p>{{ formatCurrency(totalGastos) }}</p>
              <small>Últimos 12 meses</small>
            </div>
            <div class="stat-card">
              <h3>Presença Média</h3>
              <p>{{ presencaMedia }}%</p>
              <small>Sessões plenárias</small>
            </div>
            <div class="stat-card">
              <h3>Deputados</h3>
              <p>{{ totalDeputados }}</p>
              <small>Monitorados</small>
            </div>
          </div>
        </div>
      </section>

      <!-- Links rápidos -->
      <section class="links">
        <div class="container">
          <h2>Navegação</h2>
          <div class="link-grid">
            <RouterLink to="/parlamentares" class="link-card">
              <h3>Deputados</h3>
              <p>Lista completa dos deputados</p>
            </RouterLink>
            <RouterLink to="/dashboard" class="link-card">
              <h3>Dashboard</h3>
              <p>Gráficos e análises</p>
            </RouterLink>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'
import { useMockData } from '../composables/useMockData'

const router = useRouter()
const mockData = useMockData()

const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// Stats computadas
const totalGastos = computed(() => {
  return mockData.parlamentares.value.reduce((total, p) => total + p.gastoTotal, 0)
})

const presencaMedia = computed(() => {
  const total = mockData.parlamentares.value.reduce((sum, p) => sum + p.presenca, 0)
  return Math.round(total / mockData.parlamentares.value.length)
})

const totalDeputados = computed(() => mockData.parlamentares.value.length)

// Search básico
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/parlamentares?search=${encodeURIComponent(searchQuery.value)}`)
  }
}

// Busca real na API
const performSearch = async (query: string) => {
  if (query.length < 3) {
    searchResults.value = []
    return
  }

  isSearching.value = true
  
  try {
    const response = await fetch(`http://localhost:8000/api/deputados/buscar?nome=${encodeURIComponent(query)}`)
    const data = await response.json()
    
    searchResults.value = data.resultados || []
  } catch (error) {
    console.error('Erro ao buscar deputados:', error)
    searchResults.value = []
  } finally {
    isSearching.value = false
  }
}

// Watcher para busca em tempo real
import { watch } from 'vue'
watch(searchQuery, (newQuery) => {
  performSearch(newQuery)
})

const selectSuggestion = (deputado) => {
  router.push(`/perfil/${deputado.id}`)
}

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    notation: 'compact'
  }).format(value)
}
</script>

<style scoped>
.mvp-home {
  min-height: 100vh;
  background: #f8f9fa;
}

.main {
  padding: 0;
}

.hero {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.hero-content h1 {
  font-size: 2.5rem;
  margin-bottom: 16px;
  font-weight: 700;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.9;
}

.search {
  max-width: 500px;
  margin: 0 auto;
  position: relative;
}

.search-form {
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  background: white;
}

.search-btn {
  padding: 12px 24px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.search-btn:hover {
  background: #218838;
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 60px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-top: 8px;
  z-index: 100;
}

.suggestion {
  padding: 12px 16px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  color: #333;
}

.suggestion:hover {
  background: #f8f9fa;
}

.suggestion:last-child {
  border-bottom: none;
}

.suggestion-loading, .suggestion-empty {
  padding: 12px 16px;
  color: #666;
  text-align: center;
}

.stats, .links {
  padding: 60px 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.container h2 {
  text-align: center;
  margin-bottom: 40px;
  font-size: 2rem;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
}

.stat-card {
  background: white;
  padding: 30px 20px;
  border-radius: 12px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-card h3 {
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
  font-weight: 500;
}

.stat-card p {
  font-size: 2rem;
  font-weight: 700;
  color: #007bff;
  margin-bottom: 5px;
}

.stat-card small {
  color: #888;
  font-size: 0.85rem;
}

.link-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 30px;
}

.link-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.link-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.link-card h3 {
  font-size: 1.3rem;
  color: #007bff;
  margin-bottom: 10px;
}

.link-card p {
  color: #666;
  margin: 0;
}

@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-content p {
    font-size: 1rem;
  }
  
  .search-form {
    flex-direction: column;
  }
}
</style>