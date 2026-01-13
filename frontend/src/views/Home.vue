<template>
  <div class="page-wrapper">
    
    <main class="main-content">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="container">
          <div class="hero-content">
            <h1 class="hero-title">
              Transparência na Atuação Parlamentar
            </h1>
            <p class="hero-description">
              Acompanhe gastos, votações e presença dos seus representantes no Congresso Nacional.
              Dados oficiais, atualizados e acessíveis.
            </p>

            <!-- Search Bar -->
            <div class="search-autocomplete-wrapper" ref="searchWrapper">
              <div class="search-container">
                <form @submit.prevent="handleSearch" class="search-form">
                  <div class="search-input-wrapper">
                    <Search class="search-icon" />
                    <input
                      v-model="searchQuery"
                      type="text"
                      placeholder="Buscar parlamentar por nome, partido ou estado..."
                      class="search-input"
                      @keydown.down.prevent="onArrowDown"
                      @keydown.up.prevent="onArrowUp"
                      @keydown.enter.prevent="onEnter"
                      autocomplete="off"
                    />
                  </div>
                  <button
                    type="submit"
                    class="search-button"
                    :disabled="isLoading"
                  >
                    <span v-if="!isLoading">Buscar</span>
                    <span v-else>Buscando...</span>
                  </button>
                </form>
              </div>

              <!-- LISTA DE SUGESTÕES FLUTUANTE -->
              <div v-if="showSuggestions || error" class="autocomplete-results">
                <div v-if="isLoading" class="autocomplete-feedback">Carregando...</div>
                <div v-else-if="error" class="autocomplete-feedback error-feedback">{{ error }}</div>
                <ul v-else-if="searchResults.length > 0">
                  <li 
                    v-for="(deputado, index) in searchResults" 
                    :key="deputado.id"
                    :class="{ 'is-active': index === activeIndex }"
                    @click="selectSuggestion(deputado)"
                  >
                    {{ deputado.nome_civil }} ({{ deputado.uf }})
                  </li>
                </ul>
                <div v-else class="autocomplete-feedback">Nenhum resultado encontrado.</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- KPIs Section -->
      <section class="kpis-section">
        <div class="container">
          <h2 class="section-title">Indicadores Gerais</h2>
          <div class="stats-grid">
            <StatCard
              title="Gasto Total Consolidado"
              :value="totalGastos"
              format="currency"
              subtitle="Últimos 12 meses"
              :icon="DollarSign"
            />
            <StatCard
              title="Presença Média"
              :value="presencaMedia"
              format="percentage"
              subtitle="Sessões plenárias"
              :icon="Users"
            />
            <StatCard
              title="Fidelidade Partidária"
              :value="fidelidadeMedia"
              format="percentage"
              subtitle="Alinhamento com partido"
              :icon="TrendingUp"
            />
          </div>
        </div>
      </section>

      <!-- Map Section -->
      <section class="map-section">
        <div class="container">
          <h2 class="section-title">Distribuição por Estado</h2>
          <p class="section-subtitle">Clique em um estado para ver os parlamentares daquela região</p>
          <BrazilMap :parlamentares-por-estado="parlamentaresPorEstado" />
        </div>
      </section>

      <!-- Quick Links -->
      <section class="quick-links-section">
        <div class="container">
          <h2 class="section-title">Acesso Rápido</h2>
          <div class="quick-links-grid">
            <a href="/parlamentares" class="quick-link-card">
              <div class="quick-link-header">
                <div class="quick-link-icon">
                  <Users />
                </div>
                <h3>Parlamentares</h3>
              </div>
              <p class="quick-link-description">
                Lista completa com filtros por partido, estado e desempenho
              </p>
            </a>

            <a href="/dashboard" class="quick-link-card">
              <div class="quick-link-header">
                <div class="quick-link-icon">
                  <BarChart3 />
                </div>
                <h3>Dashboard</h3>
              </div>
              <p class="quick-link-description">
                Visualizações e análises agregadas dos dados parlamentares
              </p>
            </a>

            <!-- link de comparar removido -->

            <a href="/anomalias" class="quick-link-card">
              <div class="quick-link-header">
                <div class="quick-link-icon">
                  <AlertTriangle />
                </div>
                <h3>Anomalias</h3>
              </div>
              <p class="quick-link-description">
                Identificação de gastos fora do padrão com análise estatística
              </p>
            </a>
          </div>
        </div>
      </section>

      <!-- Info Section -->
      <section class="info-section">
        <div class="container">
          <div class="info-content">
            <FileText class="info-icon" />
            <h2 class="info-title">Dados Oficiais e Transparentes</h2>
            <p class="info-description">
              Todos os dados são coletados diretamente das APIs oficiais da Câmara dos Deputados e
              Senado Federal, em conformidade com a Lei de Acesso à Informação (LAI) e LGPD.
            </p>
            <div class="info-actions">
              <a href="/metodologia" class="btn btn-primary">
                Ver Metodologia
              </a>
              <RouterLink to="/contato" class="btn btn-secondary">
                Enviar Feedback
              </RouterLink>
            </div>
          </div>
        </div>
      </section>
    </main>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Search, DollarSign, Users, TrendingUp, BarChart3, AlertTriangle, FileText
} from 'lucide-vue-next'
import AppFooter from '../components/AppFooter.vue'
import StatCard from '../components/StatCard.vue'
import BrazilMap from '../components/BrazilMap.vue'

interface SearchResult {
  id: number;
  nome_civil: string;
  uf: string;
}

interface Parlamentar {
  id: string
  nome: string
  cargo: string
  uf: string
  estado: string
  partido: string
  gastoTotal: number
  presenca: number
  fidelidadePartidaria: number
}

const apiUrl = import.meta.env.VITE_BACKEND_URL 

const searchQuery = ref('');
const originalQuery = ref('');
const searchResults = ref<SearchResult[]>([]);
const isLoading = ref(false);
const hasSearched = ref(false);
const error = ref<string | null>(null);

const router = useRouter();

const searchWrapper = ref<HTMLElement | null>(null);
const activeIndex = ref(-1);
const showSuggestions = computed(() => {
  return searchQuery.value.length >= 2 && (isLoading.value || searchResults.value.length > 0);
});

const parlamentares = ref<Parlamentar[]>([])
const parlamentaresLoading = ref(false)
const parlamentaresError = ref<string | null>(null)

const estatisticasGerais = ref({
  total_gastos: 0,
  presenca_media: 0,
  fidelidade_media: 0,
  total_parlamentares: 0
})
const estatisticasLoading = ref(false)


const partidos = [
  'Todos', 'PT', 'PSDB', 'PL', 'PP', 'MDB', 'PSD', 'REPUBLICANOS', 'UNIÃO', 'PSB', 
  'PDT', 'PSOL', 'PODE', 'AVANTE', 'PCdoB', 'CIDADANIA', 'PSC', 'PATRIOTA', 'PROS', 'SOLIDARIEDADE'
]

const estados = [
  'Todos', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 
  'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]


const fetchEstatisticasGerais = async () => {
  estatisticasLoading.value = true

  try {
    const response = await fetch(`${apiUrl}/api/deputados/estatisticas/geral`)
    if (!response.ok) {
      throw new Error('Falha ao carregar estatísticas gerais')
    }
    
    const data = await response.json()
    console.log('Estatísticas gerais recebidas:', data)
    estatisticasGerais.value = {
      total_gastos: data.total_gastos_12_meses || 0,
      presenca_media: data.presenca_media || 0,
      fidelidade_media: data.fidelidade_media || 0,
      total_parlamentares: data.total_parlamentares || 0
    }
  } catch (err: any) {
    console.error('Erro ao carregar estatísticas gerais:', err)
  } finally {
    estatisticasLoading.value = false
  }
}

const fetchParlamentares = async () => {

  parlamentaresLoading.value = true
  parlamentaresError.value = null
  
  try {
    const response = await fetch(`${apiUrl}/api/deputados/`)
    if (!response.ok) {
      throw new Error('Falha ao carregar dados dos parlamentares')
    }
    
    const data = await response.json()
    
    parlamentares.value = data.map((deputado: any) => ({
      id: deputado.id.toString(),
      nome: deputado.nome_civil,
      cargo: 'Deputado Federal',
      uf: deputado.uf,
      estado: deputado.uf,
      partido: deputado.sigla_partido || 'S/P',
      gastoTotal: 0,
      presenca: 0,
      fidelidadePartidaria: 0
    }))
  } catch (err: any) {
    console.error('Erro ao carregar parlamentares:', err)
    parlamentaresError.value = err.message
    parlamentares.value = []
  } finally {
    parlamentaresLoading.value = false
  }
}

const totalGastos = computed(() => {
  return estatisticasGerais.value.total_gastos
})

const presencaMedia = computed(() => {
  return estatisticasGerais.value.presenca_media
})

const fidelidadeMedia = computed(() => {
  return estatisticasGerais.value.fidelidade_media
})

let debounceTimer: number | null = null;
const DEBOUNCE_MS = 300;

const fetchSuggestions = async (q: string) => {
  error.value = null;
  isLoading.value = true;
  hasSearched.value = true;
  originalQuery.value = q;
  searchResults.value = [];

  if (!q || q.length < 1) {
    isLoading.value = false;
    return;
  }

  try {
    const response = await fetch(`${apiUrl}/api/deputados/buscar?nome=${encodeURIComponent(q)}`);
    if (!response.ok) throw new Error('Falha ao comunicar com o servidor. A API está rodando?');
    const data = await response.json();

    const resultados = Array.isArray(data.resultados) ? data.resultados : [];

    const filtered = resultados.filter((r: any) => {
      if (!r.nome_civil) return false;
      return r.nome_civil.toLowerCase().startsWith(q.toLowerCase());
    });

    searchResults.value = filtered.length > 0 ? filtered : resultados;
  } catch (err: any) {
    console.error('Erro na busca:', err);
    error.value = err.message || 'Ocorreu um erro inesperado.';
  } finally {
    isLoading.value = false;
  }
};

watch(searchQuery, (newVal) => {
  if (debounceTimer) window.clearTimeout(debounceTimer);
  if (!newVal || newVal.length < 1) {
    searchResults.value = [];
    hasSearched.value = false;
    error.value = null;
    return;
  }

  debounceTimer = window.setTimeout(() => {
    fetchSuggestions(newVal);
  }, DEBOUNCE_MS);
});

const handleSearch = async () => {
  if (debounceTimer) {
    window.clearTimeout(debounceTimer);
    debounceTimer = null;
  }

  const q = searchQuery.value;
  if (!q || q.length < 1) {
    error.value = 'Por favor, digite pelo menos 1 caractere.';
    return;
  }

  await fetchSuggestions(q);

  if (searchResults.value.length === 1) {
    const deputadoId = searchResults.value[0].id;
    router.push({ name: 'Perfil', params: { id: deputadoId } });
  } else if (searchResults.value.length > 1) {
    const deputadoId = searchResults.value[0].id;
    router.push({ name: 'Perfil', params: { id: deputadoId } });
  } else {
    error.value = 'Nenhum deputado encontrado com esse nome.';
  }
};

const selectSuggestion = (deputado: SearchResult) => {
  searchQuery.value = deputado.nome_civil;
  searchResults.value = []; 
  activeIndex.value = -1;
  router.push({ name: 'Perfil', params: { id: deputado.id } });
};

const onArrowDown = () => {
  if (searchResults.value.length === 0) return;
  activeIndex.value = (activeIndex.value + 1) % searchResults.value.length;
};

const onArrowUp = () => {
  if (searchResults.value.length === 0) return;
  if (activeIndex.value <= 0) {
    activeIndex.value = searchResults.value.length - 1;
  } else {
    activeIndex.value--;
  }
};

const onEnter = () => {
  if (activeIndex.value >= 0 && searchResults.value[activeIndex.value]) {
    selectSuggestion(searchResults.value[activeIndex.value]);
  } else {
    handleSearch(); 
  }
};

const handleClickOutside = (event: MouseEvent) => {
  if (searchWrapper.value && !searchWrapper.value.contains(event.target as Node)) {
    searchResults.value = []; 
    activeIndex.value = -1;
  }
};

onMounted(async () => {
  document.addEventListener('click', handleClickOutside);
  await Promise.all([
    fetchParlamentares(),
    fetchEstatisticasGerais()
  ]);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

const parlamentaresPorEstado = computed(() => {
  const contagem: Record<string, number> = {}
  parlamentares.value.forEach((p) => {
    if (p.uf) {
      contagem[p.uf] = (contagem[p.uf] || 0) + 1
    }
  })
  return contagem
})
</script>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  background: var(--bg-secondary);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text-primary);
}

.main-content {
  margin: 0 auto;
}

.hero-section {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding: 6rem 0 8rem;
  background-image: 
    linear-gradient(135deg, rgba(255, 255, 255, 0.65) 0%, rgba(255, 255, 255, 0.55) 100%),
    url('/imagem-padrao.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.dark .hero-section {
  background-image: 
    linear-gradient(135deg, rgba(15, 23, 42, 0.70) 0%, rgba(15, 23, 42, 0.60) 100%),
    url('/imagem-padrao.jpg');
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(255, 255, 255, 0.3) 100%);
  pointer-events: none;
  z-index: 1;
}

.dark .hero-section::before {
  background: linear-gradient(180deg, transparent 0%, rgba(15, 23, 42, 0.5) 100%);
}

.hero-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
  z-index: 2;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.025em;
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.3), 0 4px 20px rgba(255, 255, 255, 0.8);
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 3.5rem;
    margin-bottom: 2rem;
  }
}

.hero-description {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
  text-shadow: 0 1px 8px rgba(0, 0, 0, 0.3), 0 2px 12px rgba(255, 255, 255, 0.7);
}

.search-autocomplete-wrapper {
  position: relative;
  max-width: 600px;
  margin: 0 auto 2.5rem;
}

.search-container {
  position: relative;
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: var(--surface-primary);
  padding: 1rem;
  border-radius: 0.75rem;
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border-primary);
}

@media (min-width: 640px) {
  .search-form {
    flex-direction: row;
    padding: 0.5rem;
  }
}

.search-input-wrapper {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: var(--text-tertiary);
}

.search-input {
  width: 100%;
  height: 3rem;
  padding-left: 3rem;
  padding-right: 1rem;
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: var(--surface-primary);
}

.search-input:focus {
  border-color: var(--color-primary);
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.search-button {
  padding: 0.75rem 1.5rem;
  background-color: var(--color-primary);
  color: var(--color-white);
  border: none;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 1rem;
}

.search-button:hover {
  background-color: var(--color-primary-dark);
}

.search-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.autocomplete-results {
  position: absolute;
  top: calc(100% - 0.5rem);
  left: 1rem;
  right: 1rem;
  background: var(--surface-primary);
  border: 1px solid var(--border-primary);
  border-top: none;
  border-radius: 0 0 0.75rem 0.75rem;
  box-shadow: var(--shadow-lg);
  max-height: 300px;
  overflow-y: auto;
  z-index: 10;
  padding: 0;
  margin: 0;
  list-style: none;
  text-align: left;
}

.autocomplete-results ul {
  padding: 0;
  margin: 0;
  list-style: none;
}

.autocomplete-results li {
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-bottom: 1px solid var(--border-primary);
  color: var(--text-secondary);
}

.autocomplete-results li:last-child {
  border-bottom: none;
}

.autocomplete-results li:hover,
.autocomplete-results li.is-active {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.autocomplete-feedback {
  padding: 0.75rem 1rem;
  color: var(--text-tertiary);
  font-style: italic;
}

.error-feedback {
  color: var(--color-error);
  background-color: rgba(239, 68, 68, 0.1);
  border: 1px solid var(--color-error);
  border-radius: 0.375rem;
  margin: 0.5rem;
}

.kpis-section {
  padding: 4rem 0;
  background-color: var(--bg-secondary);
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 2rem;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.map-section {
  padding: 4rem 0;
  background-color: var(--bg-secondary);
  position: relative;
  z-index: 1;
}

.section-subtitle {
  text-align: center;
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 2rem;
  margin-top: -1rem;
}

.quick-links-section {
  padding: 4rem 0;
  background-color: var(--bg-primary);
}

.quick-links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
  justify-items: center; 
}

.quick-link-card {
  width: 100%;
  max-width: 360px;
}

.quick-link-card {
  background: var(--surface-primary);
  border: 1px solid var(--border-primary);
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-decoration: none;
  transition: all 0.2s ease;
  display: block;
}

.quick-link-card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.quick-link-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.quick-link-icon {
  padding: 0.5rem;
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
  color: var(--color-primary);
}

.quick-link-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.quick-link-card h3 {
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0;
}

.quick-link-description {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin: 0;
  line-height: 1.5;
}

.info-section {
  padding: 4rem 0;
  background-color: var(--surface-primary);
}

.info-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.info-icon {
  width: 3rem;
  height: 3rem;
  color: var(--color-primary);
  margin: 0 auto 1rem;
}

.info-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.info-description {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  margin-bottom: 2rem;
  line-height: 1.6;
}

.info-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

@media (min-width: 640px) {
  .info-actions {
    flex-direction: row;
    justify-content: center;
  }
}

.btn {
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

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 640px) {
  .container {
    padding: 0 1.5rem;
  }
}

@media (min-width: 1024px) {
  .container {
    padding: 0 2rem;
  }
}
</style>
