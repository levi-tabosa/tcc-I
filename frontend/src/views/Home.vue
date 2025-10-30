<template>
  <div class="page-wrapper">
    <!-- Header -->
    <header class="header">
      <div class="header-container">
        <nav class="nav">
          <div class="nav-brand">
            <Shield class="nav-icon" />
            <span class="nav-title">
              Fiscaliza Brasil
            </span>
          </div>
          
          <!-- Menu Desktop -->
          <div class="nav-links">
            <a href="#inicio" class="nav-link">
              Início
            </a>
            <a href="#funcionalidades" class="nav-link">
              Funcionalidades
            </a>
            <a href="#como-usar" class="nav-link">
              Como Usar
            </a>
            <a href="#sobre" class="nav-link">
              Sobre
            </a>
          </div>

          <!-- Menu Mobile Hamburger -->
          <button 
            class="mobile-menu-button"
            @click="toggleMobileMenu"
            :class="{ 'is-open': isMobileMenuOpen }"
            aria-label="Menu de navegação"
          >
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
          </button>

          <!-- Menu Mobile Overlay -->
          <div 
            class="mobile-menu-overlay" 
            v-if="isMobileMenuOpen"
            @click="closeMobileMenu"
          ></div>

          <!-- Menu Mobile -->
          <div class="mobile-menu" :class="{ 'is-open': isMobileMenuOpen }">
            <a href="#inicio" class="mobile-nav-link" @click="closeMobileMenu">
              Início
            </a>
            <a href="#funcionalidades" class="mobile-nav-link" @click="closeMobileMenu">
              Funcionalidades
            </a>
            <a href="#como-usar" class="mobile-nav-link" @click="closeMobileMenu">
              Como Usar
            </a>
            <a href="#sobre" class="mobile-nav-link" @click="closeMobileMenu">
              Sobre
            </a>
          </div>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <!-- Hero Section -->
      <section id="inicio" class="hero-section">
        <!-- Background decorativo -->
        <div class="hero-bg-overlay"></div>
        <div class="hero-bg-accent"></div>
        
        <div class="hero-content">
          <div class="hero-badge">
            <Eye class="hero-badge-icon" />
            Transparência · Dados Públicos · Cidadania
          </div>
          
          <h1 class="hero-title">
            Fiscalize seus
            <span class="hero-title-accent">
              representantes
            </span>
            com clareza
          </h1>
          
          <p class="hero-description">
            Transformamos dados complexos do Congresso em informações claras e acessíveis. 
            Fiscalização parlamentar não precisa de expertise técnica – é direito de todos.
          </p>

          <!-- Search Bar com Autocomplete -->
          <div class="search-autocomplete-wrapper" ref="searchWrapper">
            <div class="search-container">
              <form @submit.prevent="handleSearch" class="search-form">
                <div class="search-input-wrapper">
                  <Search class="search-icon" />
                  <input 
                    v-model="searchQuery"
                    type="text"
                    placeholder="Busque por um parlamentar..."
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
            <div v-if="showSuggestions" class="autocomplete-results">
              <div v-if="isLoading" class="autocomplete-feedback">Carregando...</div>
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
          
          <div class="hero-features">
            <div class="hero-feature">
              <CheckCircle2 class="hero-feature-icon" />
              <span>Dados oficiais em tempo real</span>
            </div>
            <div class="hero-feature">
              <CheckCircle2 class="hero-feature-icon" />
              <span>100% gratuito</span>
            </div>
          </div>

          <!-- Stats Preview -->
          <div class="stats-grid">
            <div class="stat-card">
              <Users class="stat-icon stat-icon-blue" />
              <div class="stat-number">594</div>
              <div class="stat-label">Parlamentares monitorados</div>
            </div>
            <div class="stat-card">
              <TrendingUp class="stat-icon stat-icon-green" />
              <div class="stat-number">23</div>
              <div class="stat-label">Partidos políticos</div>
            </div>
            <div class="stat-card">
              <FileText class="stat-icon stat-icon-purple" />
              <div class="stat-number">+10k</div>
              <div class="stat-label">Votações analisadas</div>
            </div>
            <div class="stat-card">
              <BarChart3 class="stat-icon stat-icon-orange" />
              <div class="stat-number">Real-time</div>
              <div class="stat-label">Atualização diária</div>
            </div>
          </div>
        </div>
      </section>
      
      <!-- A busca agora usa autocomplete; a seção de resultados antiga foi removida -->


      <!-- Problema e Solução -->
      <section class="problem-solution-section">
        <div class="problem-solution-container">
          <div class="problem-solution-content">
            <div class="problem-box">
              <AlertCircle class="box-icon box-icon-red" />
              <div class="box-content">
                <h3>O Problema</h3>
                <p>
                  Embora a Câmara e o Senado disponibilizem dados públicos, o acesso exige conhecimento 
                  técnico para manipular <strong>APIs, CSV e JSON</strong>. O Portal da Transparência 
                  limita-se a consultas individualizadas, incapaz de gerar <strong>estatísticas consolidadas, 
                  tendências e métricas comparativas</strong> essenciais para uma avaliação objetiva.
                </p>
              </div>
            </div>

            <div class="solution-box">
              <CheckCircle2 class="box-icon box-icon-green" />
              <div class="box-content">
                <h3>Nossa Solução</h3>
                <p>
                  Convertemos dados complexos em <strong>visualizações intuitivas, indicadores objetivos 
                  e dashboards comparativos</strong>. Qualquer pessoa pode avaliar gastos, votações e 
                  fidelidade partidária sem conhecimento técnico. <strong style="color: #15803d;">
                  A fiscalização parlamentar deixa de ser privilégio de especialistas</strong>.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Funcionalidades Principais -->
      <section id="funcionalidades" class="features-section">
        <div class="features-container">
          <div class="features-header">
            <h2 class="features-title">
              O que você pode fiscalizar
            </h2>
            <p class="features-description">
              Três pilares fundamentais para avaliar a atuação parlamentar de forma completa e objetiva
            </p>
          </div>

          <div class="features-grid">
            <div 
              v-for="(feature, idx) in features" 
              :key="idx" 
              class="feature-card"
            >
              <div class="feature-card-content">
                <h3>{{ feature.title }}</h3>
                <p>{{ feature.description }}</p>
                <ul class="feature-list">
                  <li 
                    v-for="(item, i) in feature.features" 
                    :key="i"
                  >
                    <CheckCircle2 class="feature-check-icon" />
                    <span>{{ item }}</span>
                  </li>
                </ul>
                <button class="feature-button">
                  Explorar
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Como Funciona -->
      <section id="como-usar" class="how-it-works-section">
        <div class="how-it-works-container">
          <div class="how-it-works-header">
            <h2 class="how-it-works-title">
              Como transformamos dados em transparência
            </h2>
            <p class="how-it-works-description">
              Processo automatizado que garante precisão, atualização constante e total confiabilidade
            </p>
          </div>

          <div class="steps-grid">
            <div 
              v-for="(step, idx) in steps" 
              :key="idx" 
              class="step-card"
            >
              <div class="step-content">
                <div class="step-icon-wrapper">
                  <component :is="step.icon" class="step-icon" />
                </div>
                <h3 class="step-title">{{ step.title }}</h3>
                <p class="step-description">{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Fontes e Metodologia -->
      <section class="methodology-section">
        <div class="methodology-container">
          <div class="methodology-card">
            <div class="methodology-content">
              <div class="methodology-header">
                <Shield class="methodology-shield-icon" />
                <h2 class="methodology-title">Confiabilidade e Transparência</h2>
              </div>
              
              <div class="methodology-grid">
                <div class="methodology-item">
                  <h3 class="methodology-subtitle">
                    <BarChart class="methodology-title-icon" />
                    Fontes Oficiais
                  </h3>
                  <ul class="methodology-list">
                    <li class="methodology-list-item">
                      <CheckCircle2 class="methodology-check-icon" />
                      <span>API de Dados Abertos da Câmara dos Deputados</span>
                    </li>
                    <li class="methodology-list-item">
                      <CheckCircle2 class="methodology-check-icon" />
                      <span>API do Senado Federal</span>
                    </li>
                    <li class="methodology-list-item">
                      <CheckCircle2 class="methodology-check-icon" />
                      <span>Portal da Transparência</span>
                    </li>
                  </ul>
                </div>
                
                <div class="methodology-item">
                  <h3 class="methodology-subtitle">
                    <RefreshCw class="methodology-title-icon" />
                    Atualização
                  </h3>
                  <ul class="methodology-list">
                    <li class="methodology-list-item">
                      <CheckCircle2 class="methodology-check-icon" />
                      <span>Sincronização automática diária</span>
                    </li>
                    <li class="methodology-list-item">
                      <CheckCircle2 class="methodology-check-icon" />
                      <span>Verificação de integridade dos dados</span>
                    </li>
                    <li class="methodology-list-item">
                      <CheckCircle2 class="methodology-check-icon" />
                      <span>Registro completo de alterações</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div class="methodology-commitment">
                <p>
                  <strong>Compromisso com a precisão:</strong> Todos os dados 
                  exibidos na plataforma são obtidos diretamente de fontes governamentais oficiais, sem 
                  qualquer tipo de manipulação ou interpretação editorial. Nossa metodologia está documentada 
                  e pode ser auditada por qualquer pessoa interessada.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Final -->
      <section class="cta-section">
        <div class="cta-container">
          <h2 class="cta-title">
            A fiscalização começa agora
          </h2>
          <p class="cta-description">
            Não é preciso ser especialista para acompanhar seus representantes. Exercer a cidadania 
            fiscalizadora é um direito fundamental – e agora está ao alcance de todos.
          </p>
          <div class="cta-buttons">
            <button class="cta-button-primary">
              Começar a Fiscalizar
              <ArrowRight class="cta-arrow-icon" />
            </button>
            <button class="cta-button-secondary">
              Sobre o Projeto
            </button>
          </div>
          <p class="cta-note">
            ✓ 100% gratuito · ✓ Sem cadastro · ✓ Dados oficiais verificados
          </p>
        </div>
      </section>

      <!-- Footer -->
      <footer class="footer">
        <div class="footer-container">
          <div class="footer-grid">
            <div class="footer-brand">
              <div class="footer-brand-header">
                <Shield class="footer-shield-icon" />
                <span class="footer-brand-name">Fiscaliza Brasil</span>
              </div>
              <p class="footer-brand-description">
                Democratizando o acesso aos dados parlamentares para promover a fiscalização cidadã 
                e fortalecer a transparência democrática.
              </p>
            </div>
            
            <div class="footer-section">
              <h4 class="footer-section-title">Sobre o Projeto</h4>
              <p class="footer-section-description">
                Trabalho de Conclusão de Curso desenvolvido com o objetivo de quebrar as barreiras 
                técnicas que impedem o acesso amplo aos dados públicos parlamentares.
              </p>
            </div>
            
            <div class="footer-section">
              <h4 class="footer-section-title">Fontes de Dados</h4>
              <ul class="footer-list">
                <li>• Câmara dos Deputados (API Oficial)</li>
                <li>• Senado Federal (API Oficial)</li>
                <li>• Portal da Transparência</li>
              </ul>
            </div>
          </div>
          
          <div class="footer-bottom">
            <p class="footer-copyright">
              © 2025 Fiscaliza Brasil · TCC · Todos os dados são públicos e verificáveis
            </p>
            <p class="footer-credits">
              Desenvolvido com transparência e propósito cívico
            </p>
          </div>
        </div>
      </footer>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router' // <<< 1. IMPORTE O useRouter
import { 
  Search, TrendingUp, Users, FileText, Shield, Eye, ArrowRight, Database, 
  BarChart3, CheckCircle2, AlertCircle, BarChart, RefreshCw
} from 'lucide-vue-next'

// --- Interface para Tipagem dos Resultados da Busca ---
interface SearchResult {
  id: number;
  nome_civil: string;
  uf: string;
}

// --- Variáveis Reativas ---
const searchQuery = ref('');
const originalQuery = ref('');
const searchResults = ref<SearchResult[]>([]);
const isLoading = ref(false);
const hasSearched = ref(false);
const error = ref<string | null>(null);
const isMobileMenuOpen = ref(false);

const router = useRouter(); // <<< 2. CRIE A INSTÂNCIA DO ROUTER

// Autocomplete helpers
const searchWrapper = ref<HTMLElement | null>(null);
const activeIndex = ref(-1);
const showSuggestions = computed(() => {
  return searchQuery.value.length >= 2 && (isLoading.value || searchResults.value.length > 0);
});

// --- Funções do Menu Mobile ---
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
  // Previne o scroll do body quando o menu está aberto
  document.body.style.overflow = isMobileMenuOpen.value ? 'hidden' : '';
};

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false;
  document.body.style.overflow = '';
};

// --- Busca com debounce e filtro por prefixo (nome começa com) ---
let debounceTimer: number | null = null;
const DEBOUNCE_MS = 300;

const fetchSuggestions = async (q: string) => {
  // limpa e prepara estados
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
    const response = await fetch(`http://127.0.0.1:8000/api/deputados/buscar?nome=${encodeURIComponent(q)}`);
    if (!response.ok) throw new Error('Falha ao comunicar com o servidor. A API está rodando?');
    const data = await response.json();

    const resultados = Array.isArray(data.resultados) ? data.resultados : [];

    // Filtra apenas aqueles cujo nome_civil COMEÇA com a query (case-insensitive)
    const filtered = resultados.filter((r: any) => {
      if (!r.nome_civil) return false;
      return r.nome_civil.toLowerCase().startsWith(q.toLowerCase());
    });

    // Se houver correspondências por prefixo, mostra elas; senão, exibe as correspondências por substring
    searchResults.value = filtered.length > 0 ? filtered : resultados;

    // Se restar apenas 1 resultado e for uma busca por submit, redirecionamento será feito em handleSearch (veja abaixo)
  } catch (err: any) {
    console.error('Erro na busca:', err);
    error.value = err.message || 'Ocorreu um erro inesperado.';
  } finally {
    isLoading.value = false;
  }
};

// watcher: quando o usuário digita, pesquisamos com debounce
watch(searchQuery, (newVal) => {
  if (debounceTimer) window.clearTimeout(debounceTimer);
  // mínima proteção: não pesquisar com string vazia
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

// manter handleSearch para comportamento de submit (enter / botão)
const handleSearch = async () => {
  // se houver debounce pendente, limpar e executar imediatamente
  if (debounceTimer) {
    window.clearTimeout(debounceTimer);
    debounceTimer = null;
  }

  const q = searchQuery.value;
  if (!q || q.length < 1) {
    error.value = 'Por favor, digite pelo menos 1 caractere.';
    return;
  }

  // executar busca e redirecionar se encontrar exatamente um
  await fetchSuggestions(q);

  if (searchResults.value.length === 1) {
    const deputadoId = searchResults.value[0].id;
    router.push({ name: 'Perfil', params: { id: deputadoId } });
  }
};

// --- Funções de Interatividade do Autocomplete ---

// Clicar em uma sugestão
const selectSuggestion = (deputado: SearchResult) => {
  searchQuery.value = deputado.nome_civil;
  searchResults.value = []; // Esconde o dropdown
  activeIndex.value = -1;
  // Redireciona imediatamente para o perfil
  router.push({ name: 'Perfil', params: { id: deputado.id } });
};

// --- Funções de Navegação por Teclado ---
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
    handleSearch(); // comportamento padrão de busca
  }
};

// --- Lógica para fechar ao clicar fora ---
const handleClickOutside = (event: MouseEvent) => {
  if (searchWrapper.value && !searchWrapper.value.contains(event.target as Node)) {
    searchResults.value = []; // Esconde o dropdown
    activeIndex.value = -1;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});



// --- Dados estáticos que você já usava para o template ---
const features = [
  {
    color: "blue",
    title: "Gastos da Cota Parlamentar",
    description: "Acompanhe em tempo real como cada parlamentar utiliza recursos públicos",
    features: [
      "Detalhamento por categoria de despesa",
      "Comparação entre parlamentares e partidos",
      "Alertas de gastos atípicos",
      "Histórico completo e exportável"
    ]
  },
  {
    color: "purple",
    title: "Histórico de Votações",
    description: "Analise decisões e posicionamento em pautas importantes",
    features: [
      "Registro completo de todas as votações",
      "Taxa de presença em sessões",
      "Alinhamento com bancadas temáticas",
      "Filtros por tema e relevância"
    ]
  },
  {
    color: "green",
    title: "Fidelidade Partidária",
    description: "Avalie a coerência entre discurso partidário e ação política",
    features: [
      "Índice de alinhamento com o partido",
      "Comparação com líderes partidários",
      "Identificação de votações divergentes",
      "Padrões de coligação"
    ]
  }
]

const steps = [
  {
    icon: Database,
    title: "Coleta Automatizada",
    description: "Extração diária via APIs oficiais da Câmara dos Deputados e Senado Federal. Dados brutos em JSON, CSV e XML são capturados com total integridade."
  },
  {
    icon: BarChart3,
    title: "Processamento Inteligente",
    description: "Algoritmos convertem dados técnicos em estatísticas consolidadas, identificam tendências, calculam índices e geram métricas comparativas objetivas."
  },
  {
    icon: Eye,
    title: "Visualização Acessível",
    description: "Dashboards intuitivos, gráficos interativos e relatórios compreensíveis. Sem jargão técnico, sem barreiras de acesso."
  }
]
</script>

<style scoped>
/* CSS Melhorado para Melhor Compreensão */

/* ======================
   MELHORIAS GLOBAIS MOBILE 
   ====================== */
html {
  scroll-behavior: smooth;
}

* {
  -webkit-tap-highlight-color: rgba(96, 165, 250, 0.2);
}

/* Melhor experiência de scroll em dispositivos touch */
body {
  -webkit-overflow-scrolling: touch;
}

/* ======================
   ESTRUTURA GERAL 
   ====================== */
.page-wrapper {
  min-height: 100vh;
  background: linear-gradient(180deg, #0f172a, #1e293b);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #e2e8f0;
}

/* ======================
   HEADER E NAVEGAÇÃO 
   ====================== */
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background-color: rgba(15, 23, 42, 0.95);
  border-bottom: 1px solid #334155;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3);
}

.header-container { 
  max-width: 1200px; 
  margin: 0 auto; 
  padding: 1rem 1.5rem; 
}

.nav { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
}

.nav-brand { 
  display: flex; 
  align-items: center; 
  gap: 0.75rem; 
}

.nav-icon { 
  width: 2.25rem; 
  height: 2.25rem; 
  color: #60a5fa; 
}

.nav-title { 
  font-size: 1.75rem; 
  font-weight: 800; 
  background: linear-gradient(135deg, #60a5fa, #3b82f6); 
  background-clip: text; 
  -webkit-background-clip: text; 
  color: transparent; 
}

.nav-links { 
  display: none; 
  gap: 2rem; 
}

@media (min-width: 768px) { 
  .nav-links { display: flex; } 
}

.nav-link { 
  color: #94a3b8; 
  font-weight: 500; 
  text-decoration: none; 
  transition: all 0.2s ease; 
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
}

.nav-link:hover { 
  color: #60a5fa; 
  background-color: #1e293b;
}

/* ======================
   MENU MOBILE HAMBURGER
   ====================== */
.mobile-menu-button {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 2.5rem;
  height: 2.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  position: relative;
  z-index: 60;
}

@media (min-width: 768px) {
  .mobile-menu-button {
    display: none;
  }
}

.hamburger-line {
  width: 1.5rem;
  height: 2px;
  background-color: #e2e8f0;
  margin: 2px 0;
  transition: all 0.3s ease;
  transform-origin: center;
}

.mobile-menu-button.is-open .hamburger-line:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.mobile-menu-button.is-open .hamburger-line:nth-child(2) {
  opacity: 0;
}

.mobile-menu-button.is-open .hamburger-line:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -6px);
}

.mobile-menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 40;
  backdrop-filter: blur(4px);
}

.mobile-menu {
  position: fixed;
  top: 0;
  right: -100%;
  width: 280px;
  height: 100vh;
  background: linear-gradient(180deg, #0f172a, #1e293b);
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
  z-index: 50;
  transition: right 0.3s ease;
  padding: 5rem 0 2rem;
  display: flex;
  flex-direction: column;
  border-left: 1px solid #334155;
}

.mobile-menu.is-open {
  right: 0;
}

.mobile-nav-link {
  display: block;
  padding: 1.25rem 2rem;
  color: #e2e8f0;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.125rem;
  transition: all 0.2s ease;
  border-bottom: 1px solid #334155;
}

.mobile-nav-link:hover {
  background-color: #1e293b;
  color: #60a5fa;
  padding-left: 2.5rem;
}

/* ======================
   CONTEÚDO PRINCIPAL 
   ====================== */
.main-content { 
  margin: 0 auto; 
}

/* ======================
   SEÇÃO HERO 
   ====================== */
.hero-section { 
  position: relative; 
  overflow: hidden; 
  width: 100%; 
  padding: 2rem 0 4rem; 
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
}

@media (min-width: 640px) {
  .hero-section { padding: 3rem 0 5rem; }
}

@media (min-width: 1024px) { 
  .hero-section { padding: 6rem 0 8rem; } 
}

.hero-bg-overlay { 
  position: absolute; 
  inset: 0; 
  background: radial-gradient(circle at 30% 40%, rgba(96, 165, 250, 0.2), transparent 50%);
}

.hero-bg-accent { 
  position: absolute; 
  top: 0; 
  right: 0; 
  width: 60%; 
  height: 100%; 
  background: linear-gradient(to left, rgba(30, 41, 59, 0.6), transparent); 
}

.hero-content { 
  position: relative; 
  max-width: 1000px; 
  margin: 0 auto; 
  padding: 0 1rem; 
  text-align: center; 
}

@media (min-width: 640px) {
  .hero-content {
    padding: 0 1.5rem;
  }
}

.hero-badge { 
  display: inline-flex; 
  align-items: center; 
  gap: 0.75rem; 
  padding: 0.75rem 1.5rem; 
  border-radius: 50px; 
  background: linear-gradient(135deg, #1e293b, #334155); 
  color: #60a5fa; 
  font-size: 0.9rem; 
  font-weight: 600; 
  margin-bottom: 2rem; 
  border: 1px solid #475569;
}

.hero-badge-icon { 
  width: 1.25rem; 
  height: 1.25rem; 
}

.hero-title { 
  font-size: 1.875rem; 
  font-weight: 900; 
  color: #f1f5f9; 
  margin-bottom: 1.5rem; 
  line-height: 1.2; 
  letter-spacing: -0.025em;
}

@media (min-width: 480px) {
  .hero-title { font-size: 2.25rem; }
}

@media (min-width: 768px) { 
  .hero-title { 
    font-size: 3.5rem; 
    margin-bottom: 2rem;
  } 
}

@media (min-width: 1024px) { 
  .hero-title { font-size: 4rem; } 
}

.hero-title-accent { 
  display: block; 
  background: linear-gradient(135deg, #60a5fa, #3b82f6, #8b5cf6); 
  background-clip: text; 
  -webkit-background-clip: text; 
  color: transparent; 
  margin-top: 0.5rem;
}

.hero-description { 
  font-size: 1rem; 
  color: #cbd5e1; 
  margin-bottom: 2rem; 
  line-height: 1.6; 
  max-width: 800px; 
  margin-left: auto; 
  margin-right: auto; 
  font-weight: 400;
  padding: 0 0.5rem;
}

@media (min-width: 480px) {
  .hero-description { 
    font-size: 1.125rem; 
    padding: 0;
  }
}

@media (min-width: 768px) { 
  .hero-description { 
    font-size: 1.375rem; 
    margin-bottom: 3rem;
  } 
}

/* ======================
   BARRA DE PESQUISA 
   ====================== */
.search-container { 
  max-width: 700px; 
  margin: 0 auto 2.5rem; 
}

.search-form { 
  display: flex; 
  flex-direction: column; 
  gap: 0.75rem; 
  background: #1e293b;
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  border: 1px solid #334155;
}

@media (min-width: 480px) {
  .search-form {
    padding: 1.25rem;
    gap: 1rem;
  }
}

@media (min-width: 640px) { 
  .search-form { 
    flex-direction: row; 
    padding: 1rem;
  } 
}

.search-input-wrapper { 
  position: relative; 
  flex: 1; 
}

.search-icon { 
  position: absolute; 
  left: 1.25rem; 
  top: 50%; 
  transform: translateY(-50%); 
  width: 1.5rem; 
  height: 1.5rem; 
  color: #64748b; 
}

.search-input { 
  width: 100%; 
  height: 3rem; 
  padding-left: 3.5rem; 
  padding-right: 1rem; 
  border-radius: 0.75rem; 
  border: 2px solid #475569; 
  color: #f1f5f9; 
  font-size: 0.9rem;
  transition: all 0.2s ease; 
  background-color: #334155;
}

@media (min-width: 480px) {
  .search-input {
    height: 3.5rem;
    padding-right: 1.5rem;
    font-size: 1rem;
  }
}

.search-input:focus { 
  border-color: #60a5fa; 
  outline: none; 
  background-color: #1e293b;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
}

.search-input::placeholder { 
  color: #64748b; 
  font-weight: 400;
}

.search-button { 
  height: 3rem; 
  padding: 0 1.5rem; 
  background: linear-gradient(135deg, #60a5fa, #3b82f6); 
  color: white; 
  font-weight: 600; 
  border-radius: 0.75rem; 
  transition: all 0.2s ease; 
  box-shadow: 0 4px 14px 0 rgba(96, 165, 250, 0.4);
  white-space: nowrap; 
  border: none; 
  cursor: pointer; 
  font-size: 0.9rem;
  min-width: 120px;
}

@media (min-width: 480px) {
  .search-button {
    height: 3.5rem;
    padding: 0 2.5rem;
    font-size: 1rem;
    min-width: auto;
  }
}

.search-button:hover:not(:disabled) { 
  background: linear-gradient(135deg, #3b82f6, #2563eb); 
  box-shadow: 0 6px 20px 0 rgba(96, 165, 250, 0.5);
  transform: translateY(-1px);
}

.search-button:disabled { 
  background: linear-gradient(135deg, #64748b, #475569); 
  cursor: not-allowed; 
  transform: none;
  box-shadow: none;
}

/* ======================
   CARACTERÍSTICAS DO HERO 
   ====================== */
.hero-features { 
  display: flex; 
  flex-direction: column; 
  align-items: center; 
  justify-content: center; 
  gap: 1.5rem; 
  font-size: 1rem; 
  color: #94a3b8; 
  margin-bottom: 4rem; 
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 1rem;
  backdrop-filter: blur(10px);
  border: 1px solid #475569;
}

@media (min-width: 640px) { 
  .hero-features { 
    flex-direction: row; 
    padding: 1rem 2rem;
  } 
}

.hero-feature { 
  display: flex; 
  align-items: center; 
  gap: 0.75rem; 
  font-weight: 500;
}

.hero-feature-icon { 
  width: 1.25rem; 
  height: 1.25rem; 
  color: #34d399; 
}

/* ======================
   GRID DE ESTATÍSTICAS 
   ====================== */
.stats-grid { 
  max-width: 900px; 
  margin: 0 auto; 
  display: grid; 
  grid-template-columns: repeat(2, minmax(0, 1fr)); 
  gap: 1.5rem; 
}

@media (min-width: 768px) { 
  .stats-grid { 
    grid-template-columns: repeat(4, minmax(0, 1fr)); 
    gap: 2rem;
  } 
}

.stat-card { 
  background: linear-gradient(135deg, #1e293b, #334155); 
  border-radius: 1.25rem; 
  padding: 2rem 1.5rem; 
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2); 
  border: 1px solid #475569; 
  transition: all 0.2s ease;
  text-align: center;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  border-color: #60a5fa;
}

@media (min-width: 768px) { 
  .stat-card { 
    padding: 2.5rem 2rem; 
  } 
}

.stat-icon { 
  width: 2rem; 
  height: 2rem; 
  margin: 0 auto 1rem; 
}

@media (min-width: 768px) { 
  .stat-icon { 
    width: 2.5rem; 
    height: 2.5rem; 
  } 
}

.stat-icon-blue { color: #60a5fa; }
.stat-icon-green { color: #34d399; }
.stat-icon-purple { color: #a78bfa; }
.stat-icon-orange { color: #fb923c; }

.stat-number { 
  font-size: 1.75rem; 
  font-weight: 800; 
  color: #f1f5f9; 
  margin-bottom: 0.5rem; 
  text-align: center; 
}

@media (min-width: 768px) { 
  .stat-number { 
    font-size: 2.5rem; 
  } 
}

.stat-label { 
  font-size: 0.875rem; 
  color: #94a3b8; 
  text-align: center; 
  font-weight: 500;
  line-height: 1.4;
}

@media (min-width: 768px) { 
  .stat-label { 
    font-size: 1rem; 
  } 
}

/* ======================
   SEÇÃO PROBLEMA/SOLUÇÃO 
   ====================== */
.problem-solution-section { 
  padding: 3rem 0; 
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
}

@media (min-width: 768px) {
  .problem-solution-section {
    padding: 4rem 0;
  }
}

@media (min-width: 1024px) {
  .problem-solution-section {
    padding: 6rem 0;
  }
}

.problem-solution-container { 
  max-width: 1100px; 
  margin: 0 auto; 
  padding: 0 1rem; 
}

@media (min-width: 640px) {
  .problem-solution-container {
    padding: 0 1.5rem;
  }
}

.problem-solution-content { 
  max-width: 1000px; 
  margin: 0 auto; 
  display: grid;
  gap: 2rem;
}

@media (min-width: 768px) {
  .problem-solution-content {
    gap: 3rem;
  }
}

@media (min-width: 1024px) {
  .problem-solution-content {
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
  }
}

.problem-box, .solution-box { 
  display: flex; 
  flex-direction: column; 
  gap: 1rem; 
  padding: 1.5rem; 
  border-radius: 1.5rem; 
  text-align: left; 
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  border: 1px solid;
  transition: all 0.2s ease;
}

@media (min-width: 640px) {
  .problem-box, .solution-box {
    padding: 2rem;
    gap: 1.5rem;
  }
}

.problem-box:hover, .solution-box:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
}

.problem-box { 
  background: linear-gradient(135deg, #7f1d1d, #1e293b); 
  border-color: #991b1b;
}

.solution-box { 
  background: linear-gradient(135deg, #064e3b, #1e293b); 
  border-color: #059669;
}

@media (min-width: 768px) { 
  .problem-box, .solution-box { 
    flex-direction: row; 
    align-items: flex-start;
    padding: 3rem; 
  } 
}

.box-icon { 
  width: 2rem; 
  height: 2rem; 
  margin-top: 0.25rem; 
  flex-shrink: 0; 
}

.box-icon-red { color: #f87171; }
.box-icon-green { color: #34d399; }

.box-content { flex: 1; }

.box-content h3 { 
  font-size: 1.5rem; 
  font-weight: 700; 
  color: #f1f5f9; 
  margin-bottom: 1rem; 
  line-height: 1.3;
}

.box-content p { 
  color: #cbd5e1; 
  line-height: 1.7; 
  font-size: 1.1rem;
}

/* ======================
   SEÇÃO DE FUNCIONALIDADES 
   ====================== */
.features-section {
  padding: 4rem 0;
  background: #0f172a;
}

@media (min-width: 768px) {
  .features-section {
    padding: 6rem 0;
  }
}

@media (min-width: 1024px) {
  .features-section {
    padding: 8rem 0;
  }
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

@media (min-width: 640px) {
  .features-container {
    padding: 0 1.5rem;
  }
}

.features-header {
  text-align: center;
  margin-bottom: 3rem;
}

@media (min-width: 768px) {
  .features-header {
    margin-bottom: 4rem;
  }
}

@media (min-width: 1024px) {
  .features-header {
    margin-bottom: 5rem;
  }
}

.features-title {
  font-size: 1.875rem;
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 1rem;
  line-height: 1.2;
  padding: 0 0.5rem;
}

@media (min-width: 480px) {
  .features-title {
    font-size: 2.25rem;
    padding: 0;
  }
}

@media (min-width: 768px) {
  .features-title {
    font-size: 3rem;
    margin-bottom: 1.5rem;
  }
}

.features-description {
  font-size: 1rem;
  color: #94a3b8;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
  padding: 0 0.5rem;
}

@media (min-width: 480px) {
  .features-description {
    font-size: 1.125rem;
    padding: 0;
  }
}

@media (min-width: 768px) {
  .features-description {
    font-size: 1.25rem;
  }
}

.features-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .features-grid {
    gap: 2rem;
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 3rem;
  }
}

.feature-card {
  background: linear-gradient(135deg, #1e293b, #334155);
  border-radius: 1.5rem;
  padding: 2rem 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  border: 1px solid #475569;
  transition: all 0.3s ease;
  text-align: left;
}

@media (min-width: 640px) {
  .feature-card {
    padding: 2.5rem 2rem;
  }
}

@media (min-width: 1024px) {
  .feature-card {
    padding: 3rem 2.5rem;
  }
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  border-color: #60a5fa;
}

.feature-card-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 1rem;
}

.feature-card-content p {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 2.5rem 0;
}

.feature-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #cbd5e1;
  line-height: 1.5;
}

.feature-check-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #34d399;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.feature-button {
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  color: white;
  border: none;
  padding: 0.875rem 2rem;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  font-size: 1rem;
}

.feature-button:hover {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  transform: translateY(-1px);
}


/* ======================
   SEÇÃO "COMO FUNCIONA" 
   ====================== */
.how-it-works-section {
  padding: 8rem 0;
  background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #334155 100%);
}

.how-it-works-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.how-it-works-header {
  text-align: center;
  margin-bottom: 5rem;
}

.how-it-works-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

@media (min-width: 768px) {
  .how-it-works-title {
    font-size: 3rem;
  }
}

.how-it-works-description {
  font-size: 1.25rem;
  color: #94a3b8;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.6;
}

.steps-grid {
  display: grid;
  gap: 3rem;
  grid-template-columns: 1fr;
}

@media (min-width: 1024px) {
  .steps-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }
}

.step-card {
  background: linear-gradient(135deg, #334155, #1e293b);
  border-radius: 1.5rem;
  padding: 3rem 2.5rem;
  text-align: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  border: 1px solid #475569;
  transition: all 0.3s ease;
  position: relative;
}

.step-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  border-color: #60a5fa;
}

.step-content {
  position: relative;
  z-index: 1;
}

.step-icon-wrapper {
  width: 4rem;
  height: 4rem;
  background: linear-gradient(135deg, #1e293b, #334155);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 2rem;
  border: 1px solid #60a5fa;
}

.step-icon {
  width: 2rem;
  height: 2rem;
  color: #60a5fa;
}

.step-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 1rem;
  line-height: 1.3;
}

.step-description {
  color: #94a3b8;
  line-height: 1.6;
  font-size: 1.1rem;
}

/* ======================
   SEÇÃO METODOLOGIA 
   ====================== */
.methodology-section {
  padding: 8rem 0;
  background: #0f172a;
}

.methodology-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.methodology-card {
  background: linear-gradient(135deg, #1e293b, #334155);
  border-radius: 2rem;
  padding: 4rem 3rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  border: 1px solid #475569;
}

.methodology-content {
  max-width: 1000px;
  margin: 0 auto;
}

.methodology-header {
  text-align: center;
  margin-bottom: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.methodology-shield-icon {
  width: 3rem;
  height: 3rem;
  color: #60a5fa;
}

.methodology-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #f1f5f9;
  line-height: 1.2;
}

@media (min-width: 768px) {
  .methodology-title {
    font-size: 3rem;
  }
}

.methodology-grid {
  display: grid;
  gap: 3rem;
  margin-bottom: 3rem;
}

@media (min-width: 1024px) {
  .methodology-grid {
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
  }
}

.methodology-item {
  background: linear-gradient(135deg, #334155, #1e293b);
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  border: 1px solid #475569;
}

.methodology-subtitle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.375rem;
  font-weight: 700;
  color: #f1f5f9;
  margin-bottom: 1.5rem;
}

.methodology-title-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #60a5fa;
}

.methodology-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.methodology-list-item {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: #cbd5e1;
  line-height: 1.6;
  font-size: 1.1rem;
}

.methodology-check-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #34d399;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.methodology-commitment {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  padding: 2.5rem;
  border-radius: 1.5rem;
  border: 1px solid #60a5fa;
  text-align: center;
}

.methodology-commitment p {
  color: #cbd5e1;
  line-height: 1.7;
  font-size: 1.1rem;
  margin: 0;
}

/* ======================
   SEÇÃO CTA 
   ====================== */
.cta-section {
  padding: 8rem 0;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: white;
}

.cta-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  color: #f1f5f9;
}

@media (min-width: 768px) {
  .cta-title {
    font-size: 3rem;
  }
}

.cta-description {
  font-size: 1.25rem;
  color: #cbd5e1;
  margin-bottom: 3rem;
  line-height: 1.6;
}

.cta-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (min-width: 640px) {
  .cta-buttons {
    flex-direction: row;
    justify-content: center;
    gap: 1.5rem;
  }
}

.cta-button-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  color: white;
  border: none;
  padding: 1rem 2.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cta-button-primary:hover {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  transform: translateY(-2px);
}

.cta-button-secondary {
  background: transparent;
  color: #f1f5f9;
  border: 2px solid #64748b;
  padding: 1rem 2.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cta-button-secondary:hover {
  background: #334155;
  border-color: #94a3b8;
}

.cta-arrow-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.cta-note {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

/* ======================
   FOOTER 
   ====================== */
.footer {
  background: #0f172a;
  color: white;
  padding: 4rem 0 2rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1.5rem;
}

.footer-grid {
  display: grid;
  gap: 3rem;
  margin-bottom: 3rem;
}

@media (min-width: 1024px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr 1fr;
    gap: 4rem;
  }
}

.footer-brand-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.footer-shield-icon {
  width: 2rem;
  height: 2rem;
  color: #3b82f6;
}

.footer-brand-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.footer-brand-description {
  color: #94a3b8;
  line-height: 1.6;
  font-size: 1rem;
}

.footer-section-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
  margin-bottom: 1rem;
}

.footer-section-description {
  color: #94a3b8;
  line-height: 1.6;
  font-size: 1rem;
}

.footer-list {
  list-style: none;
  padding: 0;
  margin: 0;
  color: #94a3b8;
  line-height: 1.6;
}

.footer-list li {
  margin-bottom: 0.5rem;
}

.footer-bottom {
  border-top: 1px solid #334155;
  padding-top: 2rem;
  text-align: center;
}

.footer-copyright {
  color: #94a3b8;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.footer-credits {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0;
}

/* ======================
   SEÇÃO DE RESULTADOS DA BUSCA (Melhorada)
   ====================== */
.results-section {
  background: linear-gradient(135deg, #1e293b, #0f172a);
  padding: 4rem 1.5rem;
  border-top: 1px solid #475569;
}

.results-container {
  max-width: 900px;
  margin: 0 auto;
  text-align: left;
}

.results-container h2 {
  font-size: 2rem;
  font-weight: 800;
  color: #f1f5f9;
  margin-bottom: 2.5rem;
  text-align: center;
}

.results-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 1rem;
}

.result-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border: 1px solid #475569;
  border-radius: 1rem;
  background: linear-gradient(135deg, #334155, #1e293b);
  text-decoration: none;
  color: #f1f5f9;
  font-weight: 500;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3);
}

.result-item:hover {
  border-color: #60a5fa;
  background: linear-gradient(135deg, #1e293b, #334155);
  transform: translateY(-4px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
}

.result-item span:first-child { 
  font-weight: 600; 
  font-size: 1.1rem;
  color: #f1f5f9;
}

.result-item span:last-child { 
  color: #60a5fa; 
  font-weight: 600;
  font-size: 0.95rem;
}

.feedback-message {
  text-align: center;
  color: #94a3b8;
  font-size: 1.1rem;
  padding: 3rem 2rem;
  background: linear-gradient(135deg, #334155, #1e293b);
  border-radius: 1rem;
  border: 1px solid #475569;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3);
}

.error-message {
  max-width: 900px;
  margin: 0 auto;
  color: #f87171;
  background: linear-gradient(135deg, #7f1d1d, #1e293b);
  border: 1px solid #991b1b;
  border-radius: 1rem;
}

.error-message h3 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #f87171;
}

/* ==================================================== */
/*          CSS PARA O AUTOCOMPLETE (ADICIONAL)       */
/* ==================================================== */
.search-autocomplete-wrapper {
  position: relative;
  max-width: 700px;
  margin: 0 auto 2.5rem;
}

.autocomplete-results {
  position: absolute;
  top: calc(100% - 1rem);
  left: 1rem;
  right: 1rem;
  background: linear-gradient(180deg, #1e293b, #0f172a);
  border: 1px solid #475569;
  border-top: none;
  border-radius: 0 0 1rem 1rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
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
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease;
  border-bottom: 1px solid #334155;
  color: #cbd5e1;
}

.autocomplete-results li:last-child {
  border-bottom: none;
}

.autocomplete-results li:hover,
.autocomplete-results li.is-active {
  background-color: #3b82f6;
  color: #ffffff;
}

.autocomplete-feedback {
  padding: 1rem 1.5rem;
  color: #94a3b8;
  font-style: italic;
}

</style>