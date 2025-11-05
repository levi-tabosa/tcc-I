<template>
  <div class="mvp-container">
    <AppHeader />
    <div class="content">
      <div class="header">
        <h1>Deputados</h1>
        <p>{{ mockData.parlamentares.length }} deputados</p>
      </div>

      <div class="search-box">
        <input
          type="text"
          placeholder="Buscar deputado..."
          v-model="searchTerm"
          class="search-input"
        />
      </div>

      <div class="results">
        <div 
          v-for="parlamentar in filteredParlamentares" 
          :key="parlamentar.id" 
          class="item"
        >
          <div class="info">
            <RouterLink
              :to="'/perfil/' + parlamentar.id"
              class="name"
            >
              {{ parlamentar.nome }}
            </RouterLink>
            <p class="details">{{ parlamentar.partido }} - {{ parlamentar.estado }}</p>
          </div>
          <div class="stats">
            <span>Gastos: {{ formatCurrency(parlamentar.gastoTotal) }}</span>
            <span>Presença: {{ parlamentar.presenca }}%</span>
          </div>
        </div>
        
        <div v-if="filteredParlamentares.length === 0" class="empty">
          <p>Nenhum deputado encontrado.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '../components/AppHeader.vue'
import { useMockData } from '../composables/useMockData'

const mockData = useMockData()
const searchTerm = ref('')

const filteredParlamentares = computed(() => {
  if (!searchTerm.value) {
    return mockData.parlamentares.value
  }
  
  return mockData.parlamentares.value.filter((p) => 
    p.nome.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}
</script>

<style scoped>
.mvp-container {
  min-height: 100vh;
  background: #f5f5f5;
}

.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  margin-bottom: 30px;
  text-align: center;
}

.header h1 {
  font-size: 2rem;
  margin-bottom: 10px;
  color: #333;
}

.header p {
  color: #666;
  font-size: 1rem;
}

.search-box {
  margin-bottom: 30px;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  background: white;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}

.results {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.item:last-child {
  border-bottom: none;
}

.item:hover {
  background: #f8f9fa;
}

.info {
  flex: 1;
}

.name {
  font-weight: 600;
  color: #007bff;
  text-decoration: none;
  font-size: 1.1rem;
}

.name:hover {
  text-decoration: underline;
}

.details {
  margin: 4px 0 0 0;
  color: #666;
  font-size: 0.9rem;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: right;
  font-size: 0.85rem;
  color: #555;
}

.empty {
  padding: 40px 20px;
  text-align: center;
  color: #666;
}

@media (max-width: 768px) {
  .item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .stats {
    text-align: left;
  }
}
</style>