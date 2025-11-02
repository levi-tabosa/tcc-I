<template>
  <div class="min-h-screen flex flex-col bg-background">
    <AppHeader />
    
    <main class="flex-1 py-8">
      <div class="container mx-auto px-4 max-w-6xl">
        <!-- Loading -->
        <div v-if="isLoading" class="text-center py-16">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted mb-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
          </div>
          <h2 class="text-2xl font-bold text-foreground mb-2">Carregando...</h2>
          <p class="text-muted-foreground">Buscando dados do parlamentar</p>
        </div>

        <!-- Erro -->
        <div v-else-if="error || !parlamentar" class="text-center py-16">
          <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-muted mb-4">
            <User class="h-8 w-8 text-muted-foreground" />
          </div>
          <h2 class="text-2xl font-bold text-foreground mb-2">
            {{ error || 'Parlamentar não encontrado' }}
          </h2>
          <p class="text-muted-foreground mb-6">
            {{ error ? 'Ocorreu um erro ao carregar os dados' : 'O ID fornecido não corresponde a nenhum parlamentar' }}
          </p>
          <a href="/parlamentares" class="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
            <ArrowLeft class="h-4 w-4" />
            Voltar para lista
          </a>
        </div>

        <!-- Perfil -->
        <div v-else>
          <!-- Header do Perfil -->
          <div class="perfil-header">
            <div class="perfil-header-content">
              <img 
                :src="parlamentar.foto" 
                :alt="parlamentar.nome"
                class="perfil-foto"
                @error="(e) => { (e.target as HTMLImageElement).src = 'https://via.placeholder.com/128x128/e2e8f0/64748b?text=Foto+não+disponível' }"
              />
              <div class="perfil-info">
                <h1 class="perfil-nome">{{ parlamentar.nome }}</h1>
                <p class="perfil-nome-civil">{{ parlamentar.nome_civil }}</p>
                <div class="perfil-tags">
                  <span class="tag tag-primary">
                    {{ parlamentar.partido }}
                  </span>
                  <span class="tag tag-secondary">
                    {{ parlamentar.estado }}
                  </span>
                  <span class="tag tag-secondary">
                    ID: {{ parlamentar.id }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- KPIs -->
          <div class="grid grid-cols-1 md:grid-cols-1 gap-4 mb-6">
            <StatCard
              title="Gasto Total"
              :value="`R$ ${parlamentar.gastoTotal.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`"
              icon="DollarSign"
              trend="neutral"
            />
          </div>

          <!-- Dados Pessoais -->
          <div class="info-section">
            <h2 class="section-title">
              <User class="section-icon" />
              Dados Pessoais
            </h2>
            <div class="info-grid">
              <div class="info-item">
                <label class="info-label">CPF</label>
                <p class="info-value">{{ parlamentar.cpf || 'Não informado' }}</p>
              </div>
              <div class="info-item">
                <label class="info-label">Sexo</label>
                <p class="info-value">{{ parlamentar.sexo === 'M' ? 'Masculino' : parlamentar.sexo === 'F' ? 'Feminino' : 'Não informado' }}</p>
              </div>
              <div class="info-item">
                <label class="info-label">Data de Nascimento</label>
                <p class="info-value">
                  {{ parlamentar.data_nascimento ? formatDate(parlamentar.data_nascimento) + ` (${calcularIdade(parlamentar.data_nascimento)} anos)` : 'Não informado' }}
                </p>
              </div>
              <div class="info-item">
                <label class="info-label">Escolaridade</label>
                <p class="info-value">{{ parlamentar.escolaridade || 'Não informado' }}</p>
              </div>
              <div class="info-item">
                <label class="info-label">Naturalidade</label>
                <p class="info-value">
                  {{ parlamentar.municipio_nascimento && parlamentar.uf_nascimento 
                    ? `${parlamentar.municipio_nascimento} - ${parlamentar.uf_nascimento}` 
                    : 'Não informado' }}
                </p>
              </div>
              <div v-if="parlamentar.email" class="info-item">
                <label class="info-label">E-mail</label>
                <p class="info-value">{{ parlamentar.email }}</p>
              </div>
            </div>
          </div>

          <!-- Informações Políticas -->
          <div class="info-section">
            <h2 class="section-title">
              <Building class="section-icon" />
              Informações Políticas
            </h2>
            <div class="info-grid">
              <div class="info-item">
                <label class="info-label">Partido</label>
                <p class="info-value info-highlight">{{ parlamentar.partido }}</p>
              </div>
              <div class="info-item">
                <label class="info-label">Estado</label>
                <p class="info-value info-highlight">{{ parlamentar.estado }}</p>
              </div>
            </div>
          </div>

          <!-- Fontes -->
          <div class="sources-section">
            <div class="sources-content">
              <Info class="sources-icon" />
              <div class="sources-text">
                <p class="sources-title">Fontes dos Dados</p>
                <p class="sources-description">
                  Todos os dados são coletados de fontes oficiais e atualizados regularmente.
                </p>
                <div class="sources-links">
                  <a 
                    href="https://dadosabertos.camara.leg.br" 
                    target="_blank"
                    class="source-link"
                  >
                    Dados Abertos Câmara
                    <ExternalLink class="link-icon" />
                  </a>
                  <span class="link-separator">•</span>
                  <a 
                    href="/metodologia" 
                    class="source-link"
                  >
                    Ver Metodologia Completa
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Botões de Ação -->
          <div class="action-buttons">
            <a 
              href="/parlamentares"
              class="btn btn-secondary"
            >
              <ArrowLeft class="btn-icon" />
              Voltar para lista
            </a>
            <a 
              :href="`/comparar?ids=${parlamentar.id}`"
              class="btn btn-primary"
            >
              <BarChart3 class="btn-icon" />
              Comparar com outros
            </a>
          </div>
        </div>
      </div>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { User, ArrowLeft, DollarSign, Building, Info, ExternalLink, BarChart3 } from 'lucide-vue-next'
import AppHeader from '../components/AppHeader.vue'
import AppFooter from '../components/AppFooter.vue'
import StatCard from '../components/StatCard.vue'
import { useMockData } from '../composables/useMockData'

// Interface para os dados do parlamentar da API
interface ParlamentarAPI {
  id: number
  nome_civil: string
  nome_parlamentar?: string
  cpf?: string
  sexo?: string
  data_nascimento?: string
  escolaridade?: string
  municipio_nascimento?: string
  uf_nascimento?: string
  uf: string
  sigla_partido?: string
  email?: string
  foto?: string
}

// Interface para os dados completos do parlamentar (incluindo dados calculados)
interface ParlamentarCompleto extends ParlamentarAPI {
  nome: string
  partido: string
  estado: string
  gastoTotal: number
}

const route = useRoute()
const { parlamentares } = useMockData()

// Estado para os dados do parlamentar
const parlamentarAPI = ref<ParlamentarAPI | null>(null)
const isLoading = ref(false)
const error = ref<string | null>(null)

// Função para buscar dados do parlamentar específico da API
const fetchParlamentar = async (id: number) => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await fetch(`http://localhost:8000/api/deputados/${id}`)
    if (!response.ok) {
      throw new Error('Parlamentar não encontrado')
    }
    
    const data = await response.json()
    parlamentarAPI.value = data
  } catch (err: any) {
    console.error('Erro ao buscar parlamentar:', err)
    error.value = err.message
    parlamentarAPI.value = null
  } finally {
    isLoading.value = false
  }
}

// Computed para combinar dados da API com dados mockados
const parlamentar = computed((): ParlamentarCompleto | null => {
  if (!parlamentarAPI.value) return null
  
  // Tentar encontrar dados complementares nos dados mockados
  const dadosMock = parlamentares.value.find(p => Number(p.id) === parlamentarAPI.value!.id)
  
  return {
    ...parlamentarAPI.value,
    nome: parlamentarAPI.value.nome_parlamentar || parlamentarAPI.value.nome_civil,
    partido: parlamentarAPI.value.sigla_partido || 'S/P',
    estado: parlamentarAPI.value.uf,
    foto: parlamentarAPI.value.foto || `https://www.camara.leg.br/internet/deputado/bandep/${parlamentarAPI.value.id}.jpg`,
    // Usar dados mockados se disponíveis, senão valores padrão
    gastoTotal: dadosMock?.gastoTotal || Math.floor(Math.random() * 100000) + 50000
  }
})

// Buscar dados quando o componente for montado ou quando o ID mudar
onMounted(() => {
  const id = Number(route.params.id)
  if (id) {
    fetchParlamentar(id)
  }
})

// Observar mudanças no ID da rota
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchParlamentar(Number(newId))
  }
})

const formatDate = (dateString: string) => {
  if (!dateString) return 'Não informado'
  try {
    const date = new Date(dateString)
    if (isNaN(date.getTime())) return 'Data inválida'
    return date.toLocaleDateString('pt-BR', { 
      day: '2-digit', 
      month: 'long', 
      year: 'numeric' 
    })
  } catch {
    return 'Data inválida'
  }
}

const calcularIdade = (dateString: string) => {
  if (!dateString) return 0
  try {
    const nascimento = new Date(dateString)
    if (isNaN(nascimento.getTime())) return 0
    const hoje = new Date()
    let idade = hoje.getFullYear() - nascimento.getFullYear()
    const mes = hoje.getMonth() - nascimento.getMonth()
    if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
      idade--
    }
    return idade
  } catch {
    return 0
  }
}
</script>

<style scoped>
/* ======================
   BASE STYLES 
   ====================== */
.min-h-screen {
  min-height: 100vh;
}

.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.flex-1 {
  flex: 1;
}

.bg-background {
  background-color: var(--color-white);
}

.py-8 {
  padding-top: 2rem;
  padding-bottom: 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.max-w-6xl {
  max-width: 72rem;
}

/* ======================
   LOADING & ERROR STATES 
   ====================== */
.text-center {
  text-align: center;
}

.py-16 {
  padding-top: 4rem;
  padding-bottom: 4rem;
}

.inline-flex {
  display: inline-flex;
}

.items-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.w-16 {
  width: 4rem;
}

.h-16 {
  height: 4rem;
}

.rounded-full {
  border-radius: 9999px;
}

.bg-muted {
  background-color: var(--color-gray-100);
}

.mb-4 {
  margin-bottom: 1rem;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.h-8 {
  height: 2rem;
}

.w-8 {
  width: 2rem;
}

.border-b-2 {
  border-bottom-width: 2px;
}

.border-primary {
  border-color: var(--color-primary);
}

.text-2xl {
  font-size: 1.5rem;
}

.font-bold {
  font-weight: 700;
}

.text-foreground {
  color: var(--color-gray-900);
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.text-muted-foreground {
  color: var(--color-gray-600);
}

.mb-6 {
  margin-bottom: 1.5rem;
}

.gap-2 {
  gap: 0.5rem;
}

.px-6 {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}

.py-3 {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}

.bg-primary {
  background-color: var(--color-primary);
}

.text-primary-foreground {
  color: var(--color-white);
}

.rounded-lg {
  border-radius: 0.5rem;
}

.hover\:bg-primary\/90:hover {
  background-color: rgba(37, 99, 235, 0.9);
}

.transition-colors {
  transition-property: color, background-color, border-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

.h-4 {
  height: 1rem;
}

.w-4 {
  width: 1rem;
}

/* ======================
   PROFILE HEADER 
   ====================== */
.perfil-header {
  background: linear-gradient(135deg, rgba(37, 99, 235, 0.05), rgba(37, 99, 235, 0.1));
  border: 1px solid rgba(37, 99, 235, 0.1);
  border-radius: 0.75rem;
  padding: 2rem;
  margin-bottom: 1.5rem;
}

.perfil-header-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: flex-start;
}

@media (min-width: 768px) {
  .perfil-header-content {
    flex-direction: row;
    align-items: center;
  }
}

.perfil-foto {
  width: 8rem;
  height: 8rem;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--color-white);
  box-shadow: var(--shadow-lg);
}

.perfil-info {
  flex: 1;
}

.perfil-nome {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.perfil-nome-civil {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  margin-bottom: 0.75rem;
}

.perfil-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.tag-primary {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--color-primary);
}

.tag-secondary {
  background-color: var(--color-gray-100);
  color: var(--color-gray-900);
}

/* ======================
   KPI GRID 
   ====================== */
.grid {
  display: grid;
}

.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}

@media (min-width: 768px) {
  .md\:grid-cols-1 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
}

.gap-4 {
  gap: 1rem;
}

/* ======================
   INFO SECTIONS 
   ====================== */
.info-section {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.75rem;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.section-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-primary);
}

.info-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.info-item {
  background: var(--color-gray-50);
  padding: 1rem;
  border-radius: 0.5rem;
  border-left: 4px solid var(--color-primary);
}

.info-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-600);
  margin-bottom: 0.25rem;
}

.info-value {
  color: var(--color-gray-900);
  font-size: 0.95rem;
  margin: 0;
}

.info-highlight {
  font-weight: 600;
}

/* ======================
   SOURCES SECTION 
   ====================== */
.sources-section {
  background: rgba(37, 99, 235, 0.05);
  border: 1px solid rgba(37, 99, 235, 0.2);
  border-radius: 0.75rem;
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.sources-content {
  display: flex;
  gap: 0.75rem;
}

.sources-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-primary);
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.sources-text {
  flex: 1;
}

.sources-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-900);
  margin-bottom: 0.25rem;
  margin-top: 0;
}

.sources-description {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin-bottom: 0.5rem;
  margin-top: 0;
}

.sources-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.source-link {
  font-size: 0.75rem;
  color: var(--color-primary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.2s ease;
}

.source-link:hover {
  text-decoration: underline;
}

.link-icon {
  width: 0.75rem;
  height: 0.75rem;
}

.link-separator {
  font-size: 0.75rem;
  color: var(--color-gray-400);
}

/* ======================
   ACTION BUTTONS 
   ====================== */
.action-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-size: 1rem;
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
}

.btn-secondary {
  background-color: var(--color-white);
  color: var(--color-gray-700);
  border: 1px solid var(--color-gray-300);
}

.btn-secondary:hover {
  background-color: var(--color-gray-50);
}

.btn-icon {
  width: 1rem;
  height: 1rem;
}
</style>
