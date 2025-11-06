<template>
  <div class="page-wrapper">
    <AppHeader />
    
    <main class="main-content">
      <!-- Header Section -->
      <section class="header-section">
        <div class="container">
          <div class="page-header">
            <h1 class="page-title">Parlamentares</h1>
            <p class="page-subtitle">
              Acompanhe a atuação de {{ mockData.parlamentares.length }} deputados federais
            </p>
          </div>
        </div>
      </section>

      <!-- Search Section -->
      <section class="search-section">
        <div class="container">
          <div class="search-container">
            <div class="search-input-wrapper">
              <Search class="search-icon" />
              <input
                type="text"
                placeholder="Buscar por nome, partido ou estado..."
                v-model="searchTerm"
                class="search-input"
              />
            </div>
          </div>
        </div>
      </section>

      <!-- Results Section -->
      <section class="results-section">
        <div class="container">
          <div class="results-header">
            <h2 class="results-title">
              {{ filteredParlamentares.length }} parlamentares encontrados
            </h2>
          </div>
          
          <div class="parliamentarians-grid">
            <div 
              v-for="parlamentar in filteredParlamentares" 
              :key="parlamentar.id" 
              class="parliamentarian-card"
            >
              <div class="card-header">
                <div class="parliamentarian-info">
                  <RouterLink
                    :to="'/perfil/' + parlamentar.id"
                    class="parliamentarian-name"
                  >
                    {{ parlamentar.nome }}
                  </RouterLink>
                  <p class="parliamentarian-details">
                    {{ parlamentar.partido }} - {{ parlamentar.estado }}
                  </p>
                </div>
              </div>
              
              <div class="card-content">
                <div class="stats-row">
                  <div class="stat-item">
                    <span class="stat-label">Gastos Totais</span>
                    <span class="stat-value">{{ formatCurrency(parlamentar.gastoTotal) }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-label">Presença</span>
                    <span class="stat-value">{{ parlamentar.presenca }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div v-if="filteredParlamentares.length === 0" class="empty-state">
            <div class="empty-state-content">
              <div class="empty-state-icon">
                <Users />
              </div>
              <h3 class="empty-state-title">Nenhum parlamentar encontrado</h3>
              <p class="empty-state-description">
                Tente ajustar os termos de busca ou remova os filtros aplicados.
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Search, Users } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import { useMockData } from '../composables/useMockData'

const mockData = useMockData()
const searchTerm = ref('')

const filteredParlamentares = computed(() => {
  if (!searchTerm.value) {
    return mockData.parlamentares.value
  }
  
  return mockData.parlamentares.value.filter((p) => 
    p.nome.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    p.partido.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    p.estado.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}
</script>

<style scoped>
/* ======================
   ESTRUTURA GERAL 
   ====================== */
.page-wrapper {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc, #f1f5f9);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #1e293b;
}

.main-content {
  margin: 0 auto;
}

/* ======================
   SEÇÃO HEADER 
   ====================== */

/* Header Section */
.header-section {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding: 4rem 0 6rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
}

.page-header {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-gray-900);
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

@media (min-width: 768px) {
  .page-title {
    font-size: 3.5rem;
    margin-bottom: 2rem;
  }
}

.page-subtitle {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  line-height: 1.6;
  max-width: 700px;
  margin: 0 auto;
}

/* ======================
   SEÇÃO DE BUSCA 
   ====================== */
.search-section {
  padding: 4rem 0;
  background: var(--color-white);
}

.search-container {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
  background: var(--color-white);
  padding: 1rem;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-gray-200);
}

.search-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-gray-400);
}

.search-input {
  width: 100%;
  height: 3rem;
  padding-left: 3rem;
  padding-right: 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--color-gray-300);
  color: var(--color-gray-900);
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: var(--color-white);
}

.search-input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search-input::placeholder {
  color: var(--color-gray-500);
}

/* ======================
   SEÇÃO RESULTADOS 
   ====================== */
.results-section {
  padding: 4rem 0;
  background: var(--color-gray-50);
}

.results-header {
  margin-bottom: var(--space-8);
}

.results-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-gray-900);
  text-align: center;
}

/* ======================
   GRID DE PARLAMENTARES 
   ====================== */
.parliamentarians-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(20rem, 1fr));
  gap: var(--space-6);
  margin-top: var(--space-8);
}

.parliamentarian-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-gray-200);
  transition: all 0.2s ease;
  overflow: hidden;
}

.parliamentarian-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary-light);
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-gray-100);
}

.parliamentarian-info {
  text-align: center;
}

.parliamentarian-name {
  display: block;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-primary);
  text-decoration: none;
  margin-bottom: var(--space-2);
  transition: color 0.2s ease;
}

.parliamentarian-name:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

.parliamentarian-details {
  color: var(--color-gray-600);
  font-size: 0.875rem;
  margin: 0;
}

.card-content {
  padding: var(--space-6);
}

.stats-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
}

.stat-item {
  text-align: center;
  padding: var(--space-3);
  background: var(--color-gray-50);
  border-radius: var(--radius-md);
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-gray-600);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-1);
}

.stat-value {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-gray-900);
}

/* ======================
   ESTADO VAZIO 
   ====================== */
.empty-state {
  text-align: center;
  padding: var(--space-16) var(--space-8);
}

.empty-state-content {
  max-width: 24rem;
  margin: 0 auto;
}

.empty-state-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 4rem;
  height: 4rem;
  background: var(--color-gray-100);
  border-radius: 50%;
  margin-bottom: var(--space-6);
  color: var(--color-gray-400);
}

.empty-state-icon svg {
  width: 2rem;
  height: 2rem;
}

.empty-state-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: var(--space-2);
}

.empty-state-description {
  color: var(--color-gray-600);
  line-height: 1.6;
  margin: 0;
}

/* ======================
   DESIGN RESPONSIVO 
   ====================== */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .parliamentarians-grid {
    grid-template-columns: 1fr;
    gap: var(--space-4);
  }
  
  .stats-row {
    grid-template-columns: 1fr;
    gap: var(--space-3);
  }
}

@media (max-width: 640px) {
  .header-section {
    padding: var(--space-12) 0;
  }
  
  .search-section {
    padding: var(--space-8) 0;
  }
  
  .results-section {
    padding: var(--space-8) 0;
  }
}
</style>