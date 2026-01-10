<template>
  <div class="page-wrapper">
    <main class="main-content">
      <!-- Header Section -->
      <section class="comparison-header-section">
        <div class="container">
          <div class="comparison-header">
            <div class="header-icon-wrapper">
              <BarChart3 class="header-icon" />
            </div>
            <h1 class="comparison-title">Comparativo de Parlamentares</h1>
            <p class="comparison-subtitle">
              Analise e compare gastos, média mensal e categorias de despesas entre dois deputados federais de forma intuitiva.
            </p>
          </div>
        </div>
      </section>

      <!-- Selection Section -->
      <section class="selection-section">
        <div class="container">
          <div class="selection-grid">

            <!-- Parlamentar A -->
            <div class="selector-card" :class="{ 'has-selection': deputado1 }">
              <div class="selector-label">Deputado 1</div>
              
              <div v-if="!deputado1" class="search-mode">
                <div class="selector-icon-wrapper">
                  <UserPlus class="selector-icon" />
                </div>
                <p class="selector-instruction">Busque e selecione o primeiro parlamentar</p>
                <div class="search-wrapper">
                  <div class="search-input-group">
                    <Search class="search-icon-input" />
                    <input 
                      v-model="termoBusca1"
                      @input="buscar(1)"
                      type="text" 
                      placeholder="Digite o nome do deputado..." 
                      class="search-input"
                    />
                  </div>
                  <!-- Resultados da Busca -->
                  <transition name="fade-dropdown">
                    <div v-if="resultados1.length > 0" class="search-results">
                      <div 
                        v-for="dep in resultados1" 
                        :key="dep.id"
                        @click="selecionarDeputado(1, dep)"
                        class="search-result-item"
                      >
                        <img :src="getFotoUrl(dep.id)" class="result-avatar" @error="handleImgError" />
                        <div class="result-info">
                          <div class="result-name">{{ dep.nome_civil }}</div>
                          <div class="result-state">{{ dep.uf }}</div>
                        </div>
                        <ChevronRight class="result-arrow" />
                      </div>
                    </div>
                  </transition>
                </div>
              </div>

              <div v-else class="selected-mode">
                <button @click="removerDeputado(1)" class="remove-button" title="Remover">
                  <X class="remove-icon" />
                </button>
                <div class="selected-avatar-container">
                  <img :src="deputado1.foto" class="selected-avatar" @error="handleImgError" />
                </div>
                <h2 class="selected-name">{{ deputado1.nome }}</h2>
                <div class="selected-tags">
                  <span class="info-tag tag-partido">{{ deputado1.partido }}</span>
                  <span class="info-tag tag-estado">{{ deputado1.estado }}</span>
                </div>
              </div>
            </div>

            <!-- Parlamentar B -->
            <div class="selector-card" :class="{ 'has-selection': deputado2 }">
              <div class="selector-label">Deputado 2</div>
              
              <div v-if="!deputado2" class="search-mode">
                <div class="selector-icon-wrapper">
                  <UserPlus class="selector-icon" />
                </div>
                <p class="selector-instruction">Busque e selecione o segundo parlamentar</p>
                <div class="search-wrapper">
                  <div class="search-input-group">
                    <Search class="search-icon-input" />
                    <input 
                      v-model="termoBusca2"
                      @input="buscar(2)"
                      type="text" 
                      placeholder="Digite o nome do deputado..." 
                      class="search-input"
                    />
                  </div>
                  <!-- Resultados da Busca -->
                  <transition name="fade-dropdown">
                    <div v-if="resultados2.length > 0" class="search-results">
                      <div 
                        v-for="dep in resultados2" 
                        :key="dep.id"
                        @click="selecionarDeputado(2, dep)"
                        class="search-result-item"
                      >
                        <img :src="getFotoUrl(dep.id)" class="result-avatar" @error="handleImgError" />
                        <div class="result-info">
                          <div class="result-name">{{ dep.nome_civil }}</div>
                          <div class="result-state">{{ dep.uf }}</div>
                        </div>
                        <ChevronRight class="result-arrow" />
                      </div>
                    </div>
                  </transition>
                </div>
              </div>

              <div v-else class="selected-mode">
                <button @click="removerDeputado(2)" class="remove-button" title="Remover">
                  <X class="remove-icon" />
                </button>
                <div class="selected-avatar-container">
                  <img :src="deputado2.foto" class="selected-avatar" @error="handleImgError" />
                </div>
                <h2 class="selected-name">{{ deputado2.nome }}</h2>
                <div class="selected-tags">
                  <span class="info-tag tag-partido">{{ deputado2.partido }}</span>
                  <span class="info-tag tag-estado">{{ deputado2.estado }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Comparison Content -->
      <section v-if="deputado1 && deputado2" class="comparison-section">
        <div class="container">
          
          <!-- Stats Overview -->
          <div class="stats-overview-grid">
            <div class="comparison-stat-card">
              <div class="stat-card-icon-wrapper">
                <DollarSign class="stat-card-icon" />
              </div>
              <div class="stat-card-content">
                <p class="stat-card-label">Total Gasto</p>
                <div class="stat-comparison-wrapper">
                  <div class="stat-value-group">
                    <span class="stat-value">{{ formatCurrency(dadosDep1.total) }}</span>
                    <span class="stat-deputy-label">Parlamentar A</span>
                  </div>
                  <div class="stat-divider"></div>
                  <div class="stat-value-group">
                    <span class="stat-value">{{ formatCurrency(dadosDep2.total) }}</span>
                    <span class="stat-deputy-label">Parlamentar B</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="comparison-stat-card">
              <div class="stat-card-icon-wrapper">
                <TrendingUp class="stat-card-icon" />
              </div>
              <div class="stat-card-content">
                <p class="stat-card-label">Média Mensal</p>
                <div class="stat-comparison-wrapper">
                  <div class="stat-value-group">
                    <span class="stat-value">{{ formatCurrency(dadosDep1.media) }}</span>
                    <span class="stat-deputy-label">Parlamentar A</span>
                  </div>
                  <div class="stat-divider"></div>
                  <div class="stat-value-group">
                    <span class="stat-value">{{ formatCurrency(dadosDep2.media) }}</span>
                    <span class="stat-deputy-label">Parlamentar B</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="comparison-stat-card">
              <div class="stat-card-icon-wrapper">
                <FileText class="stat-card-icon" />
              </div>
              <div class="stat-card-content">
                <p class="stat-card-label">Notas Fiscais</p>
                <div class="stat-comparison-wrapper">
                  <div class="stat-value-group">
                    <span class="stat-value">{{ dadosDep1.qtd }}</span>
                    <span class="stat-deputy-label">Parlamentar A</span>
                  </div>
                  <div class="stat-divider"></div>
                  <div class="stat-value-group">
                    <span class="stat-value">{{ dadosDep2.qtd }}</span>
                    <span class="stat-deputy-label">Parlamentar B</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Visual Comparison Bars -->
          <div class="comparison-bars-container">
            <div class="section-header-divider">
              <span class="divider-line"></span>
              <h3 class="section-divider-title">Comparação Visual</h3>
              <span class="divider-line"></span>
            </div>
            
            <div class="comparison-bars-content">
              <!-- Total Gasto -->
              <div class="comparison-bar-wrapper">
                <div class="comparison-bar-header">
                  <div class="bar-deputy-info">
                    <span class="deputy-label">{{ deputado1.nome }}</span>
                    <span class="deputy-value">{{ formatCurrency(dadosDep1.total) }}</span>
                  </div>
                  <div class="bar-metric-label">
                    <span>GASTOS TOTAIS</span>
                  </div>
                  <div class="bar-deputy-info text-right">
                    <span class="deputy-label">{{ deputado2.nome }}</span>
                    <span class="deputy-value">{{ formatCurrency(dadosDep2.total) }}</span>
                  </div>
                </div>
                <div class="dual-progress-bar">
                  <div class="progress-half progress-left">
                    <div class="progress-fill progress-blue" :style="{ width: getPorcentagem(dadosDep1.total) + '%' }"></div>
                  </div>
                  <div class="progress-half progress-right">
                    <div class="progress-fill progress-green" :style="{ width: getPorcentagem(dadosDep2.total) + '%' }"></div>
                  </div>
                </div>
              </div>

              <!-- Média Mensal -->
              <div class="comparison-bar-wrapper">
                <div class="comparison-bar-header">
                  <div class="bar-deputy-info">
                    <span class="deputy-value">{{ formatCurrency(dadosDep1.media) }}</span>
                  </div>
                  <div class="bar-metric-label">
                    <span>MÉDIA MENSAL</span>
                  </div>
                  <div class="bar-deputy-info text-right">
                    <span class="deputy-value">{{ formatCurrency(dadosDep2.media) }}</span>
                  </div>
                </div>
                <div class="dual-progress-bar">
                  <div class="progress-half progress-left">
                    <div class="progress-fill progress-blue" :style="{ width: getPorcentagemMedia(dadosDep1.media) + '%' }"></div>
                  </div>
                  <div class="progress-half progress-right">
                    <div class="progress-fill progress-green" :style="{ width: getPorcentagemMedia(dadosDep2.media) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Categories Comparison -->
          <div class="categories-comparison-grid">
            <!-- Deputado 1 Categories -->
            <div class="category-comparison-card">
              <div class="category-card-accent accent-blue"></div>
              <div class="category-card-header">
                <Award class="category-icon" />
                <h4 class="category-title">Principais Categorias</h4>
              </div>
              <div class="category-list">
                <div v-for="cat in dadosDep1.topCategorias" :key="cat.tipo" class="category-list-item">
                  <div class="category-item-header">
                    <span class="category-name">{{ cat.tipo }}</span>
                    <span class="category-value">{{ formatCurrency(cat.total) }}</span>
                  </div>
                  <div class="category-progress-track">
                    <div class="category-progress-fill category-blue" :style="{ width: (cat.total / dadosDep1.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Deputado 2 Categories -->
            <div class="category-comparison-card">
              <div class="category-card-accent accent-green"></div>
              <div class="category-card-header">
                <Award class="category-icon" />
                <h4 class="category-title">Principais Categorias</h4>
              </div>
              <div class="category-list">
                <div v-for="cat in dadosDep2.topCategorias" :key="cat.tipo" class="category-list-item">
                  <div class="category-item-header">
                    <span class="category-name">{{ cat.tipo }}</span>
                    <span class="category-value">{{ formatCurrency(cat.total) }}</span>
                  </div>
                  <div class="category-progress-track">
                    <div class="category-progress-fill category-green" :style="{ width: (cat.total / dadosDep2.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Empty State -->
      <section v-else class="empty-state-section">
        <div class="container">
          <div class="empty-state-content">
            <div class="empty-state-icon-wrapper">
              <Users class="empty-state-icon" />
            </div>
            <h3 class="empty-state-title">Selecione dois deputados para comparar</h3>
            <p class="empty-state-description">
              Use os seletores acima para escolher dois deputados federais e visualizar uma comparação detalhada de seus gastos, médias mensais e categorias de despesas.
            </p>
          </div>
        </div>
      </section>

    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  UserPlus, X, DollarSign, BarChart3, Search, 
  ChevronRight, TrendingUp, FileText, Award, Users, 
  Brackets
} from 'lucide-vue-next'
import AppFooter from '@/components/AppFooter.vue'

// --- Interfaces ---
interface DeputadoBusca {
  id: number
  nome_civil: string
  uf: string
}

interface DeputadoCompleto {
  id: number
  nome: string
  foto: string
  partido: string
  estado: string
}

// --- Estado ---
const termoBusca1 = ref('')
const termoBusca2 = ref('')
const resultados1 = ref<DeputadoBusca[]>([])
const resultados2 = ref<DeputadoBusca[]>([])

const deputado1 = ref<DeputadoCompleto | null>(null)
const deputado2 = ref<DeputadoCompleto | null>(null)

// Dados processados das despesas
const dadosDep1 = ref({ total: 0, media: 0, qtd: 0, topCategorias: [] as any[] })
const dadosDep2 = ref({ total: 0, media: 0, qtd: 0, topCategorias: [] as any[] })

const getFotoUrl = (id: number) => `https://www.camara.leg.br/internet/deputado/bandep/${id}.jpg`

const handleImgError = (e: Event) => {
  (e.target as HTMLImageElement).src = 'https://via.placeholder.com/150/f1f5f9/94a3b8?text=Foto'
}

const apiUrl = import.meta.env.VITE_BACKEND_URL 
// --- Funções de Busca ---
const buscar = async (slot: number) => {
  const termo = slot === 1 ? termoBusca1.value : termoBusca2.value
  if (termo.length < 2) {
    if (slot === 1) resultados1.value = []
    else resultados2.value = []
    return
  }

  try {
    const res = await fetch(`${apiUrl}/api/deputados/buscar?nome=${termo}`)
    const data = await res.json()
    if (slot === 1) resultados1.value = data.resultados
    else resultados2.value = data.resultados
  } catch (err) {
    console.error(err)
  }
}

// --- Selecionar e Carregar Dados Completos ---
const selecionarDeputado = async (slot: number, depBasic: DeputadoBusca) => {
  // 1. Limpa busca
  if (slot === 1) { termoBusca1.value = ''; resultados1.value = [] }
  else { termoBusca2.value = ''; resultados2.value = [] }

  try {
    // 2. Busca Perfil Completo
    const resPerfil = await fetch(`${apiUrl}/api/deputados/${depBasic.id}`)
    const perfil = await resPerfil.json()
    
    const objDeputado = {
      id: perfil.id,
      nome: perfil.nome_civil,
      foto: perfil.foto || getFotoUrl(perfil.id),
      partido: perfil.sigla_partido,
      estado: perfil.uf_nascimento
    }

    if (slot === 1) deputado1.value = objDeputado
    else deputado2.value = objDeputado

    // 3. Busca e Processa Despesas
    carregarDespesas(slot, depBasic.id)

  } catch (err) {
    console.error("Erro ao carregar detalhes", err)
  }
}

const carregarDespesas = async (slot: number, id: number) => {
  try {
    const res = await fetch(`${apiUrl}/api/deputados/${id}/despesas`)
    const data = await res.json()
    const despesas = data.despesas || []

    // Cálculos
    const total = despesas.reduce((acc: number, d: any) => acc + d.valor, 0)
    const meses = new Set(despesas.map((d: any) => `${d.ano}-${d.mes}`)).size
    const media = meses > 0 ? total / meses : 0

    // Categorias
    const cats = despesas.reduce((acc: any, d: any) => {
      acc[d.tipo_despesa] = (acc[d.tipo_despesa] || 0) + d.valor
      return acc
    }, {})
    
    const topCategorias = Object.entries(cats)
      .map(([tipo, val]) => ({ tipo, total: Number(val) }))
      .sort((a, b) => b.total - a.total)
      .slice(0, 5)

    const stats = { total, media, qtd: despesas.length, topCategorias }

    if (slot === 1) dadosDep1.value = stats
    else dadosDep2.value = stats

  } catch (err) {
    console.error(err)
  }
}

const removerDeputado = (slot: number) => {
  if (slot === 1) deputado1.value = null
  else deputado2.value = null
}

// --- Utilitários de Visualização ---
const getPorcentagem = (valor: number) => {
  const max = Math.max(dadosDep1.value.total, dadosDep2.value.total)
  if (max === 0) return 0
  return (valor / max) * 100
}

const getPorcentagemMedia = (valor: number) => {
  const max = Math.max(dadosDep1.value.media, dadosDep2.value.media)
  if (max === 0) return 0
  return (valor / max) * 100
}

const formatCurrency = (val: number) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 }).format(val)
}
</script>

<style scoped>
/* ===========================
   ANIMATIONS & TRANSITIONS
   =========================== */
.fade-dropdown-enter-active,
.fade-dropdown-leave-active {
  transition: all 0.2s ease;
}

.fade-dropdown-enter-from,
.fade-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* ===========================
   HEADER SECTION
   =========================== */
.comparison-header-section {
  padding: var(--space-16) 0 var(--space-12);
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
}

.comparison-header {
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
}

.header-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  background: var(--color-primary);
  border-radius: var(--radius-2xl);
  margin-bottom: var(--space-6);
  box-shadow: var(--shadow-xl);
}

.header-icon {
  width: 40px;
  height: 40px;
  color: white;
}

.comparison-title {
  font-size: var(--font-size-4xl);
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: var(--space-4);
  line-height: 1.2;
}

.comparison-subtitle {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ===========================
   SELECTION SECTION
   =========================== */
.selection-section {
  padding: var(--space-12) 0;
  position: relative;
}

.selection-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  position: relative;
}

@media (max-width: 768px) {
  .selection-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}

/* Selector Cards */
.selector-card {
  background: var(--card-bg);
  border: 2px solid var(--border-primary);
  border-radius: var(--radius-xl);
  min-height: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  padding: 2rem;
  position: relative;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--shadow-sm);
}

.selector-label {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-primary);
  color: white;
  padding: 0.35rem 1.25rem;
  border-radius: var(--radius-full);
  font-size: var(--font-size-sm);
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.selector-card.has-selection {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-xl);
  background: var(--card-hover-bg);
}

.selector-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.selector-card.has-selection:hover {
  box-shadow: 0 20px 40px -10px rgba(37, 99, 235, 0.15);
}

/* Search Mode */
.search-mode {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 1rem;
}

.selector-icon-wrapper {
  width: 64px;
  height: 64px;
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-4);
  box-shadow: var(--shadow-md);
}

.selector-icon {
  width: 32px;
  height: 32px;
  color: white;
}

.selector-instruction {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
  text-align: center;
  line-height: 1.5;
}

.search-wrapper {
  width: 100%;
  position: relative;
}

.search-input-group {
  position: relative;
  width: 100%;
}

.search-icon-input {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-tertiary);
  width: 20px;
  height: 20px;
  z-index: 1;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3.5rem;
  background-color: var(--surface-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  outline: none;
  font-size: var(--font-size-base);
  font-weight: 500;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: var(--text-tertiary);
}

.search-input:focus {
  border-color: var(--color-primary);
  background-color: var(--surface-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Search Results */
.search-results {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  background: var(--surface-primary);
  border: 1px solid var(--border-primary);
  border-radius: var(--radius-xl);
  overflow: hidden;
  max-height: 300px;
  overflow-y: auto;
  z-index: 50;
  box-shadow: var(--shadow-xl);
}

.search-results::-webkit-scrollbar {
  width: 6px;
}

.search-results::-webkit-scrollbar-track {
  background: transparent;
}

.search-results::-webkit-scrollbar-thumb {
  background: var(--border-secondary);
  border-radius: 10px;
}

.search-result-item {
  padding: 1rem 1.25rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: background 0.15s ease;
  border-bottom: 1px solid var(--border-primary);
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background-color: var(--surface-secondary);
}

.result-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-lg);
  object-fit: cover;
  background: var(--surface-secondary);
  border: 2px solid var(--border-primary);
}

.result-info {
  flex: 1;
  min-width: 0;
}

.result-name {
  font-weight: 700;
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  margin-bottom: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.result-state {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
  font-weight: 600;
}

.result-arrow {
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  flex-shrink: 0;
}

/* Selected Mode */
.selected-mode {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeInUp 0.4s ease;
  padding-top: 1rem;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.remove-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--color-error);
  color: white;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-lg);
  cursor: pointer;
  border: none;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-md);
  z-index: 10;
}

.remove-button:hover {
  transform: scale(1.1) rotate(90deg);
  background: #b91c1c;
}

.remove-icon {
  width: 20px;
  height: 20px;
}

.selected-avatar-container {
  position: relative;
  padding: 5px;
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  border-radius: 50%;
  box-shadow: var(--shadow-lg);
  margin-bottom: var(--space-4);
}

.selected-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid white;
  display: block;
}

.selected-name {
  font-size: var(--font-size-xl);
  font-weight: 800;
  color: var(--text-primary);
  text-align: center;
  line-height: 1.3;
  margin-bottom: var(--space-3);
  padding: 0 1rem;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
}

.info-tag {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-lg);
  font-size: var(--font-size-sm);
  font-weight: 700;
  letter-spacing: 0.02em;
}

.tag-partido {
  background: var(--color-primary);
  color: white;
}

.tag-estado {
  background: var(--surface-secondary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
}

/* ===========================
   COMPARISON SECTION
   =========================== */
.comparison-section {
  padding: var(--space-12) 0;
  animation: fadeInUp 0.5s ease;
}

/* Stats Overview */
.stats-overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: var(--space-12);
}

.comparison-stat-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.comparison-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.stat-card-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-lg);
  background: linear-gradient(135deg, var(--color-primary-light), var(--color-primary));
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-card-icon {
  width: 28px;
  height: 28px;
  color: white;
}

.stat-card-content {
  flex: 1;
  min-width: 0;
}

.stat-card-label {
  font-size: var(--font-size-xs);
  font-weight: 800;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--space-3);
}

.stat-comparison-wrapper {
  display: flex;
  align-items: center;
  gap: 1rem;
  justify-content: space-between;
}

.stat-value-group {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.stat-value {
  font-size: var(--font-size-lg);
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
}

.stat-deputy-label {
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--text-tertiary);
  text-transform: uppercase;
}

.stat-divider {
  width: 1px;
  height: 36px;
  background: var(--border-primary);
  flex-shrink: 0;
}

/* ===========================
   COMPARISON BARS
   =========================== */
.comparison-bars-container {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: 2.5rem 2rem;
  margin-bottom: var(--space-12);
  box-shadow: var(--shadow-sm);
}

.section-header-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.divider-line {
  height: 2px;
  width: 60px;
  background: linear-gradient(90deg, transparent, var(--border-primary), transparent);
}

.section-divider-title {
  font-size: var(--font-size-sm);
  font-weight: 800;
  color: var(--text-primary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

.comparison-bars-content {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
}

.comparison-bar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.comparison-bar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.bar-deputy-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.bar-deputy-info.text-right {
  align-items: flex-end;
}

.deputy-label {
  font-size: var(--font-size-xs);
  font-weight: 700;
  color: var(--text-secondary);
  text-transform: uppercase;
}

.deputy-value {
  font-size: var(--font-size-xl);
  font-weight: 800;
  color: var(--text-primary);
}

.bar-metric-label {
  text-align: center;
  padding-bottom: 0.25rem;
}

.bar-metric-label span {
  font-size: 0.7rem;
  font-weight: 800;
  color: var(--text-tertiary);
  letter-spacing: 0.05em;
}

/* Dual Progress Bar */
.dual-progress-bar {
  height: 48px;
  display: flex;
  gap: 6px;
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.progress-half {
  flex: 1;
  background: var(--surface-secondary);
  border-radius: var(--radius-lg);
  overflow: hidden;
  position: relative;
}

.progress-fill {
  height: 100%;
  transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
  border-radius: var(--radius-lg);
}

.progress-blue {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.progress-green {
  background: linear-gradient(270deg, #10b981, #34d399);
}

.progress-left .progress-fill {
  float: right;
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
}

.progress-right .progress-fill {
  float: left;
  border-radius: var(--radius-lg) 0 0 var(--radius-lg);
}

/* ===========================
   CATEGORIES COMPARISON
   =========================== */
.categories-comparison-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: var(--space-12);
}

.category-comparison-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all 0.3s ease;
}

.category-comparison-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.category-card-accent {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.accent-blue {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.accent-green {
  background: linear-gradient(90deg, #10b981, #34d399);
}

.category-card-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 2rem;
  padding-top: 0.5rem;
}

.category-icon {
  width: 24px;
  height: 24px;
  color: var(--color-primary);
}

.category-title {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.category-list-item {
  transition: transform 0.2s ease;
}

.category-list-item:hover {
  transform: translateX(6px);
}

.category-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
  gap: 1rem;
}

.category-name {
  font-size: var(--font-size-sm);
  font-weight: 700;
  color: var(--text-secondary);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.category-value {
  font-size: var(--font-size-sm);
  font-weight: 800;
  color: var(--text-primary);
  flex-shrink: 0;
}

.category-progress-track {
  height: 8px;
  background: var(--surface-secondary);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.category-progress-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
}

.category-blue {
  background: linear-gradient(90deg, #3b82f6, #60a5fa);
}

.category-green {
  background: linear-gradient(90deg, #10b981, #34d399);
}

/* ===========================
   EMPTY STATE
   =========================== */
.empty-state-section {
  padding: var(--space-20) 0;
}

.empty-state-content {
  text-align: center;
  padding: 5rem 2rem;
  background: var(--surface-secondary);
  border-radius: var(--radius-2xl);
  border: 2px dashed var(--border-primary);
  max-width: 600px;
  margin: 0 auto;
}

.empty-state-icon-wrapper {
  display: inline-flex;
  padding: 2rem;
  background: var(--surface-primary);
  border-radius: var(--radius-2xl);
  margin-bottom: 2rem;
  box-shadow: var(--shadow-lg);
}

.empty-state-icon {
  width: 64px;
  height: 64px;
  color: var(--text-tertiary);
}

.empty-state-title {
  font-size: var(--font-size-2xl);
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

.empty-state-description {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  line-height: 1.6;
}

/* ===========================
   RESPONSIVE ADJUSTMENTS
   =========================== */
@media (max-width: 768px) {
  .comparison-title {
    font-size: var(--font-size-3xl);
  }

  .stats-overview-grid {
    grid-template-columns: 1fr;
  }

  .comparison-bar-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .bar-deputy-info.text-right {
    align-items: flex-start;
  }

  .categories-comparison-grid {
    grid-template-columns: 1fr;
  }

  .selector-card {
    padding: 2rem 1.5rem;
    min-height: 380px;
  }

  .stat-comparison-wrapper {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .stat-divider {
    width: 100%;
    height: 1px;
  }
}

@media (max-width: 640px) {
  .comparison-header-section {
    padding: var(--space-12) 0 var(--space-8);
  }

  .header-icon-wrapper {
    width: 64px;
    height: 64px;
  }

  .header-icon {
    width: 32px;
    height: 32px;
  }

  .comparison-title {
    font-size: var(--font-size-2xl);
  }

  .comparison-subtitle {
    font-size: var(--font-size-base);
  }

  .deputy-value {
    font-size: var(--font-size-lg);
  }

  .dual-progress-bar {
    height: 36px;
  }

  .selector-card {
    min-height: 350px;
  }

  .selected-avatar {
    width: 100px;
    height: 100px;
  }

  .selected-name {
    font-size: var(--font-size-lg);
  }
}
</style>