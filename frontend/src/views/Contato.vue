<template>
  <div class="min-h-screen bg-background">
    <AppHeader />
    
    <!-- Success State -->
    <div v-if="submitted" class="container mx-auto px-4 py-8 max-w-2xl">
      <div class="card border-primary">
        <div class="card-content pt-6">
          <div class="text-center space-y-4">
            <div class="flex justify-center">
              <div class="rounded-full bg-primary/10 p-3">
                <CheckCircle class="h-12 w-12 text-primary" />
              </div>
            </div>
            <div>
              <h2 class="text-2xl font-bold mb-2">Feedback Enviado com Sucesso!</h2>
              <p class="text-muted-foreground mb-4">Obrigado por contribuir para a transparência e melhoria da plataforma</p>
            </div>
            <div class="alert">
              <AlertCircle class="h-4 w-4" />
              <div class="alert-description">
                <strong>Número de Protocolo:</strong> {{ protocolo }}
                <br />
                <span class="text-sm">Guarde este número para acompanhar o status da sua solicitação</span>
              </div>
            </div>
            <div class="space-y-3 text-sm text-muted-foreground text-left bg-muted/50 p-4 rounded-lg">
              <p class="font-semibold text-foreground">Próximos passos:</p>
              <ol class="list-decimal list-inside space-y-2">
                <li>Nossa equipe revisará sua mensagem em até 48 horas úteis</li>
                <li>Se for uma correção de dados, verificaremos nas fontes oficiais</li>
                <li>Você receberá uma resposta no email fornecido</li>
                <li>Correções confirmadas serão aplicadas na próxima atualização</li>
              </ol>
            </div>
            <div class="flex gap-2 justify-center pt-4">
              <button @click="resetForm" class="btn btn-primary">
                <MessageSquare class="h-4 w-4 mr-2" />
                Enviar Outro Feedback
              </button>
              <RouterLink to="/" class="btn btn-outline">Voltar ao Início</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Form State -->
    <div v-else class="container mx-auto px-4 py-8 max-w-4xl">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold text-foreground mb-2">Feedback e Correções</h1>
        <p class="text-lg text-muted-foreground">Ajude-nos a manter a precisão e qualidade dos dados</p>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="card">
          <div class="card-header pb-3">
            <div class="flex items-center gap-2">
              <MessageSquare class="h-5 w-5 text-primary" />
              <h3 class="card-title text-base">Sugestões</h3>
            </div>
          </div>
          <div class="card-content">
            <p class="text-sm text-muted-foreground">
              Compartilhe ideias para novas funcionalidades ou melhorias na plataforma
            </p>
          </div>
        </div>

        <div class="card">
          <div class="card-header pb-3">
            <div class="flex items-center gap-2">
              <AlertCircle class="h-5 w-5 text-primary" />
              <h3 class="card-title text-base">Correções</h3>
            </div>
          </div>
          <div class="card-content">
            <p class="text-sm text-muted-foreground">
              Reporte dados incorretos ou inconsistências que você identificou
            </p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Form -->
        <div class="lg:col-span-2">
          <div class="card">
            <div class="card-header">
              <h3 class="card-title">Formulário de Contato</h3>
              <p class="card-description">
                Todos os campos são obrigatórios. Seu email será usado apenas para resposta.
              </p>
            </div>
            <div class="card-content">
              <form @submit.prevent="handleSubmit" class="space-y-6">
                <!-- Type -->
                <div class="space-y-2">
                  <label for="tipo" class="label">Tipo de Feedback</label>
                  <select 
                    id="tipo" 
                    v-model="formData.tipo" 
                    class="select"
                    required
                  >
                    <option value="">Selecione o tipo</option>
                    <option value="correcao">Correção de Dados</option>
                    <option value="sugestao">Sugestão de Melhoria</option>
                    <option value="duvida">Dúvida sobre Metodologia</option>
                    <option value="outro">Outro</option>
                  </select>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <!-- Name -->
                  <div class="space-y-2">
                    <label for="nome" class="label">Seu Nome</label>
                    <input
                      id="nome"
                      type="text"
                      placeholder="Nome completo"
                      v-model="formData.nome"
                      class="input"
                      required
                    />
                  </div>

                  <!-- Email -->
                  <div class="space-y-2">
                    <label for="email" class="label">Email</label>
                    <input
                      id="email"
                      type="email"
                      placeholder="seu@email.com"
                      v-model="formData.email"
                      class="input"
                      required
                    />
                  </div>
                </div>

                <!-- Parlamentar (optional for corrections) -->
                <div v-if="formData.tipo === 'correcao'" class="space-y-2">
                  <label for="parlamentar" class="label">Parlamentar (se aplicável)</label>
                  <input
                    id="parlamentar"
                    type="text"
                    placeholder="Nome do parlamentar relacionado"
                    v-model="formData.parlamentar"
                    class="input"
                  />
                </div>

                <!-- Message -->
                <div class="space-y-2">
                  <label for="mensagem" class="label">Mensagem</label>
                  <textarea
                    id="mensagem"
                    placeholder="Descreva detalhadamente sua solicitação..."
                    v-model="formData.mensagem"
                    rows="6"
                    class="textarea"
                    required
                  ></textarea>
                  <p class="text-xs text-muted-foreground">
                    Para correções, inclua links para as fontes oficiais quando possível
                  </p>
                </div>

                <!-- Privacy Notice -->
                <div class="alert">
                  <Mail class="h-4 w-4" />
                  <div class="alert-description text-xs">
                    <strong>Privacidade:</strong> Seus dados serão usados apenas para processar esta solicitação e não
                    serão compartilhados com terceiros. Conforme LGPD, você pode solicitar a exclusão dos seus dados a
                    qualquer momento.
                  </div>
                </div>

                <!-- Submit -->
                <button type="submit" class="btn btn-primary w-full" size="lg" :disabled="isSubmitting">
                  <span v-if="!isSubmitting" class="flex items-center justify-center gap-2">
                    <MessageSquare class="h-4 w-4" />
                    Enviar Feedback
                  </span>
                  <span v-else class="flex items-center justify-center gap-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Enviando...
                  </span>
                </button>
              </form>
            </div>
          </div>
        </div>
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Process Transparency -->
          <div class="card">
            <div class="card-header">
              <h3 class="card-title text-base">Processo de Revisão</h3>
            </div>
            <div class="card-content space-y-2 text-sm text-muted-foreground">
              <p>
                <strong class="text-foreground">Transparência:</strong> Todas as correções aplicadas são documentadas
                publicamente no nosso repositório GitHub com referência ao protocolo.
              </p>
              <p>
                <strong class="text-foreground">Tempo de resposta:</strong> Feedback é revisado em até 48 horas úteis.
                Correções confirmadas são aplicadas na próxima atualização diária.
              </p>
              <p>
                <strong class="text-foreground">Verificação:</strong> Correções de dados são verificadas diretamente
                nas fontes oficiais antes de serem aplicadas.
              </p>
            </div>
          </div>

          <!-- Alternative Contact -->
          <div class="card">
            <div class="card-content pt-6">
              <div class="text-center text-sm text-muted-foreground">
                <p class="mb-2">Prefere outro canal de contato?</p>
                <div class="flex justify-center gap-4">
                  <a href="mailto:contato@transparencia.gov.br" class="text-primary hover:underline">
                    Email direto
                  </a>
                  <span>•</span>
                  <RouterLink to="/metodologia" class="text-primary hover:underline">
                    Ver metodologia
                  </RouterLink>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { RouterLink } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import { CheckCircle, Mail, MessageSquare, AlertCircle } from 'lucide-vue-next'

// Reactive form data
const formData = reactive({
  tipo: '',
  nome: '',
  email: '',
  parlamentar: '',
  mensagem: ''
})

// State management
const submitted = ref(false)
const protocolo = ref('')
const isSubmitting = ref(false)

// Form submission handler with loading state
const handleSubmit = async () => {
  isSubmitting.value = true
  
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // Generate protocol number
  const protocolNumber = `TRANSP-${Date.now().toString().slice(-8)}`
  protocolo.value = protocolNumber
  submitted.value = true
  isSubmitting.value = false

  // Reset form data
  Object.assign(formData, {
    tipo: '',
    nome: '',
    email: '',
    parlamentar: '',
    mensagem: ''
  })
}

// Reset form to send another feedback
const resetForm = () => {
  submitted.value = false
  protocolo.value = ''
}

// Character limit for textarea
const messageLength = computed(() => formData.mensagem.length)

// Watch for tipo changes to add smooth transitions
watch(() => formData.tipo, (newVal) => {
  if (newVal === 'correcao') {
    // Add focus to parlamentar field after animation
    setTimeout(() => {
      const parlamentarField = document.getElementById('parlamentar')
      if (parlamentarField) {
        parlamentarField.focus()
      }
    }, 300)
  }
})
</script>

<style scoped>
/* Base Layout */
.min-h-screen {
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* Header Section */
.header-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  align-items: center;
  margin-bottom: 4rem;
  padding: 2rem 0;
}

.header-content {
  z-index: 10;
}

.header-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.badge-icon {
  width: 1rem;
  height: 1rem;
}

.header-title {
  font-size: 3.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #1e293b, #3b82f6);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  line-height: 1.1;
  margin-bottom: 1rem;
}

.header-subtitle {
  font-size: 1.25rem;
  color: #64748b;
  line-height: 1.6;
  max-width: 500px;
}

/* Header Visual */
.header-visual {
  position: relative;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-card {
  position: absolute;
  background: white;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.card-1 {
  top: 20px;
  right: 50px;
  animation: float 6s ease-in-out infinite;
}

.card-2 {
  bottom: 80px;
  left: 20px;
  animation: float 6s ease-in-out infinite 2s;
}

.card-3 {
  top: 120px;
  left: 120px;
  animation: float 6s ease-in-out infinite 4s;
}

.floating-icon {
  width: 2rem;
  height: 2rem;
  color: #3b82f6;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

/* Features Grid */
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.feature-card {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f1f5f9;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #3b82f6, #1d4ed8);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
}

.feature-icon-wrapper {
  width: 4rem;
  height: 4rem;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.feature-icon-wrapper.suggestions {
  background: linear-gradient(135deg, #dbeafe, #bfdbfe);
}

.feature-icon-wrapper.corrections {
  background: linear-gradient(135deg, #fef3c7, #fde68a);
}

.feature-icon {
  width: 2rem;
  height: 2rem;
  color: #3b82f6;
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.75rem;
}

.feature-description {
  color: #64748b;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.feature-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f8fafc;
  border-radius: 0.5rem;
  min-width: 80px;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3b82f6;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* Form Section */
.form-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  align-items: start;
}

.form-container {
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

.form-header {
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  padding: 2rem;
  border-bottom: 1px solid #e2e8f0;
}

.form-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 0.5rem;
}

.form-description {
  color: #64748b;
  line-height: 1.6;
}

.contact-form {
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.5rem;
}

.form-label.required::after {
  content: ' *';
  color: #ef4444;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 0.75rem;
  font-size: 0.875rem;
  background-color: white;
  transition: all 0.2s ease;
  font-family: inherit;
}

.form-input:focus, .form-textarea:focus, .form-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.form-textarea {
  resize: vertical;
  min-height: 120px;
  line-height: 1.6;
}

.select-wrapper {
  position: relative;
}

.form-select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

.form-help {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.textarea-counter {
  font-size: 0.75rem;
  color: #6b7280;
  text-align: right;
  margin-top: 0.25rem;
}

.conditional-field {
  animation: slideDown 0.3s ease;
  overflow: hidden;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    max-height: 200px;
    transform: translateY(0);
  }
}

/* Privacy Notice */
.privacy-notice {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  margin-bottom: 2rem;
}

.privacy-icon {
  flex-shrink: 0;
  width: 2.5rem;
  height: 2.5rem;
  background: #dbeafe;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.privacy-icon .icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #3b82f6;
}

.privacy-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.privacy-text {
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.5;
}

/* Submit Button */
.submit-button {
  width: 100%;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-content, .submit-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.loading-spinner {
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Info Sidebar */
.info-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.info-card, .stats-card, .contact-card {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #f1f5f9;
  overflow: hidden;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  border-bottom: 1px solid #e2e8f0;
}

.info-icon-wrapper {
  width: 2.5rem;
  height: 2.5rem;
  background: #dbeafe;
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #3b82f6;
}

.info-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
}

.info-content {
  padding: 1.5rem;
}

.info-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  margin-bottom: 1.5rem;
}

.info-item:last-child {
  margin-bottom: 0;
}

.info-step {
  width: 2rem;
  height: 2rem;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}

.info-item h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.info-item p {
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.4;
}

/* Stats Card */
.stats-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: #e2e8f0;
}

.stat-box {
  background: white;
  padding: 1rem;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  font-weight: 500;
}

/* Contact Card */
.contact-title {
  font-size: 1rem;
  font-weight: 600;
  color: #1e293b;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
}

.contact-options {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.contact-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  color: #3b82f6;
  text-decoration: none;
  transition: all 0.2s ease;
  border: 1px solid #e2e8f0;
}

.contact-option:hover {
  background: #f8fafc;
  transform: translateX(5px);
}

.contact-icon {
  width: 1rem;
  height: 1rem;
}

/* Success State */
.success-animation {
  animation: fadeInUp 0.6s ease;
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

.success-card {
  background: white;
  border-radius: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid #f1f5f9;
  overflow: hidden;
  text-align: center;
  padding: 3rem;
}

.success-icon-container {
  position: relative;
  display: inline-block;
  margin-bottom: 2rem;
}

.success-pulse {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100px;
  height: 100px;
  background: rgba(34, 197, 94, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(0.8);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(1.4);
    opacity: 0;
  }
}

.success-icon-wrapper {
  position: relative;
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.success-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: #22c55e;
}

.success-title {
  font-size: 2rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 1rem;
}

.success-subtitle {
  font-size: 1.125rem;
  color: #64748b;
  margin-bottom: 2rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.protocol-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.protocol-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.protocol-icon {
  width: 1rem;
  height: 1rem;
  color: #3b82f6;
}

.protocol-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #64748b;
}

.protocol-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: #3b82f6;
  font-family: 'Courier New', monospace;
  margin-bottom: 0.5rem;
}

.protocol-note {
  font-size: 0.75rem;
  color: #6b7280;
  line-height: 1.4;
}

.steps-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  text-align: left;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.steps-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 1.5rem;
  text-align: center;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.step-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.step-number {
  width: 2rem;
  height: 2rem;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  flex-shrink: 0;
}

.step-content h4 {
  font-size: 0.875rem;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 0.25rem;
}

.step-content p {
  font-size: 0.75rem;
  color: #64748b;
  line-height: 1.4;
}

.success-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
}

.btn-secondary {
  background: white;
  color: #3b82f6;
  border: 1px solid #3b82f6;
}

.btn-secondary:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-2px);
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1rem;
}

.btn-icon {
  width: 1rem;
  height: 1rem;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .header-section,
  .form-section {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .header-visual {
    height: 200px;
  }
  
  .header-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 0.75rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .success-actions {
    flex-direction: column;
  }
  
  .header-title {
    font-size: 2rem;
  }
  
  .header-subtitle {
    font-size: 1rem;
  }
}

@media (max-width: 640px) {
  .form-container,
  .success-card {
    margin: 0 -0.75rem;
    border-radius: 0;
  }
  
  .contact-form,
  .success-card {
    padding: 1.5rem;
  }
}
</style>
