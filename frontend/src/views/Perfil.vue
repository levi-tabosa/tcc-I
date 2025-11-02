<template>
  <div class="page-container">
    <AppHeader />
    
    <div v-if="isLoading" class="feedback-container loading-container">
      <div class="loading-spinner"></div>
      <p class="loading-text">Carregando dados do parlamentar...</p>
    </div>

    <div v-else-if="error" class="feedback-container error-container">
      <div class="error-icon">
        <span>❌</span>
      </div>
      <h2>Oops! Algo deu errado</h2>
      <p class="error-message">{{ error }}</p>
      <router-link to="/" class="back-button">
        Voltar ao Início
      </router-link>
    </div>

    <div v-else-if="deputado" class="perfil-container animate-fade-in">
      <div class="perfil-card">
        <header class="perfil-header">
          <div class="header-background"></div>
          <div class="header-content">
            <div class="perfil-avatar">
              <span class="avatar-placeholder">{{ deputado.nome_civil.charAt(0) }}</span>
            </div>
            <div class="perfil-info">
              <h1 class="deputado-nome">{{ deputado.nome_civil }}</h1>
              <p class="deputado-cargo">Deputado Federal</p>
              <div class="deputado-detalhes">
                <span class="badge">{{ deputado.uf_nascimento }}</span>
              </div>
            </div>
          </div>
        </header>

        <div class="perfil-body">
          <section class="info-section">
            <h2>Informações Pessoais</h2>
            <div class="info-grid">
              <div class="info-item" v-if="deputado.data_nascimento">
                <strong>Data de Nascimento:</strong>
                <span>{{ formatarData(deputado.data_nascimento) }}</span>
              </div>
              <div class="info-item" v-if="deputado.escolaridade">
                <strong>Escolaridade:</strong>
                <span>{{ deputado.escolaridade }}</span>
              </div>
              <div class="info-item" v-if="deputado.email">
                <strong>Email:</strong>
                <span>{{ deputado.email }}</span>
              </div>
              <div class="info-item" v-if="deputado.municipio_nascimento">
                <strong>Cidade de Nascimento:</strong>
                <span>{{ deputado.municipio_nascimento }}, {{ deputado.uf_nascimento }}</span>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  </div>
</template>
          <div class="header-background"></div>
          <div class="header-content">
            <div class="avatar-container">
              <div class="avatar-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="avatar-icon">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
              </div>
              <div class="status-badge">
                <span class="status-dot"></span>
                Ativo
              </div>
            </div>
            
            <div class="perfil-info">
              <h1 class="perfil-nome">{{ deputado.nome_civil }}</h1>
              <p class="perfil-origem">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                  <circle cx="12" cy="10" r="3"/>
                </svg>
                Natural de {{ deputado.municipio_nascimento }} - {{ deputado.uf_nascimento }}
              </p>
            </div>
          </div>
        </header>

        <!-- Conteúdo Principal -->
        <main class="perfil-content">
          <!-- Seção de Informações Pessoais -->
          <section class="info-section">
            <div class="section-header">
              <h3 class="section-title">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                  <circle cx="9" cy="7" r="4"/>
                  <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                  <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
                </svg>
                Informações Pessoais
              </h3>
            </div>
            
            <div class="info-grid">
              <div class="info-item">
                <div class="info-label">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/>
                    <rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>
                  </svg>
                  ID Câmara
                </div>
                <div class="info-value">{{ deputado.id }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                    <polyline points="22,6 12,13 2,6"/>
                  </svg>
                  Email de Contato
                </div>
                <div class="info-value">{{ deputado.email || 'Não informado' }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                    <line x1="16" y1="2" x2="16" y2="6"/>
                    <line x1="8" y1="2" x2="8" y2="6"/>
                    <line x1="3" y1="10" x2="21" y2="10"/>
                  </svg>
                  Data de Nascimento
                </div>
                <div class="info-value">{{ formatarData(deputado.data_nascimento) }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M2 3h6l1 9h9l1-9h2"/>
                    <path d="M9 21v-6a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v6"/>
                    <path d="M9 21h6"/>
                  </svg>
                  Escolaridade
                </div>
                <div class="info-value">{{ deputado.escolaridade || 'Não informada' }}</div>
              </div>

              <div class="info-item">
                <div class="info-label">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                  Município de Nascimento
                </div>
                <div class="info-value">          </section>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'

interface Deputado {
  id: number;
  nome_civil: string;
  email: string | null;
  data_nascimento: string | null;
  escolaridade: string | null;
  uf_nascimento: string;
  municipio_nascimento: string;
}

const route = useRoute()
const isLoading = ref(true)
const error = ref<string | null>(null)
const deputado = ref<Deputado | null>(null)

const formatarData = (dataString: string) => {
  const data = new Date(dataString)
  return data.toLocaleDateString('pt-BR')
}

const carregarDeputado = async () => {
  const deputadoId = route.params.id
  if (!deputadoId) {
    error.value = 'ID do deputado não fornecido'
    isLoading.value = false
    return
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/deputados/${deputadoId}`)
    
    if (response.status === 404) {
      error.value = 'Deputado não encontrado. Verifique se o ID está correto.'
      return
    }
    
    if (!response.ok) {
      throw new Error('Falha ao carregar dados do deputado')
    }
    
    const dados = await response.json()
    deputado.value = dados
  } catch (err: any) {
    console.error('Erro ao carregar deputado:', err)
    error.value = err.message || 'Erro inesperado ao carregar dados'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  carregarDeputado()
})
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #f8fafc, #f1f5f9);
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--color-gray-900);
}

.feedback-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  text-align: center;
  padding: 2rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  color: var(--color-gray-600);
  font-size: 1.1rem;
}

.error-container h2 {
  color: var(--color-gray-900);
  margin: 1rem 0 0.5rem 0;
  font-size: 1.5rem;
}

.error-message {
  color: var(--color-gray-600);
  margin-bottom: 1.5rem;
}

.back-button {
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: var(--color-primary-dark);
}

.perfil-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.perfil-card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.perfil-header {
  position: relative;
  background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
  padding: 2rem;
  color: white;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.perfil-avatar {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  color: white;
}

.deputado-nome {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 0 0 0.25rem 0;
}

.deputado-cargo {
  font-size: 1rem;
  opacity: 0.9;
  margin: 0 0 0.5rem 0;
}

.badge {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
}

.perfil-body {
  padding: 2rem;
}

.info-section h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-gray-900);
  margin-bottom: 1rem;
}

.info-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
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

.info-item strong {
  display: block;
  color: var(--color-gray-700);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.info-item span {
  color: var(--color-gray-900);
  font-weight: 500;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style></div>
              </div>
            </div>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'

// --- Interface de dados ajustada para o seu banco de dados ---
interface Deputado {
  id: number;
  nome_civil: string;
  email: string | null;
  data_nascimento: string | null;
  escolaridade: string | null;
  uf_nascimento: string;
  municipio_nascimento: string;
}

// --- Variáveis Reativas ---
const route = useRoute();
const deputado = ref<Deputado | null>(null);
const isLoading = ref(true);
const error = ref<string | null>(null);

// --- Funções Auxiliares ---
const formatarData = (dataIso: string | null): string => {
  if (!dataIso) return 'Não informada';
  const data = new Date(dataIso);
  return data.toLocaleDateString('pt-BR', { timeZone: 'UTC' });
};

// --- Lógica Principal ---
onMounted(async () => {
  const deputadoId = route.params.id;

  if (!deputadoId) {
    error.value = "ID do parlamentar não foi encontrado na URL.";
    isLoading.value = false;
    return;
  }

  try {
    const response = await fetch(`http://127.0.0.1:8000/api/deputados/${deputadoId}`);
    
    if (response.status === 404) {
      throw new Error(`Nenhum parlamentar foi encontrado com o ID ${deputadoId}.`);
    }
    if (!response.ok) {
      throw new Error('Falha na comunicação com o servidor. Por favor, tente novamente mais tarde.');
    }
    
    deputado.value = await response.json();

  } catch (err: any) {
    console.error("Erro ao buscar dados do perfil:", err);
    error.value = err.message;
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
/* ======================
   TEMA ESCURO - PERFIL
   ====================== */

.page-container {
  min-height: 100vh;
  background: linear-gradient(180deg, #0f172a, #1e293b);
  color: #e2e8f0;
  padding: 1rem 0.75rem 2rem;
}

@media (min-width: 640px) {
  .page-container {
    padding: 1.5rem 1rem 3rem;
  }
}

@media (min-width: 768px) {
  .page-container {
    padding: 2rem 1rem 4rem;
  }
}

/* ======================
   FEEDBACK CONTAINERS
   ====================== */
   FEEDBACK E LOADING
   ====================== */
.feedback-container {
  max-width: 500px;
  margin: 4rem auto;
  text-align: center;
  padding: 3rem;
  border-radius: 1.5rem;
  background: linear-gradient(135deg, #1e293b, #334155);
  border: 1px solid #475569;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
}

.loading-container {
  border: 1px solid #60a5fa;
}

.loading-spinner {
  width: 3rem;
  height: 3rem;
  border: 3px solid #334155;
  border-top: 3px solid #60a5fa;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1.1rem;
  color: #94a3b8;
  margin: 0;
}

.error-container {
  border: 1px solid #ef4444;
  background: linear-gradient(135deg, #7f1d1d, #1e293b);
}

.error-icon {
  margin: 0 auto 1.5rem;
  color: #f87171;
}

.error-container h2 {
  font-size: 1.5rem;
  color: #f87171;
  margin: 0 0 1rem;
  font-weight: 700;
}

.error-message {
  color: #fca5a5;
  margin: 0 0 2rem;
  line-height: 1.6;
}

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 2rem;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  color: white;
  text-decoration: none;
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.back-button:hover {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  transform: translateY(-1px);
}

/* ======================
   CONTAINER PRINCIPAL
   ====================== */
.perfil-container {
  max-width: 1000px;
  margin: 0 auto;
}

.perfil-card {
  background: linear-gradient(135deg, #1e293b, #334155);
  border: 1px solid #475569;
  border-radius: 2rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

/* ======================
   HEADER DO PERFIL
   ====================== */
.perfil-header {
  position: relative;
  padding: 3rem 2rem 2rem;
  background: linear-gradient(135deg, #0f172a, #1e293b);
}

.header-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: radial-gradient(circle at 70% 30%, rgba(96, 165, 250, 0.2), transparent 50%);
}

.header-content {
  position: relative;
  display: flex;
  align-items: center;
  gap: 2rem;
}

@media (max-width: 640px) {
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar-wrapper {
  width: 5rem;
  height: 5rem;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #1e293b;
  box-shadow: 0 8px 25px rgba(96, 165, 250, 0.3);
}

.avatar-icon {
  color: white;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.875rem;
  background: linear-gradient(135deg, #064e3b, #065f46);
  color: #34d399;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 50px;
  border: 1px solid #059669;
}

.status-dot {
  width: 0.5rem;
  height: 0.5rem;
  background-color: #34d399;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.perfil-info {
  flex: 1;
}

.perfil-nome {
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: 800;
  color: #f1f5f9;
  margin: 0 0 0.75rem;
  line-height: 1.2;
}

.perfil-origem {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  color: #94a3b8;
  margin: 0;
  font-weight: 500;
}

@media (max-width: 640px) {
  .perfil-origem {
    justify-content: center;
  }
}

/* ======================
   CONTEÚDO PRINCIPAL
   ====================== */
.perfil-content {
  padding: 2rem;
}

.info-section {
  margin-bottom: 2rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #f1f5f9;
  margin: 0;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid #60a5fa;
}

/* ======================
   GRID DE INFORMAÇÕES
   ====================== */
.info-grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: 1fr;
}

@media (min-width: 640px) {
  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.info-item {
  background: linear-gradient(135deg, #334155, #1e293b);
  padding: 1.5rem;
  border-radius: 1rem;
  border: 1px solid #475569;
  transition: all 0.2s ease;
}

.info-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
  border-color: #60a5fa;
}

.info-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  color: #94a3b8;
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.info-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #f1f5f9;
  line-height: 1.4;
  word-break: break-word;
}

/* ======================
   ANIMAÇÕES
   ====================== */
.animate-fade-in {
  animation: fadeInUp 0.6s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* ======================
   MELHORIAS MOBILE
   ====================== */
/* Melhor experiência touch */
.perfil-card, .info-item, .nav-back-button {
  -webkit-tap-highlight-color: rgba(96, 165, 250, 0.2);
}

/* Smooth scroll para links âncora */
html {
  scroll-behavior: smooth;
}

/* ======================
   RESPONSIVIDADE OTIMIZADA
   ====================== */
@media (max-width: 768px) {
  .perfil-header {
    padding: 1.5rem 1rem 1rem;
  }
  
  .perfil-content {
    padding: 1.25rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .info-item {
    padding: 1rem;
  }
  
  .perfil-nome {
    font-size: 1.75rem;
  }
}

@media (max-width: 480px) {
  .perfil-header {
    padding: 1.25rem 0.75rem 0.75rem;
  }
  
  .perfil-content {
    padding: 1rem 0.75rem;
  }
  
  .perfil-nome {
    font-size: 1.5rem;
  }
  
  .perfil-origem {
    font-size: 1rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .info-item {
    padding: 0.875rem;
  }
  
  .info-value {
    font-size: 1rem;
  }
}
</style>