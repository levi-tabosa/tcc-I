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
              <h2 class="text-2xl font-bold mb-2">Feedback Recebido!</h2>
              <p class="text-muted-foreground mb-4">Obrigado por contribuir para a melhoria da plataforma</p>
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
              <button @click="resetForm" class="btn btn-primary">Enviar Outro Feedback</button>
              <RouterLink to="/" class="btn btn-outline">Voltar ao Início</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Form State -->
    <div v-else class="container mx-auto px-4 py-8 max-w-2xl">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-foreground mb-2">Feedback e Correções</h1>
        <p class="text-lg text-muted-foreground">Ajude-nos a manter a precisão e qualidade dos dados</p>
      </div>

      <!-- Info Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
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

      <!-- Form -->
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
              <p class="text-xs text-muted-foreground">Usado apenas para responder sua solicitação</p>
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
            <button type="submit" class="btn btn-primary w-full" size="lg">
              Enviar Feedback
            </button>
          </form>
        </div>
      </div>

      <!-- Process Transparency -->
      <div class="card mt-6">
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
      <div class="card mt-6">
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
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
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

// Form submission handler
const handleSubmit = () => {
  // Generate protocol number
  const protocolNumber = `TRANSP-${Date.now().toString().slice(-8)}`
  protocolo.value = protocolNumber
  submitted.value = true

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
/* Form Styles */
.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-gray-700);
  margin-bottom: 0.5rem;
}

.input, .textarea, .select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-gray-300);
  border-radius: 0.5rem;
  font-size: 0.875rem;
  background-color: var(--color-white);
  transition: border-color 0.2s ease;
}

.input:focus, .textarea:focus, .select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.textarea {
  resize: vertical;
  min-height: 6rem;
}

.alert {
  display: flex;
  gap: 0.75rem;
  padding: 1rem;
  border: 1px solid var(--color-gray-200);
  border-radius: 0.5rem;
  background-color: var(--color-gray-50);
}

.alert-description {
  flex: 1;
  color: var(--color-gray-700);
  line-height: 1.5;
}

.space-y-2 > * + * {
  margin-top: 0.5rem;
}

.space-y-3 > * + * {
  margin-top: 0.75rem;
}

.space-y-4 > * + * {
  margin-top: 1rem;
}

.space-y-6 > * + * {
  margin-top: 1.5rem;
}

/* Responsive */
@media (min-width: 768px) {
  .grid-cols-1.md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Utilities */
.bg-muted\/50 {
  background-color: rgba(0, 0, 0, 0.05);
}

.text-muted-foreground {
  color: var(--color-gray-600);
}

.text-foreground {
  color: var(--color-gray-900);
}

.text-primary {
  color: var(--color-primary);
}

.border-primary {
  border-color: var(--color-primary);
}

.bg-primary\/10 {
  background-color: rgba(59, 130, 246, 0.1);
}
</style>
