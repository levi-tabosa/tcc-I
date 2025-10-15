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

          <!-- Search Bar -->
          <div class="search-container">
            <form @submit="handleSearch" class="search-form">
              <div class="search-input-wrapper">
                <Search class="search-icon" />
                <input 
                  v-model="searchQuery"
                  type="text"
                  placeholder="Busque por parlamentar, partido ou proposição..."
                  class="search-input"
                />
              </div>
              <button 
                type="submit"
                class="search-button"
              >
                Buscar
              </button>
            </form>
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
import { ref } from 'vue'
import { 
  Search, 
  TrendingUp, 
  Users, 
  FileText, 
  Shield, 
  Eye, 
  ArrowRight, 
  Database, 
  BarChart3, 
  CheckCircle2, 
  AlertCircle,
  BarChart,
  RefreshCw
} from 'lucide-vue-next'

const searchQuery = ref('')

const handleSearch = (e: Event) => {
  e.preventDefault()
  console.log('Buscando por:', searchQuery.value)
}

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
/* Page wrapper */
.page-wrapper {
  min-height: 100vh;
  background: linear-gradient(180deg, var(--color-gray-50), var(--color-white));
}

/* Header */
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(12px);
  background-color: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid var(--color-gray-200);
}

.header-container {
  max-width: 72rem;
  margin: 0 auto;
  padding: var(--space-4);
}

.nav {
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (min-width: 768px) {
  .nav {
    justify-content: space-between;
  }
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.nav-icon {
  width: var(--space-8);
  height: var(--space-8);
  color: var(--color-primary);
}

.nav-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  background: linear-gradient(to right, var(--color-primary), var(--color-primary-dark));
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.nav-links {
  display: none;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  color: var(--color-gray-600);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.15s ease-in-out;
}

.nav-link:hover {
  color: var(--color-primary);
}

/* Main content */
.main-content {
  margin: 0 auto;
  text-align: center;
}

/* Hero section */
.hero-section {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding: var(--space-20) 0;
}

@media (min-width: 1024px) {
  .hero-section {
    padding: var(--space-32) 0;
  }
}

.hero-bg-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, #eff6ff, var(--color-white), var(--color-gray-50));
  opacity: 0.7;
}

.hero-bg-accent {
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  background: linear-gradient(to left, rgba(219, 234, 254, 0.3), transparent);
}

.hero-content {
  position: relative;
  max-width: 56rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  background-color: #dbeafe;
  color: var(--color-primary-dark);
  font-size: var(--font-size-sm);
  font-weight: 600;
  margin-bottom: var(--space-6);
}

.hero-badge-icon {
  width: var(--space-4);
  height: var(--space-4);
}

.hero-title {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--color-gray-900);
  margin-bottom: var(--space-6);
  line-height: 1.25;
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }
}

@media (min-width: 1024px) {
  .hero-title {
    font-size: 3.75rem;
  }
}

.hero-title-accent {
  display: block;
  background: linear-gradient(to right, var(--color-primary), var(--color-primary-dark));
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

.hero-description {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  margin-bottom: var(--space-8);
  line-height: 1.625;
  max-width: 48rem;
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 768px) {
  .hero-description {
    font-size: var(--font-size-xl);
  }
}

/* Search */
.search-container {
  max-width: 42rem;
  margin: 0 auto var(--space-6);
}

.search-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

@media (min-width: 640px) {
  .search-form {
    flex-direction: row;
  }
}

.search-input-wrapper {
  position: relative;
  flex: 1;
}

.search-icon {
  position: absolute;
  left: var(--space-4);
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-gray-400);
}

.search-input {
  width: 100%;
  height: 3.5rem;
  padding-left: var(--space-12);
  padding-right: var(--space-4);
  border-radius: var(--radius-xl);
  border: 2px solid var(--color-gray-200);
  color: var(--color-gray-900);
  transition: border-color 0.15s ease-in-out;
}

.search-input:focus {
  border-color: var(--color-primary-light);
  outline: none;
}

.search-input::placeholder {
  color: var(--color-gray-400);
}

.search-button {
  height: 3.5rem;
  padding: 0 var(--space-8);
  background: linear-gradient(to right, var(--color-primary), var(--color-primary-dark));
  color: var(--color-white);
  font-weight: 600;
  border-radius: var(--radius-xl);
  transition: all 0.15s ease-in-out;
  box-shadow: var(--shadow-lg);
  white-space: nowrap;
}

.search-button:hover {
  background: linear-gradient(to right, var(--color-primary-dark), #1e40af);
  box-shadow: var(--shadow-xl);
}

/* Hero features */
.hero-features {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-gray-500);
  margin-bottom: var(--space-12);
}

@media (min-width: 640px) {
  .hero-features {
    flex-direction: row;
  }
}

.hero-feature {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.hero-feature-icon {
  width: var(--space-4);
  height: var(--space-4);
  color: var(--color-success);
}

/* Stats grid */
.stats-grid {
  max-width: 42rem;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--space-4);
}

.stat-card {
  background-color: var(--color-white);
  border-radius: var(--radius-2xl);
  padding: var(--space-4);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-gray-100);
}

@media (min-width: 768px) {
  .stat-card {
    padding: var(--space-6);
  }
}

.stat-icon {
  width: var(--space-6);
  height: var(--space-6);
  margin: 0 auto var(--space-3);
}

@media (min-width: 768px) {
  .stat-icon {
    width: var(--space-8);
    height: var(--space-8);
  }
}

.stat-icon-blue {
  color: var(--color-primary);
}

.stat-icon-green {
  color: var(--color-success);
}

.stat-icon-purple {
  color: #9333ea;
}

.stat-icon-orange {
  color: #ea580c;
}

.stat-number {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-1);
  text-align: center;
}

@media (min-width: 768px) {
  .stat-number {
    font-size: var(--font-size-4xl);
  }
}

.stat-label {
  font-size: var(--font-size-xs);
  color: var(--color-gray-600);
  text-align: center;
}

@media (min-width: 768px) {
  .stat-label {
    font-size: var(--font-size-sm);
  }
}

/* Problem/Solution section */
.problem-solution-section {
  padding: var(--space-20) 0;
  background-color: var(--color-white);
}

.problem-solution-container {
  max-width: 64rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.problem-solution-content {
  max-width: 56rem;
  margin: 0 auto;
}

.problem-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-6);
  background-color: #fef2f2;
  border-left: 4px solid var(--color-error);
  border-radius: 0 var(--radius-2xl) var(--radius-2xl) 0;
  margin-bottom: var(--space-8);
  text-align: center;
}

@media (min-width: 768px) {
  .problem-box {
    flex-direction: row;
    padding: var(--space-8);
    text-align: left;
  }
}

.solution-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-4);
  padding: var(--space-6);
  background-color: #ecfdf5;
  border-left: 4px solid var(--color-success);
  border-radius: 0 var(--radius-2xl) var(--radius-2xl) 0;
  text-align: center;
}

@media (min-width: 768px) {
  .solution-box {
    flex-direction: row;
    padding: var(--space-8);
    text-align: left;
  }
}

.box-icon {
  width: var(--space-6);
  height: var(--space-6);
  margin-top: var(--space-1);
  flex-shrink: 0;
}

.box-icon-red {
  color: var(--color-error);
}

.box-icon-green {
  color: var(--color-success);
}

.box-content h3 {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-2);
}

.box-content p {
  color: var(--color-gray-700);
  line-height: 1.625;
}

/* Features section */
.features-section {
  padding: var(--space-20) 0;
  background-color: var(--color-gray-50);
}

.features-container {
  max-width: 64rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.features-header {
  text-align: center;
  margin-bottom: var(--space-16);
}

.features-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-4);
}

@media (min-width: 768px) {
  .features-title {
    font-size: var(--font-size-4xl);
  }
}

.features-description {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  max-width: 48rem;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .features-description {
    font-size: var(--font-size-xl);
  }
}

.features-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--space-6);
}

@media (min-width: 768px) {
  .features-grid {
    gap: var(--space-8);
  }
}

.feature-card {
  width: 100%;
  max-width: 24rem;
  background-color: var(--color-white);
  border-radius: var(--radius-2xl);
  padding: var(--space-6);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--color-gray-100);
  transition: box-shadow 0.15s ease-in-out;
}

@media (min-width: 768px) {
  .feature-card {
    padding: var(--space-8);
  }
}

.feature-card:hover {
  box-shadow: var(--shadow-xl);
}

.feature-card-content {
  text-align: center;
}

.feature-card h3 {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-3);
}

@media (min-width: 768px) {
  .feature-card h3 {
    font-size: var(--font-size-2xl);
  }
}

.feature-card p {
  color: var(--color-gray-600);
  margin-bottom: var(--space-6);
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--space-6) 0;
  text-align: left;
}

.feature-list li {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-gray-700);
  margin-bottom: var(--space-3);
}

.feature-list li:last-child {
  margin-bottom: 0;
}

.feature-check-icon {
  width: var(--space-4);
  height: var(--space-4);
  color: var(--color-success);
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.feature-button {
  width: 100%;
  padding: var(--space-3) 0;
  background-color: var(--color-gray-100);
  color: var(--color-gray-900);
  font-weight: 600;
  border-radius: var(--radius-xl);
  transition: background-color 0.15s ease-in-out;
  border: none;
  cursor: pointer;
}

.feature-button:hover {
  background-color: var(--color-gray-200);
}

/* How it works section */
.how-it-works-section {
  padding: var(--space-20) 0;
  background-color: var(--color-white);
}

.how-it-works-container {
  max-width: 64rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.how-it-works-header {
  text-align: center;
  margin-bottom: var(--space-16);
}

.how-it-works-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-4);
}

@media (min-width: 768px) {
  .how-it-works-title {
    font-size: var(--font-size-4xl);
  }
}

.how-it-works-description {
  font-size: var(--font-size-lg);
  color: var(--color-gray-600);
  max-width: 48rem;
  margin: 0 auto;
}

@media (min-width: 768px) {
  .how-it-works-description {
    font-size: var(--font-size-xl);
  }
}

.steps-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: var(--space-8);
}

@media (min-width: 768px) {
  .steps-grid {
    gap: var(--space-12);
  }
}

.step-card {
  position: relative;
  text-align: center;
  max-width: 20rem;
}

.step-content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.step-icon-wrapper {
  position: relative;
  width: var(--space-20);
  height: var(--space-20);
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  border-radius: var(--radius-2xl);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-white);
  margin-bottom: var(--space-6);
  box-shadow: var(--shadow-lg);
}

.step-icon {
  width: var(--space-8);
  height: var(--space-8);
}

.step-title {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-3);
}

.step-description {
  color: var(--color-gray-600);
  line-height: 1.625;
}

/* Methodology section */
.methodology-section {
  padding: var(--space-20) 0;
  background-color: var(--color-gray-50);
}

.methodology-container {
  max-width: 64rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.methodology-card {
  background-color: var(--color-white);
  border-radius: var(--radius-3xl);
  padding: var(--space-8);
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-gray-100);
}

@media (min-width: 768px) {
  .methodology-card {
    padding: var(--space-12);
  }
}

.methodology-content {
  max-width: 56rem;
  margin: 0 auto;
  text-align: center;
}

.methodology-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  margin-bottom: var(--space-8);
}

.methodology-shield-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: var(--color-primary);
}

.methodology-title {
  font-size: var(--font-size-2xl);
  font-weight: 700;
  color: var(--color-gray-900);
}

@media (min-width: 768px) {
  .methodology-title {
    font-size: var(--font-size-3xl);
  }
}

.methodology-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-8);
  margin-bottom: var(--space-8);
  text-align: left;
}

@media (min-width: 768px) {
  .methodology-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.methodology-item h3 {
  font-size: var(--font-size-lg);
  font-weight: 700;
  color: var(--color-gray-900);
  margin-bottom: var(--space-4);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

@media (min-width: 768px) {
  .methodology-item h3 {
    text-align: left;
    justify-content: flex-start;
  }
}

.methodology-title-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-primary);
}

.methodology-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.methodology-list-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  color: var(--color-gray-700);
  margin-bottom: var(--space-2);
}

.methodology-list-item:last-child {
  margin-bottom: 0;
}

.methodology-check-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-success);
  margin-top: 0.125rem;
  flex-shrink: 0;
}

.methodology-commitment {
  background-color: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}

.methodology-commitment p {
  color: var(--color-gray-700);
  line-height: 1.625;
  text-align: center;
  margin: 0;
}

.methodology-commitment strong {
  color: var(--color-gray-900);
}

/* CTA section */
.cta-section {
  padding: var(--space-20) 0;
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark));
  color: var(--color-white);
}

.cta-container {
  max-width: 56rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
  text-align: center;
}

.cta-title {
  font-size: var(--font-size-3xl);
  font-weight: 700;
  margin-bottom: var(--space-6);
}

@media (min-width: 768px) {
  .cta-title {
    font-size: var(--font-size-4xl);
  }
}

@media (min-width: 1024px) {
  .cta-title {
    font-size: var(--font-size-5xl);
  }
}

.cta-description {
  font-size: var(--font-size-lg);
  color: #dbeafe;
  margin-bottom: 2.5rem;
  line-height: 1.625;
  max-width: 48rem;
  margin-left: auto;
  margin-right: auto;
}

@media (min-width: 768px) {
  .cta-description {
    font-size: var(--font-size-xl);
  }
}

.cta-buttons {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  justify-content: center;
  align-items: center;
}

@media (min-width: 640px) {
  .cta-buttons {
    flex-direction: row;
  }
}

.cta-button-primary {
  padding: var(--space-4) var(--space-8);
  background-color: var(--color-white);
  color: var(--color-primary-dark);
  font-weight: 700;
  border-radius: var(--radius-xl);
  transition: background-color 0.15s ease-in-out;
  box-shadow: var(--shadow-xl);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border: none;
  cursor: pointer;
}

@media (min-width: 768px) {
  .cta-button-primary {
    padding: var(--space-4) 2.5rem;
  }
}

.cta-button-primary:hover {
  background-color: #eff6ff;
}

.cta-arrow-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.cta-button-secondary {
  padding: var(--space-4) var(--space-8);
  background-color: var(--color-primary-dark);
  color: var(--color-white);
  font-weight: 700;
  border-radius: var(--radius-xl);
  transition: background-color 0.15s ease-in-out;
  border: 2px solid #60a5fa;
  cursor: pointer;
}

@media (min-width: 768px) {
  .cta-button-secondary {
    padding: var(--space-4) 2.5rem;
  }
}

.cta-button-secondary:hover {
  background-color: #1e40af;
}

.cta-note {
  font-size: var(--font-size-sm);
  color: #bfdbfe;
  margin-top: var(--space-8);
}

/* Footer */
.footer {
  background-color: var(--color-gray-900);
  color: #cbd5e1;
  padding: var(--space-12) 0;
}

.footer-container {
  max-width: 72rem;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-8);
  margin-bottom: var(--space-8);
  text-align: center;
}

@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(3, 1fr);
    text-align: left;
  }
}

.footer-brand {
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media (min-width: 768px) {
  .footer-brand {
    align-items: flex-start;
  }
}

.footer-brand-header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}

.footer-shield-icon {
  width: var(--space-6);
  height: var(--space-6);
  color: #60a5fa;
}

.footer-brand-name {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--color-white);
}

.footer-brand-description {
  font-size: var(--font-size-sm);
  color: var(--color-gray-400);
  line-height: 1.625;
  max-width: 20rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media (min-width: 768px) {
  .footer-section {
    align-items: flex-start;
  }
}

.footer-section-title {
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: var(--space-4);
}

.footer-section-description {
  font-size: var(--font-size-sm);
  color: var(--color-gray-400);
  max-width: 20rem;
}

.footer-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-list li {
  font-size: var(--font-size-sm);
  color: var(--color-gray-400);
  margin-bottom: var(--space-2);
}

.footer-list li:last-child {
  margin-bottom: 0;
}

.footer-bottom {
  border-top: 1px solid var(--color-gray-800);
  padding-top: var(--space-8);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  text-align: center;
}

@media (min-width: 768px) {
  .footer-bottom {
    flex-direction: row;
  }
}

.footer-copyright,
.footer-credits {
  font-size: var(--font-size-sm);
  color: var(--color-gray-500);
  margin: 0;
}
</style>