<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-50 to-white">
    
    <!-- Success State -->
    <div v-if="submitted" class="container mx-auto px-4 py-8 max-w-2xl">
      <div class="card border-primary">
        <div class="card-content pt-6">
          <div class="text-center space-y-4">
            <div class="flex justify-center">
              <div class="rounded-full bg-blue-50 p-4">
                <CheckCircle class="h-12 w-12 text-primary" />
              </div>
            </div>
            <div>
              <h2 class="text-2xl font-bold mb-2 text-slate-900">Feedback Enviado com Sucesso!</h2>
              <p class="text-slate-600 mb-4">Obrigado por contribuir para a transparência e melhoria da plataforma</p>
            </div>
            <div class="alert">
              <AlertCircle class="h-4 w-4 text-primary" />
              <div class="alert-description">
                <strong>Número de Protocolo:</strong> {{ protocolo }}
                <br />
                <span class="text-sm">Guarde este número para acompanhar o status da sua solicitação</span>
              </div>
            </div>
            <div class="space-y-3 text-sm text-slate-600 text-left bg-slate-100 p-4 rounded-lg">
              <p class="font-semibold text-slate-900">Próximos passos:</p>
              <ol class="list-decimal list-inside space-y-2">
                <li>Nossa equipe revisará sua mensagem em até 48 horas úteis</li>
                <li>Se for uma correção de dados, verificaremos nas fontes oficiais</li>
                <li>Você receberá uma resposta no email fornecido</li>
                <li>Correções confirmadas serão aplicadas na próxima atualização</li>
              </ol>
            </div>
            <div class="flex gap-3 justify-center pt-4">
              <button @click="resetForm" class="btn btn-primary">
                <MessageSquare class="h-4 w-4 mr-2" />
                Enviar Outro Feedback
              </button>
              <RouterLink to="/" class="btn btn-secondary">Voltar ao Início</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Form State -->
    <div v-else class="container mx-auto px-4 py-8 max-w-4xl">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold text-slate-900 mb-2">Feedback e Correções</h1>
        <p class="text-lg text-slate-600">Ajude-nos a manter a precisão e qualidade dos dados</p>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div class="card">
          <div class="card-header pb-3">
            <div class="flex items-center gap-2">
              <div class="p-2 bg-blue-50 rounded-lg">
                <MessageSquare class="h-5 w-5 text-primary" />
              </div>
              <h3 class="card-title text-base text-slate-900">Sugestões</h3>
            </div>
          </div>
          <div class="card-content">
            <p class="text-sm text-slate-600">
              Compartilhe ideias para novas funcionalidades ou melhorias na plataforma
            </p>
          </div>
        </div>

        <div class="card">
          <div class="card-header pb-3">
            <div class="flex items-center gap-2">
              <div class="p-2 bg-blue-50 rounded-lg">
                <AlertCircle class="h-5 w-5 text-primary" />
              </div>
              <h3 class="card-title text-base text-slate-900">Correções</h3>
            </div>
          </div>
          <div class="card-content">
            <p class="text-sm text-slate-600">
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
              <h3 class="card-title text-slate-900">Formulário de Contato</h3>
              <p class="card-description text-slate-600">
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
                    class="input"
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
                <div v-if="formData.tipo === 'correcao'" class="space-y-2 fade-in">
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
                    :maxlength="maxMessageLength"
                    class="input"
                    required
                    aria-describedby="mensagem-help mensagem-counter"
                  ></textarea>
                  <div class="flex justify-between">
                    <p id="mensagem-help" class="text-xs text-slate-500">
                      Para correções, inclua links para as fontes oficiais quando possível
                    </p>
                    <div id="mensagem-counter" class="text-xs text-slate-500">
                      {{ messageLength }} / {{ maxMessageLength }}
                    </div>
                  </div>
                </div>

                <!-- Privacy Notice -->
                <div class="alert bg-blue-50 border-blue-200" role="status" aria-live="polite">
                  <Mail class="h-4 w-4 text-primary" />
                  <div class="alert-description text-xs text-slate-700">
                    <strong>Privacidade:</strong> Seus dados serão usados apenas para processar esta solicitação e não
                    serão compartilhados com terceiros. Conforme LGPD, você pode solicitar a exclusão dos seus dados a
                    qualquer momento.
                  </div>
                </div>

                <!-- Submit -->
                <button type="submit" class="btn btn-primary w-full btn-lg" :disabled="isSubmitting">
                  <span v-if="!isSubmitting" class="flex items-center justify-center gap-2">
                    <MessageSquare class="h-4 w-4" />
                    Enviar Feedback
                  </span>
                  <span v-else class="flex items-center justify-center gap-2">
                    <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white" aria-hidden="true"></div>
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
              <h3 class="card-title text-base text-slate-900">Processo de Revisão</h3>
            </div>
            <div class="card-content space-y-3 text-sm text-slate-600">
              <div class="flex items-start gap-3">
                <div class="w-6 h-6 bg-blue-50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-xs font-semibold text-primary">1</span>
                </div>
                <div>
                  <p class="font-semibold text-slate-900">Transparência</p>
                  <p>Todas as correções aplicadas são documentadas publicamente no nosso repositório GitHub.</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <div class="w-6 h-6 bg-blue-50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-xs font-semibold text-primary">2</span>
                </div>
                <div>
                  <p class="font-semibold text-slate-900">Tempo de resposta</p>
                  <p>Feedback é revisado em até 48 horas úteis. Correções confirmadas são aplicadas na próxima atualização.</p>
                </div>
              </div>
              <div class="flex items-start gap-3">
                <div class="w-6 h-6 bg-blue-50 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5">
                  <span class="text-xs font-semibold text-primary">3</span>
                </div>
                <div>
                  <p class="font-semibold text-slate-900">Verificação</p>
                  <p>Correções de dados são verificadas diretamente nas fontes oficiais antes de serem aplicadas.</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Alternative Contact -->
          <div class="card">
            <div class="card-content pt-6">
              <div class="text-center text-sm text-slate-600">
                <p class="mb-3 font-medium text-slate-700">Prefere outro canal de contato?</p>
                <div class="space-y-2">
                  <a href="mailto:contato@transparencia.gov.br" class="flex items-center justify-center gap-2 p-2 rounded-lg hover:bg-slate-50 text-primary transition-colors">
                    <Mail class="h-4 w-4" />
                    Email direto
                  </a>
                  <RouterLink to="/metodologia" class="flex items-center justify-center gap-2 p-2 rounded-lg hover:bg-slate-50 text-primary transition-colors">
                    <AlertCircle class="h-4 w-4" />
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
import { ref, reactive } from 'vue'
import { RouterLink } from 'vue-router'
import { CheckCircle, Mail, MessageSquare, AlertCircle } from 'lucide-vue-next'
import { computed } from 'vue'

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
const maxMessageLength = 1000

const messageLength = computed(() => formData.mensagem ? formData.mensagem.length : 0)

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
</script>

<style scoped>
/* Use das CSS Custom Properties do projeto */
.card {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: var(--shadow-lg);
}

.card-content {
  padding: var(--space-6);
}

.card-header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-gray-200);
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0;
}

.card-description {
  font-size: var(--font-size-sm);
  color: var(--color-gray-600);
  margin: var(--space-2) 0 0 0;
}

/* Labels e Form Elements seguindo o padrão */
.label {
  display: block;
  font-size: var(--font-size-sm);
  font-weight: 600;
  color: var(--color-gray-700);
  margin-bottom: var(--space-2);
}

.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border: 1px solid var(--color-gray-300);
  border-radius: var(--radius-md);
  font-size: var(--font-size-sm);
  background-color: var(--color-white);
  transition: all 0.2s ease;
  color: var(--color-gray-900);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.input::placeholder {
  color: var(--color-gray-400);
}

/* Alert usando o padrão do projeto */
.alert {
  display: flex;
  gap: var(--space-3);
  padding: var(--space-4);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radius-lg);
  background-color: var(--color-gray-50);
}

.alert-description {
  flex: 1;
  color: var(--color-gray-700);
  line-height: 1.5;
}

/* Botões seguindo exatamente o padrão do projeto */
.btn {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s ease;
  cursor: pointer;
  border: none;
  font-size: var(--font-size-base);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

.btn-lg {
  padding: var(--space-4) var(--space-8);
  font-size: var(--font-size-lg);
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-white);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background-color: var(--color-white);
  color: var(--color-gray-700);
  border: 1px solid var(--color-gray-300);
}

.btn-secondary:hover {
  background-color: var(--color-gray-50);
  border-color: var(--color-gray-400);
}

/* Cores usando as variáveis do projeto */
.text-primary {
  color: var(--color-primary);
}

.text-slate-900 {
  color: var(--color-gray-900);
}

.text-slate-700 {
  color: var(--color-gray-700);
}

.text-slate-600 {
  color: var(--color-gray-600);
}

.text-slate-500 {
  color: var(--color-gray-500);
}

.bg-blue-50 {
  background-color: rgba(37, 99, 235, 0.05);
}

.bg-slate-100 {
  background-color: var(--color-gray-100);
}

.border-blue-200 {
  border-color: rgba(37, 99, 235, 0.2);
}

.border-primary {
  border-color: var(--color-primary);
}

/* Animações e transições */
.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.transition-colors {
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Spinner para loading */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Spacing utilities usando as variáveis do projeto */
.space-y-2 > * + * {
  margin-top: var(--space-2);
}

.space-y-3 > * + * {
  margin-top: var(--space-3);
}

.space-y-4 > * + * {
  margin-top: var(--space-4);
}

.space-y-6 > * + * {
  margin-top: var(--space-6);
}

/* Utility classes seguindo o padrão */
.w-full { width: 100%; }
.w-4 { width: var(--space-4); }
.w-5 { width: 1.25rem; }
.w-6 { width: var(--space-6); }
.h-4 { height: var(--space-4); }
.h-5 { height: 1.25rem; }
.h-6 { height: var(--space-6); }
.h-12 { height: var(--space-12); }

.flex { display: flex; }
.grid { display: grid; }
.items-center { align-items: center; }
.items-start { align-items: flex-start; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }

.gap-2 { gap: var(--space-2); }
.gap-3 { gap: var(--space-3); }
.gap-6 { gap: var(--space-6); }

.mb-2 { margin-bottom: var(--space-2); }
.mb-3 { margin-bottom: var(--space-3); }
.mb-4 { margin-bottom: var(--space-4); }
.mb-8 { margin-bottom: var(--space-8); }
.mr-2 { margin-right: var(--space-2); }
.mt-0\.5 { margin-top: 0.125rem; }

.p-2 { padding: var(--space-2); }
.p-4 { padding: var(--space-4); }
.pt-4 { padding-top: var(--space-4); }
.pt-6 { padding-top: var(--space-6); }
.pb-3 { padding-bottom: var(--space-3); }

.text-center { text-align: center; }
.text-right { text-align: right; }

.text-xs { font-size: var(--font-size-xs); }
.text-sm { font-size: var(--font-size-sm); }
.text-base { font-size: var(--font-size-base); }
.text-lg { font-size: var(--font-size-lg); }
.text-2xl { font-size: var(--font-size-2xl); }
.text-4xl { font-size: var(--font-size-4xl); }

.font-bold { font-weight: 700; }
.font-semibold { font-weight: 600; }
.font-medium { font-weight: 500; }

.rounded-lg { border-radius: var(--radius-lg); }
.rounded-full { border-radius: var(--radius-full); }

.border-b-2 { border-bottom-width: 2px; }
.border-white { border-color: var(--color-white); }

.flex-shrink-0 { flex-shrink: 0; }

/* Grid responsivo */
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }

@media (min-width: 768px) {
  .md\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}

@media (min-width: 1024px) {
  .lg\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  .lg\:col-span-2 { grid-column: span 2 / span 2; }
}

/* Container responsivo seguindo o padrão */
.container {
  width: 100%;
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-4);
  padding-right: var(--space-4);
}

@media (min-width: 640px) {
  .container { max-width: var(--container-sm); }
}
@media (min-width: 768px) {
  .container { max-width: var(--container-md); }
}
@media (min-width: 1024px) {
  .container { max-width: var(--container-lg); }
}
@media (min-width: 1280px) {
  .container { max-width: var(--container-xl); }
}

.max-w-2xl { max-width: 42rem; }
.max-w-4xl { max-width: 56rem; }
.min-h-screen { min-height: 100vh; }
.mx-auto { margin-left: auto; margin-right: auto; }
.px-4 { padding-left: var(--space-4); padding-right: var(--space-4); }
.py-8 { padding-top: var(--space-8); padding-bottom: var(--space-8); }

/* List styles */
.list-decimal { list-style-type: decimal; }
.list-inside { list-style-position: inside; }

/* Hover effects consistentes com o projeto */
.hover\:bg-slate-50:hover {
  background-color: var(--color-gray-50);
}
</style>
