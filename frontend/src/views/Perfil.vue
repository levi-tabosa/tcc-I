<template>
  <div class="min-h-screen flex flex-col bg-background">
    
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
          <a href="/" class="inline-flex items-center gap-2 px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors">
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

          <!-- Despesas Parlamentares -->
          <div class="info-section">
            <h2 class="section-title">
              <DollarSign class="section-icon" />
              Despesas Parlamentares
            </h2>
            
            <!-- Loading de despesas -->
            <div v-if="isLoadingDespesas" class="despesas-loading">
              <div class="loading-spinner"></div>
              <p>Carregando despesas...</p>
            </div>
            
            <!-- Erro nas despesas -->
            <div v-else-if="errorDespesas" class="despesas-error">
              <p>Erro ao carregar despesas: {{ errorDespesas }}</p>
            </div>
            
            <!-- Sem despesas -->
            <div v-else-if="despesas.length === 0" class="despesas-empty">
              <FileText class="empty-icon" />
              <p>Nenhuma despesa encontrada para este parlamentar</p>
            </div>
            
            <!-- Despesas carregadas -->
            <div v-else class="despesas-content">
              <!-- Resumo Estatístico -->
              <div class="despesas-stats">
                <div class="stat-card">
                  <div class="stat-icon total">
                    <DollarSign class="icon" />
                  </div>
                  <div class="stat-info">
                    <p class="stat-label">Total Gasto</p>
                    <p class="stat-value">{{ formatCurrency(totalDespesas) }}</p>
                  </div>
                </div>
                
                <div class="stat-card">
                  <div class="stat-icon average">
                    <TrendingUp class="icon" />
                  </div>
                  <div class="stat-info">
                    <p class="stat-label">Média Mensal</p>
                    <p class="stat-value">{{ formatCurrency(mediaGastoMensal) }}</p>
                  </div>
                </div>
                
                <div class="stat-card">
                  <div class="stat-icon count">
                    <FileText class="icon" />
                  </div>
                  <div class="stat-info">
                    <p class="stat-label">Total de Despesas</p>
                    <p class="stat-value">{{ despesas.length }}</p>
                  </div>
                </div>
                
                <div v-if="maiorDespesa" class="stat-card">
                  <div class="stat-icon highest">
                    <TrendingUp class="icon" />
                  </div>
                  <div class="stat-info">
                    <p class="stat-label">Maior Despesa</p>
                    <p class="stat-value">{{ formatCurrency(maiorDespesa.valor) }}</p>
                    <p class="stat-detail">{{ maiorDespesa.tipo_despesa }}</p>
                  </div>
                </div>
              </div>

              <!-- Despesas por Ano -->
              <div class="despesas-section">
                <h3 class="subsection-title">
                  <Calendar class="subsection-icon" />
                  Gastos por Ano
                </h3>
                <div class="year-grid">
                  <div v-for="ano in despesasPorAno" :key="ano.ano" class="year-card">
                    <div class="year-header">
                      <span class="year-number">{{ ano.ano }}</span>
                      <span class="year-total">{{ formatCurrency(ano.total) }}</span>
                    </div>
                    <div class="year-bar">
                      <div 
                        class="year-progress" 
                        :style="{ width: `${(ano.total / totalDespesas) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Despesas por Tipo -->
              <div class="despesas-section">
                <h3 class="subsection-title">
                  <BarChart3 class="subsection-icon" />
                  Despesas por Categoria
                </h3>
                <div class="tipo-grid">
                  <div v-for="tipo in mostrarTodasCategorias ? despesasPorTipo : despesasPorTipo.slice(0, 8)" :key="tipo.tipo" class="tipo-card">
                    <div class="tipo-header">
                      <h4 class="tipo-name">{{ tipo.tipo }}</h4>
                      <span class="tipo-total">{{ formatCurrency(tipo.total) }}</span>
                    </div>
                    <div class="tipo-details">
                      <span class="tipo-count">{{ tipo.quantidade }} despesa{{ tipo.quantidade > 1 ? 's' : '' }}</span>
                      <span class="tipo-average">Média: {{ formatCurrency(tipo.total / tipo.quantidade) }}</span>
                    </div>
                    <div class="tipo-bar">
                      <div 
                        class="tipo-progress" 
                        :style="{ width: `${(tipo.total / totalDespesas) * 100}%` }"
                      ></div>
                    </div>
                  </div>
                </div>
                
                <div v-if="despesasPorTipo.length > 8" class="show-more">
                  <button 
                    @click="mostrarTodasCategorias = !mostrarTodasCategorias" 
                    class="show-more-button"
                  >
                    <span v-if="!mostrarTodasCategorias">
                      Ver todas as {{ despesasPorTipo.length }} categorias
                    </span>
                    <span v-else>
                      Mostrar menos
                    </span>
                  </button>
                </div>
              </div>

              <!-- Despesas Recentes -->
              <div class="despesas-section">
                <h3 class="subsection-title">
                  <FileText class="subsection-icon" />
                  Despesas Recentes
                </h3>
                <div class="despesas-list">
                  <div v-for="despesa in mostrarTodasDespesas ? despesas : despesas.slice(0, 10)" :key="`${despesa.ano}-${despesa.mes}-${despesa.tipo_despesa}-${despesa.valor}`" class="despesa-item">
                    <div class="despesa-info">
                      <h4 class="despesa-tipo">{{ despesa.tipo_despesa }}</h4>
                      <p class="despesa-periodo">{{ formatMonth(despesa.mes) }} de {{ despesa.ano }}</p>
                    </div>
                    <div class="despesa-valor">
                      <span class="valor">{{ formatCurrency(despesa.valor) }}</span>
                      <a 
                        v-if="despesa.url_documento" 
                        :href="despesa.url_documento" 
                        target="_blank"
                        class="documento-link"
                        title="Ver documento"
                      >
                        <ExternalLink class="link-icon" />
                      </a>
                    </div>
                  </div>
                </div>
                
                <div v-if="despesas.length > 10" class="show-more">
                  <button 
                    @click="mostrarTodasDespesas = !mostrarTodasDespesas" 
                    class="show-more-button"
                  >
                    <span v-if="!mostrarTodasDespesas">
                      Ver todas as {{ despesas.length }} despesas
                    </span>
                    <span v-else>
                      Mostrar menos
                    </span>
                  </button>
                </div>
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
              href="/"
              class="btn btn-secondary"
            >
              <ArrowLeft class="btn-icon" />
              Voltar para lista
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
import { User, ArrowLeft, Building, Info, ExternalLink, BarChart3, DollarSign, TrendingUp, Calendar, FileText } from 'lucide-vue-next'
// AppHeader agora é importado globalmente em App.vue
import AppFooter from '../components/AppFooter.vue'

// Interface para as despesas do parlamentar
interface DespesaParlamentar {
  ano: number
  mes: number
  tipo_despesa: string
  valor: number
  url_documento?: string
}

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
  sigla_partido?: string
  email?: string
  foto?: string
}

// Interface para os dados completos do parlamentar (incluindo dados calculados)
interface ParlamentarCompleto extends ParlamentarAPI {
  nome: string
  partido: string
  estado: string
}

const route = useRoute()

// Estado para os dados do parlamentar
const parlamentarAPI = ref<ParlamentarAPI | null>(null)
const despesas = ref<DespesaParlamentar[]>([])
const isLoading = ref(false)
const isLoadingDespesas = ref(false)
const error = ref<string | null>(null)
const errorDespesas = ref<string | null>(null)

// Estados para controlar exibição expandida
const mostrarTodasCategorias = ref(false)
const mostrarTodasDespesas = ref(false)

const apiUrl = import.meta.env.VITE_BACKEND_URL
// Função para buscar despesas do parlamentar
const fetchDespesas = async (id: number) => {
  isLoadingDespesas.value = true
  errorDespesas.value = null
  
  try {
    const response = await fetch(`${apiUrl}/api/deputados/${id}/despesas`)
    if (!response.ok) {
      throw new Error('Erro ao buscar despesas')
    }
    
    const data = await response.json()
    despesas.value = data.despesas || []
  } catch (err: any) {
    console.error('Erro ao buscar despesas:', err)
    errorDespesas.value = err.message
    despesas.value = []
  } finally {
    isLoadingDespesas.value = false
  }
}

// Função para buscar dados do parlamentar específico da API
const fetchParlamentar = async (id: number) => {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${apiUrl}/api/deputados/${id}`)
    if (!response.ok) {
      throw new Error('Parlamentar não encontrado')
    }
    
    const data = await response.json()
    parlamentarAPI.value = data
    
    // Buscar despesas após carregar os dados do parlamentar
    await fetchDespesas(id)
  } catch (err: any) {
    console.error('Erro ao buscar parlamentar:', err)
    error.value = err.message
    parlamentarAPI.value = null
  } finally {
    isLoading.value = false
  }
}

// Computed para dados do parlamentar direto da API
const parlamentar = computed((): ParlamentarCompleto | null => {
  if (!parlamentarAPI.value) return null
  
  return {
    ...parlamentarAPI.value,
    nome: parlamentarAPI.value.nome_parlamentar || parlamentarAPI.value.nome_civil,
    partido: parlamentarAPI.value.sigla_partido || 'S/P',
    estado: parlamentarAPI.value.uf_nascimento || 'N/A',
    foto: parlamentarAPI.value.foto || `https://www.camara.leg.br/internet/deputado/bandep/${parlamentarAPI.value.id}.jpg`
  }
})

// Computed para análise das despesas
const totalDespesas = computed(() => {
  return despesas.value.reduce((total, despesa) => total + despesa.valor, 0)
})

const despesasPorTipo = computed(() => {
  const agrupadas = despesas.value.reduce((acc, despesa) => {
    if (!acc[despesa.tipo_despesa]) {
      acc[despesa.tipo_despesa] = { total: 0, quantidade: 0 }
    }
    acc[despesa.tipo_despesa].total += despesa.valor
    acc[despesa.tipo_despesa].quantidade += 1
    return acc
  }, {} as Record<string, { total: number; quantidade: number }>)
  
  return Object.entries(agrupadas)
    .map(([tipo, dados]) => ({ tipo, ...dados }))
    .sort((a, b) => b.total - a.total)
})

const despesasPorAno = computed(() => {
  const agrupadas = despesas.value.reduce((acc, despesa) => {
    if (!acc[despesa.ano]) {
      acc[despesa.ano] = 0
    }
    acc[despesa.ano] += despesa.valor
    return acc
  }, {} as Record<number, number>)
  
  return Object.entries(agrupadas)
    .map(([ano, total]) => ({ ano: parseInt(ano), total }))
    .sort((a, b) => b.ano - a.ano)
})

const mediaGastoMensal = computed(() => {
  if (despesas.value.length === 0) return 0
  
  const mesesUnicos = new Set(despesas.value.map(d => `${d.ano}-${d.mes}`))
  return totalDespesas.value / mesesUnicos.size
})

const maiorDespesa = computed(() => {
  if (despesas.value.length === 0) return null
  return despesas.value.reduce((maior, atual) => 
    atual.valor > maior.valor ? atual : maior
  )
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
    // Reset estados de expansão ao mudar de parlamentar
    mostrarTodasCategorias.value = false
    mostrarTodasDespesas.value = false
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

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value)
}

const formatMonth = (mes: number) => {
  const meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
  ]
  return meses[mes - 1] || `Mês ${mes}`
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

/* ======================
   DESPESAS SECTION 
   ====================== */
.despesas-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 2rem;
  color: var(--color-gray-600);
}

.loading-spinner {
  width: 1.5rem;
  height: 1.5rem;
  border: 2px solid var(--color-gray-200);
  border-top: 2px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.despesas-error {
  padding: 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: 0.5rem;
  color: rgb(185, 28, 28);
  text-align: center;
}

.despesas-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
  color: var(--color-gray-600);
}

.empty-icon {
  width: 3rem;
  height: 3rem;
  color: var(--color-gray-400);
}

.despesas-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Stats Cards */
.despesas-stats {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .despesas-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .despesas-stats {
    grid-template-columns: repeat(4, 1fr);
  }
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-sm);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 0.5rem;
  flex-shrink: 0;
}

.stat-icon.total {
  background-color: rgba(37, 99, 235, 0.1);
  color: var(--color-primary);
}

.stat-icon.average {
  background-color: rgba(16, 185, 129, 0.1);
  color: rgb(16, 185, 129);
}

.stat-icon.count {
  background-color: rgba(245, 158, 11, 0.1);
  color: rgb(245, 158, 11);
}

.stat-icon.highest {
  background-color: rgba(239, 68, 68, 0.1);
  color: rgb(239, 68, 68);
}

.stat-icon .icon {
  width: 1.25rem;
  height: 1.25rem;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin-bottom: 0.25rem;
  margin-top: 0;
}

.stat-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0;
}

.stat-detail {
  font-size: 0.75rem;
  color: var(--color-gray-500);
  margin-top: 0.25rem;
  margin-bottom: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Subsections */
.despesas-section {
  margin-top: 1rem;
}

.subsection-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.subsection-icon {
  width: 1rem;
  height: 1rem;
  color: var(--color-primary);
}

/* Year Grid */
.year-grid {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .year-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .year-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.year-card {
  padding: 1rem;
  background: var(--color-gray-50);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.5rem;
}

.year-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.year-number {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-900);
}

.year-total {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-primary);
}

.year-bar {
  height: 0.25rem;
  background-color: var(--color-gray-200);
  border-radius: 0.125rem;
  overflow: hidden;
}

.year-progress {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 0.3s ease;
}

/* Tipo Grid */
.tipo-grid {
  display: grid;
  gap: 0.75rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .tipo-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.tipo-card {
  padding: 1rem;
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.5rem;
  box-shadow: var(--shadow-sm);
}

.tipo-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.5rem;
  gap: 0.5rem;
}

.tipo-name {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-900);
  margin: 0;
  flex: 1;
  line-height: 1.25;
}

.tipo-total {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-primary);
  white-space: nowrap;
}

.tipo-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 0.5rem;
}

.tipo-count,
.tipo-average {
  font-size: 0.75rem;
  color: var(--color-gray-600);
}

.tipo-bar {
  height: 0.25rem;
  background-color: var(--color-gray-200);
  border-radius: 0.125rem;
  overflow: hidden;
}

.tipo-progress {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 0.3s ease;
}

/* Despesas List */
.despesas-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.despesa-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: var(--color-gray-50);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.5rem;
  gap: 1rem;
}

.despesa-info {
  flex: 1;
}

.despesa-tipo {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-900);
  margin: 0 0 0.25rem 0;
  line-height: 1.25;
}

.despesa-periodo {
  font-size: 0.75rem;
  color: var(--color-gray-600);
  margin: 0;
}

.despesa-valor {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-shrink: 0;
}

.valor {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-primary);
}

.documento-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-gray-500);
  transition: color 0.2s ease;
  text-decoration: none;
}

.documento-link:hover {
  color: var(--color-primary);
}

.documento-link .link-icon {
  width: 0.875rem;
  height: 0.875rem;
}

/* Show More */
.show-more {
  margin-top: 0.75rem;
  text-align: center;
}

.show-more-text {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin: 0;
}
</style>
