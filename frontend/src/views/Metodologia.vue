"""
Replace React/Next content with a Vue Single File Component implementing the same UI
"""

<template>
  <div class="page-wrapper">
    
    <main class="main-content">
      <!-- Hero Section -->
      <section class="hero-section">
        <div class="container">
          <div class="hero-content">
            <h1 class="hero-title">
              Metodologia e Fontes
            </h1>
            <p class="hero-description">
              Transparência total sobre como coletamos, processamos e apresentamos os dados parlamentares
            </p>
          </div>
        </div>
      </section>

      <!-- Content Section -->
      <section class="content-section">
        <div class="container">
          <!-- Last Update Card -->
          <div class="info-card update-card">
            <div class="info-card-content">
              <div class="update-info">
                <Calendar class="update-icon" />
                <span class="update-label">Última atualização:</span>
                <span class="update-date">{{ lastUpdate }}</span>
              </div>
            </div>
          </div>

          <!-- Data Sources -->
          <div class="info-card">
            <div class="info-card-header">
              <div class="card-header-content">
                <Database class="card-icon" />
                <h2 class="card-title">Fontes de Dados</h2>
              </div>
              <p class="card-subtitle">Todos os dados são obtidos de fontes oficiais e públicas</p>
            </div>
            
            <div class="info-card-content">
              <div class="sources-grid">
                <div class="source-item">
                  <h3 class="source-title">Portal da Câmara dos Deputados</h3>
                  <p class="source-description">
                    Dados de gastos parlamentares, presença em sessões e informações biográficas
                  </p>
                  <div class="source-links">
                    <span class="source-badge">API Dados Abertos</span>
                    <a
                      href="https://dadosabertos.camara.leg.br/swagger/api.html"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="external-link"
                    >
                      Documentação da API
                      <ExternalLink class="external-icon" />
                    </a>
                  </div>
                </div>

                <div class="source-item">
                  <h3 class="source-title">Portal do Senado Federal</h3>
                  <p class="source-description">
                    Dados de senadores, votações nominais e atividade legislativa
                  </p>
                  <div class="source-links">
                    <span class="source-badge">API Dados Abertos</span>
                    <a
                      href="https://legis.senado.leg.br/dadosabertos/"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="external-link"
                    >
                      Documentação da API
                      <ExternalLink class="external-icon" />
                    </a>
                  </div>
                </div>

                <div class="source-item">
                  <h3 class="source-title">Tribunal Superior Eleitoral (TSE)</h3>
                  <p class="source-description">
                    Informações sobre filiação partidária e histórico eleitoral
                  </p>
                  <div class="source-links">
                    <span class="source-badge">Dados Públicos</span>
                    <a
                      href="https://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="external-link"
                    >
                      Portal TSE
                      <ExternalLink class="external-icon" />
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Methodology -->
          <div class="info-card">
            <div class="info-card-header">
              <div class="card-header-content">
                <Code class="card-icon" />
                <h2 class="card-title">Metodologia de Coleta</h2>
              </div>
              <p class="card-subtitle">Como processamos e validamos os dados</p>
            </div>
            
            <div class="info-card-content">
              <div class="methodology-steps">
                <div class="step-item">
                  <div class="step-number">1</div>
                  <div class="step-content">
                    <h3 class="step-title">Coleta Automatizada</h3>
                    <p class="step-description">
                      Os dados são coletados diariamente através de scripts automatizados que consultam as APIs oficiais.
                      Utilizamos endpoints REST documentados publicamente e seguimos as boas práticas de rate limiting para
                      não sobrecarregar os servidores públicos.
                    </p>
                  </div>
                </div>

                <div class="step-item">
                  <div class="step-number">2</div>
                  <div class="step-content">
                    <h3 class="step-title">Validação e Limpeza</h3>
                    <p class="step-description">
                      Todos os dados passam por validação de integridade, verificação de tipos e normalização de formatos.
                      Registros duplicados são removidos e inconsistências são sinalizadas para revisão manual.
                    </p>
                  </div>
                </div>

                <div class="step-item">
                  <div class="step-number">3</div>
                  <div class="step-content">
                    <h3 class="step-title">Cálculo de Métricas</h3>
                    <p class="step-description">
                      As métricas apresentadas (presença, fidelidade partidária, gastos totais) são calculadas com base nos
                      dados brutos oficiais. A fórmula de cada métrica está documentada no nosso repositório público.
                    </p>
                  </div>
                </div>

                <div class="step-item">
                  <div class="step-number">4</div>
                  <div class="step-content">
                    <h3 class="step-title">Detecção de Anomalias</h3>
                    <p class="step-description">
                      Utilizamos análise estatística (desvio padrão e quartis) para identificar gastos atípicos. Um gasto é
                      considerado anomalia quando está 2 desvios padrão acima da média ou no percentil 95+.
                    </p>
                  </div>
                </div>

                <div class="step-item">
                  <div class="step-number">5</div>
                  <div class="step-content">
                    <h3 class="step-title">Atualização Contínua</h3>
                    <p class="step-description">
                      A plataforma é atualizada diariamente às 3h da manhã (horário de Brasília). Dados históricos são
                      preservados para permitir análise temporal.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Legal Basis -->
          <div class="info-card">
            <div class="info-card-header">
              <div class="card-header-content">
                <Shield class="card-icon" />
                <h2 class="card-title">Base Legal e Conformidade</h2>
              </div>
              <p class="card-subtitle">Fundamentos legais para acesso e publicação dos dados</p>
            </div>
            
            <div class="info-card-content">
              <div class="legal-grid">
                <div class="legal-item">
                  <h3 class="legal-title">Lei de Acesso à Informação (LAI)</h3>
                  <p class="legal-description">
                    Lei nº 12.527/2011 - Garante o acesso a informações públicas e estabelece que dados sobre atividades
                    parlamentares devem ser disponibilizados de forma proativa.
                  </p>
                  <a
                    href="http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2011/lei/l12527.htm"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="external-link"
                  >
                    Ler texto completo da LAI
                    <ExternalLink class="external-icon" />
                  </a>
                </div>

                <div class="legal-item">
                  <h3 class="legal-title">Lei Geral de Proteção de Dados (LGPD)</h3>
                  <p class="legal-description">
                    Lei nº 13.709/2018 - Todos os dados apresentados são de natureza pública e referem-se a agentes públicos
                    no exercício de suas funções. Não coletamos dados pessoais de usuários da plataforma além do necessário
                    para o formulário de feedback.
                  </p>
                  <a
                    href="http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="external-link"
                  >
                    Ler texto completo da LGPD
                    <ExternalLink class="external-icon" />
                  </a>
                </div>

                <div class="legal-item full-width">
                  <h3 class="legal-title">Princípios Éticos</h3>
                  <p class="legal-description">
                    Esta plataforma apresenta apenas fatos e dados oficiais, sem interpretações opinativas. Nosso objetivo é
                    facilitar o acesso à informação pública e promover a transparência, não fazer julgamentos políticos ou
                    partidários.
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Open Source -->
          <div class="info-card">
            <div class="info-card-header">
              <div class="card-header-content">
                <GitBranch class="card-icon" />
                <h2 class="card-title">Código Aberto</h2>
              </div>
              <p class="card-subtitle">Transparência também no código</p>
            </div>
            
            <div class="info-card-content">
              <p class="opensource-description">
                Todo o código-fonte desta plataforma está disponível publicamente no GitHub. Você pode auditar nossos
                métodos de coleta, cálculo de métricas e detecção de anomalias. Contribuições e sugestões são bem-vindas.
              </p>
              <a
                class="cta-button"
                href="https://github.com/seu-usuario/transparencia-parlamentar"
                target="_blank"
                rel="noopener noreferrer"
              >
                <GitBranch class="button-icon" />
                Ver repositório no GitHub
              </a>
            </div>
          </div>

          <!-- Limitations -->
          <div class="info-card limitations-card">
            <div class="info-card-header">
              <div class="card-header-content">
                <h2 class="card-title">Limitações e Avisos</h2>
              </div>
            </div>
            
            <div class="info-card-content">
              <div class="limitations-list">
                <div class="limitation-item">
                  <strong class="limitation-label">Dados em tempo real:</strong>
                  <span class="limitation-text">Existe um delay de até 24 horas entre a publicação oficial e a disponibilização nesta plataforma.</span>
                </div>
                <div class="limitation-item">
                  <strong class="limitation-label">Responsabilidade:</strong>
                  <span class="limitation-text">Nos esforçamos para garantir a precisão dos dados, mas erros podem ocorrer. Sempre consulte as fontes oficiais para decisões importantes.</span>
                </div>
                <div class="limitation-item">
                  <strong class="limitation-label">Interpretação:</strong>
                  <span class="limitation-text">As métricas apresentadas são calculadas automaticamente e não substituem análise contextual aprofundada.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- CTA -->
          <div class="info-card cta-card">
            <div class="info-card-content">
              <div class="cta-content">
                <div class="cta-text">
                  <h3 class="cta-title">Encontrou algum erro?</h3>
                  <p class="cta-description">Ajude-nos a melhorar reportando inconsistências</p>
                </div>
                <RouterLink to="/contato" class="cta-button primary">
                  Enviar Feedback
                </RouterLink>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
/*
  Converted from React/Next page to Vue SFC. Uses existing app styles and lucide-vue-next icons.
*/
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { Database, Shield, Code, Calendar, GitBranch, ExternalLink } from 'lucide-vue-next'

const now = new Date()
const lastUpdate = computed(() =>
  now.toLocaleString('pt-BR', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
)
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

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* ======================
   SEÇÃO HERO 
   ====================== */
.hero-section {
  position: relative;
  overflow: hidden;
  width: 100%;
  padding: 4rem 0 6rem;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 100%);
}

.hero-content {
  position: relative;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1rem;
  text-align: center;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-gray-900);
  margin-bottom: 1.5rem;
  line-height: 1.2;
  letter-spacing: -0.025em;
}

@media (min-width: 768px) {
  .hero-title {
    font-size: 3.5rem;
    margin-bottom: 2rem;
  }
}

.hero-description {
  font-size: 1.125rem;
  color: var(--color-gray-600);
  margin-bottom: 3rem;
  line-height: 1.6;
  max-width: 700px;
  margin-left: auto;
  margin-right: auto;
}

/* ======================
   SEÇÃO DE CONTEÚDO 
   ====================== */
.content-section {
  padding: 0 0 6rem;
  margin-top: -3rem;
  position: relative;
  z-index: 2;
}

.info-card {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  margin-bottom: 2rem;
  transition: all 0.3s ease;
}

.info-card:hover {
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border-color: var(--color-primary);
}

.info-card-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid var(--color-gray-100);
}

.card-header-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.card-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-primary);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-gray-900);
  margin: 0;
}

.card-subtitle {
  font-size: 1rem;
  color: var(--color-gray-600);
  margin: 0;
  line-height: 1.5;
}

.info-card-content {
  padding: 2rem;
}

/* ======================
   CARD DE ATUALIZAÇÃO 
   ====================== */
.update-card {
  border-color: rgba(59, 130, 246, 0.3);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.02), var(--color-white));
}

.update-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.95rem;
}

.update-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-primary);
}

.update-label {
  font-weight: 600;
  color: var(--color-gray-900);
}

.update-date {
  color: var(--color-gray-600);
}

/* ======================
   GRID DE FONTES 
   ====================== */
.sources-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .sources-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .sources-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.source-item {
  padding: 1.5rem;
  border: 1px solid var(--color-gray-200);
  border-radius: 0.75rem;
  background: var(--color-gray-50);
  border-left: 4px solid var(--color-primary);
  transition: all 0.2s ease;
}

.source-item:hover {
  background: var(--color-white);
  border-color: var(--color-primary);
  transform: translateY(-2px);
}

.source-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 0.75rem;
}

.source-description {
  font-size: 0.9rem;
  color: var(--color-gray-600);
  line-height: 1.5;
  margin-bottom: 1rem;
}

.source-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  align-items: flex-start;
}

.source-badge {
  display: inline-block;
  padding: 0.375rem 0.75rem;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.external-link {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.85rem;
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
}

.external-link:hover {
  color: var(--color-primary-dark);
  text-decoration: underline;
}

.external-icon {
  width: 0.75rem;
  height: 0.75rem;
}

/* ======================
   METODOLOGIA STEPS 
   ====================== */
.methodology-steps {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.step-item {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.step-number {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  background: linear-gradient(135deg, var(--color-primary), #2563eb);
  color: var(--color-white);
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.125rem;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 0.75rem;
}

.step-description {
  color: var(--color-gray-600);
  line-height: 1.6;
  font-size: 0.95rem;
}

/* ======================
   GRID LEGAL 
   ====================== */
.legal-grid {
  display: grid;
  gap: 2rem;
  grid-template-columns: 1fr;
}

@media (min-width: 768px) {
  .legal-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.legal-item {
  padding: 1.5rem;
  border: 1px solid var(--color-gray-200);
  border-radius: 0.75rem;
  background: var(--color-gray-50);
  transition: all 0.2s ease;
}

.legal-item.full-width {
  grid-column: 1 / -1;
}

.legal-item:hover {
  background: var(--color-white);
  border-color: var(--color-primary);
}

.legal-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 0.75rem;
}

.legal-description {
  color: var(--color-gray-600);
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 1rem;
}

/* ======================
   OPEN SOURCE 
   ====================== */
.opensource-description {
  color: var(--color-gray-600);
  line-height: 1.6;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, var(--color-primary), #2563eb);
  color: var(--color-white);
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.2s ease;
  border: none;
  font-size: 0.95rem;
}

.cta-button:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.cta-button.primary {
  background: linear-gradient(135deg, var(--color-primary), #2563eb);
}

.button-icon {
  width: 1rem;
  height: 1rem;
}

/* ======================
   LIMITAÇÕES 
   ====================== */
.limitations-card {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.02), var(--color-white));
  border-color: rgba(245, 158, 11, 0.2);
}

.limitations-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.limitation-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--color-gray-50);
  border-radius: 0.5rem;
  border-left: 4px solid #f59e0b;
}

.limitation-label {
  font-weight: 600;
  color: var(--color-gray-900);
  font-size: 0.95rem;
}

.limitation-text {
  color: var(--color-gray-600);
  line-height: 1.5;
  font-size: 0.9rem;
}

/* ======================
   CTA FINAL 
   ====================== */
.cta-card {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.02), var(--color-white));
  border-color: rgba(34, 197, 94, 0.2);
}

.cta-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  text-align: center;
}

@media (min-width: 768px) {
  .cta-content {
    flex-direction: row;
    justify-content: space-between;
    text-align: left;
  }
}

.cta-text {
  flex: 1;
}

.cta-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 0.5rem;
}

.cta-description {
  color: var(--color-gray-600);
  margin: 0;
  font-size: 0.95rem;
}

/* ======================
   RESPONSIVIDADE 
   ====================== */
@media (max-width: 768px) {
  .step-item {
    flex-direction: column;
    gap: 1rem;
  }
  
  .step-number {
    align-self: flex-start;
  }
  
  .info-card-header,
  .info-card-content {
    padding: 1.5rem;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.75rem;
  }
  
  .info-card-header,
  .info-card-content {
    padding: 1rem;
  }
  
  .sources-grid,
  .legal-grid {
    gap: 1rem;
  }
  
  .source-item,
  .legal-item {
    padding: 1rem;
  }
}
</style>
