<template>
  <div class="min-h-screen bg-gradient-to-b from-slate-50 to-white">
    <!-- Header -->
    <header class="sticky top-0 z-50 backdrop-blur-md bg-white/80 border-b border-slate-200">
      <div class="max-w-6xl mx-auto px-4 py-4">
        <nav class="flex items-center justify-center md:justify-between">
          <div class="flex items-center gap-2">
            <Shield class="w-8 h-8 text-blue-600" />
            <span class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              Fiscaliza Brasil
            </span>
          </div>
          <div class="hidden md:flex gap-6">
            <a href="#inicio" class="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Início
            </a>
            <a href="#funcionalidades" class="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Funcionalidades
            </a>
            <a href="#como-usar" class="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Como Usar
            </a>
            <a href="#sobre" class="text-slate-600 hover:text-blue-600 transition-colors font-medium">
              Sobre
            </a>
          </div>
        </nav>
      </div>
    </header>

    <main class="container-center">
      <!-- Hero Section - Melhorado -->
      <section id="inicio" class="relative overflow-hidden w-full">
        <!-- Background decorativo -->
        <div class="absolute inset-0 bg-gradient-to-br from-blue-50 via-white to-slate-50 opacity-70"></div>
        <div class="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-blue-100/30 to-transparent"></div>
        
        <div class="relative max-w-4xl mx-auto px-4 py-20 lg:py-32 text-center">
          <div class="flex justify-center mb-6">
            <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 text-blue-700 text-sm font-semibold">
              <Eye class="w-4 h-4" />
              Transparência · Dados Públicos · Cidadania
            </div>
          </div>
          
          <h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold text-slate-900 mb-6 leading-tight">
            Fiscalize seus
            <span class="block bg-gradient-to-r from-blue-600 to-blue-800 bg-clip-text text-transparent">
              representantes
            </span>
            com clareza
          </h1>
          
          <p class="text-lg md:text-xl text-slate-600 mb-8 leading-relaxed max-w-3xl mx-auto">
            Transformamos dados complexos do Congresso em informações claras e acessíveis. 
            Fiscalização parlamentar não precisa de expertise técnica – é direito de todos.
          </p>

          <!-- Search Bar Melhorada -->
          <div class="max-w-2xl mx-auto mb-6">
            <form @submit="handleSearch" class="flex flex-col sm:flex-row gap-3">
              <div class="relative flex-1">
                <Search class="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input 
                  v-model="searchQuery"
                  type="text"
                  placeholder="Busque por parlamentar, partido ou proposição..."
                  class="w-full h-14 pl-12 pr-4 rounded-xl border-2 border-slate-200 focus:border-blue-500 focus:outline-none text-slate-900 placeholder-slate-400"
                />
              </div>
              <button 
                type="submit"
                class="h-14 px-8 bg-gradient-to-r from-blue-600 to-blue-700 text-white font-semibold rounded-xl hover:from-blue-700 hover:to-blue-800 transition-all shadow-lg hover:shadow-xl whitespace-nowrap"
              >
                Buscar
              </button>
            </form>
          </div>
          
          <div class="flex flex-col sm:flex-row items-center justify-center gap-4 text-sm text-slate-500 mb-12">
            <div class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-green-600" />
              <span>Dados oficiais em tempo real</span>
            </div>
            <div class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-green-600" />
              <span>100% gratuito</span>
            </div>
          </div>

          <!-- Stats Preview -->
          <div class="max-w-2xl mx-auto">
            <div class="grid grid-cols-2 gap-4">
              <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-slate-100">
                <Users class="w-6 md:w-8 h-6 md:h-8 text-blue-600 mb-3 mx-auto" />
                <div class="text-2xl md:text-4xl font-bold text-slate-900 mb-1 text-center">594</div>
                <div class="text-xs md:text-sm text-slate-600 text-center">Parlamentares monitorados</div>
              </div>
              <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-slate-100">
                <TrendingUp class="w-6 md:w-8 h-6 md:h-8 text-green-600 mb-3 mx-auto" />
                <div class="text-2xl md:text-4xl font-bold text-slate-900 mb-1 text-center">23</div>
                <div class="text-xs md:text-sm text-slate-600 text-center">Partidos políticos</div>
              </div>
              <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-slate-100">
                <FileText class="w-6 md:w-8 h-6 md:h-8 text-purple-600 mb-3 mx-auto" />
                <div class="text-2xl md:text-4xl font-bold text-slate-900 mb-1 text-center">+10k</div>
                <div class="text-xs md:text-sm text-slate-600 text-center">Votações analisadas</div>
              </div>
              <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-slate-100">
                <BarChart3 class="w-6 md:w-8 h-6 md:h-8 text-orange-600 mb-3 mx-auto" />
                <div class="text-2xl md:text-4xl font-bold text-slate-900 mb-1 text-center">Real-time</div>
                <div class="text-xs md:text-sm text-slate-600 text-center">Atualização diária</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Problema e Solução -->
      <section class="py-20 bg-white">
        <div class="max-w-5xl mx-auto px-4">
          <div class="max-w-4xl mx-auto">
            <div class="flex flex-col md:flex-row items-start gap-4 p-6 md:p-8 bg-red-50 border-l-4 border-red-500 rounded-r-2xl mb-8">
              <AlertCircle class="w-6 h-6 text-red-600 mt-1 flex-shrink-0" />
              <div class="text-center md:text-left">
                <h3 class="text-xl font-bold text-slate-900 mb-2">O Problema</h3>
                <p class="text-slate-700 leading-relaxed">
                  Embora a Câmara e o Senado disponibilizem dados públicos, o acesso exige conhecimento 
                  técnico para manipular <strong>APIs, CSV e JSON</strong>. O Portal da Transparência 
                  limita-se a consultas individualizadas, incapaz de gerar <strong>estatísticas consolidadas, 
                  tendências e métricas comparativas</strong> essenciais para uma avaliação objetiva.
                </p>
              </div>
            </div>

            <div class="flex flex-col md:flex-row items-start gap-4 p-6 md:p-8 bg-green-50 border-l-4 border-green-500 rounded-r-2xl">
              <CheckCircle2 class="w-6 h-6 text-green-600 mt-1 flex-shrink-0" />
              <div class="text-center md:text-left">
                <h3 class="text-xl font-bold text-slate-900 mb-2">Nossa Solução</h3>
                <p class="text-slate-700 leading-relaxed">
                  Convertemos dados complexos em <strong>visualizações intuitivas, indicadores objetivos 
                  e dashboards comparativos</strong>. Qualquer pessoa pode avaliar gastos, votações e 
                  fidelidade partidária sem conhecimento técnico. <strong class="text-green-700">
                  A fiscalização parlamentar deixa de ser privilégio de especialistas</strong>.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Funcionalidades Principais -->
      <section id="funcionalidades" class="py-20 bg-slate-50">
        <div class="max-w-5xl mx-auto px-4">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              O que você pode fiscalizar
            </h2>
            <p class="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto">
              Três pilares fundamentais para avaliar a atuação parlamentar de forma completa e objetiva
            </p>
          </div>

          <div class="flex flex-wrap justify-center gap-6 md:gap-8">
            <div 
              v-for="(feature, idx) in features" 
              :key="idx" 
              class="w-full max-w-sm bg-white rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-xl transition-all border border-slate-100"
            >
              <div class="text-center">
                <div :class="`w-16 h-16 bg-${feature.color}-100 rounded-2xl flex items-center justify-center text-3xl mb-6 mx-auto`">
                  {{ feature.icon }}
                </div>
                <h3 class="text-xl md:text-2xl font-bold text-slate-900 mb-3">{{ feature.title }}</h3>
                <p class="text-slate-600 mb-6">{{ feature.description }}</p>
                <ul class="space-y-3 text-left">
                  <li 
                    v-for="(item, i) in feature.features" 
                    :key="i" 
                    class="flex items-start gap-2 text-sm text-slate-700"
                  >
                    <CheckCircle2 class="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span>{{ item }}</span>
                  </li>
                </ul>
                <button class="mt-6 w-full py-3 bg-slate-100 hover:bg-slate-200 text-slate-900 font-semibold rounded-xl transition-colors">
                  Explorar
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Como Funciona -->
      <section id="como-usar" class="py-20 bg-white">
        <div class="max-w-5xl mx-auto px-4">
          <div class="text-center mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Como transformamos dados em transparência
            </h2>
            <p class="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto">
              Processo automatizado que garante precisão, atualização constante e total confiabilidade
            </p>
          </div>

          <div class="flex flex-wrap justify-center gap-8 md:gap-12">
            <div 
              v-for="(step, idx) in steps" 
              :key="idx" 
              class="relative text-center max-w-xs"
            >
              <div class="flex flex-col items-center">
                <div class="w-20 h-20 bg-gradient-to-br from-blue-600 to-blue-800 rounded-2xl flex items-center justify-center text-white mb-6 shadow-lg relative">
                  <component :is="step.icon" class="w-8 h-8" />
                  <div class="absolute -top-2 -left-2 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span class="text-sm font-bold text-blue-600">{{ step.number }}</span>
                  </div>
                </div>
                <h3 class="text-xl font-bold text-slate-900 mb-3">{{ step.title }}</h3>
                <p class="text-slate-600 leading-relaxed">{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Fontes e Metodologia -->
      <section class="py-20 bg-slate-50">
        <div class="max-w-5xl mx-auto px-4">
          <div class="bg-white rounded-3xl p-8 md:p-12 shadow-xl border border-slate-100">
            <div class="max-w-4xl mx-auto text-center">
              <div class="flex items-center justify-center gap-3 mb-8">
                <Shield class="w-10 h-10 text-blue-600" />
                <h2 class="text-2xl md:text-3xl font-bold text-slate-900">Confiabilidade e Transparência</h2>
              </div>
              
              <div class="grid md:grid-cols-2 gap-8 mb-8 text-left">
                <div>
                  <h3 class="text-lg font-bold text-slate-900 mb-4 text-center md:text-left">📊 Fontes Oficiais</h3>
                  <ul class="space-y-2 text-slate-700">
                    <li class="flex items-start gap-2">
                      <CheckCircle2 class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>API de Dados Abertos da Câmara dos Deputados</span>
                    </li>
                    <li class="flex items-start gap-2">
                      <CheckCircle2 class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>API do Senado Federal</span>
                    </li>
                    <li class="flex items-start gap-2">
                      <CheckCircle2 class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>Portal da Transparência</span>
                    </li>
                  </ul>
                </div>
                
                <div>
                  <h3 class="text-lg font-bold text-slate-900 mb-4 text-center md:text-left">🔄 Atualização</h3>
                  <ul class="space-y-2 text-slate-700">
                    <li class="flex items-start gap-2">
                      <CheckCircle2 class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>Sincronização automática diária</span>
                    </li>
                    <li class="flex items-start gap-2">
                      <CheckCircle2 class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>Verificação de integridade dos dados</span>
                    </li>
                    <li class="flex items-start gap-2">
                      <CheckCircle2 class="w-5 h-5 text-green-600 mt-0.5 flex-shrink-0" />
                      <span>Registro completo de alterações</span>
                    </li>
                  </ul>
                </div>
              </div>

              <div class="bg-blue-50 border border-blue-200 rounded-xl p-6">
                <p class="text-slate-700 leading-relaxed text-center">
                  <strong class="text-slate-900">Compromisso com a precisão:</strong> Todos os dados 
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
      <section class="py-20 bg-gradient-to-br from-blue-600 to-blue-800 text-white">
        <div class="max-w-4xl mx-auto px-4 text-center">
          <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
            A fiscalização começa agora
          </h2>
          <p class="text-lg md:text-xl text-blue-100 mb-10 leading-relaxed max-w-3xl mx-auto">
            Não é preciso ser especialista para acompanhar seus representantes. Exercer a cidadania 
            fiscalizadora é um direito fundamental – e agora está ao alcance de todos.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <button class="px-8 md:px-10 py-4 bg-white text-blue-700 font-bold rounded-xl hover:bg-blue-50 transition-colors shadow-xl flex items-center justify-center gap-2">
              Começar a Fiscalizar
              <ArrowRight class="w-5 h-5" />
            </button>
            <button class="px-8 md:px-10 py-4 bg-blue-700 text-white font-bold rounded-xl hover:bg-blue-800 transition-colors border-2 border-blue-400">
              Sobre o Projeto
            </button>
          </div>
          <p class="text-sm text-blue-200 mt-8">
            ✓ 100% gratuito · ✓ Sem cadastro · ✓ Dados oficiais verificados
          </p>
        </div>
      </section>

      <!-- Footer -->
      <footer class="bg-slate-900 text-slate-300 py-12">
        <div class="max-w-6xl mx-auto px-4">
          <div class="grid md:grid-cols-3 gap-8 mb-8 text-center md:text-left">
            <div class="flex flex-col items-center md:items-start">
              <div class="flex items-center gap-2 mb-4">
                <Shield class="w-6 h-6 text-blue-400" />
                <span class="text-xl font-bold text-white">Fiscaliza Brasil</span>
              </div>
              <p class="text-sm text-slate-400 leading-relaxed max-w-xs">
                Democratizando o acesso aos dados parlamentares para promover a fiscalização cidadã 
                e fortalecer a transparência democrática.
              </p>
            </div>
            
            <div class="flex flex-col items-center md:items-start">
              <h4 class="font-bold text-white mb-4">Sobre o Projeto</h4>
              <p class="text-sm text-slate-400 max-w-xs">
                Trabalho de Conclusão de Curso desenvolvido com o objetivo de quebrar as barreiras 
                técnicas que impedem o acesso amplo aos dados públicos parlamentares.
              </p>
            </div>
            
            <div class="flex flex-col items-center md:items-start">
              <h4 class="font-bold text-white mb-4">Fontes de Dados</h4>
              <ul class="space-y-2 text-sm text-slate-400">
                <li>• Câmara dos Deputados (API Oficial)</li>
                <li>• Senado Federal (API Oficial)</li>
                <li>• Portal da Transparência</li>
              </ul>
            </div>
          </div>
          
          <div class="border-t border-slate-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-center">
            <p class="text-sm text-slate-500">
              © 2025 Fiscaliza Brasil · TCC · Todos os dados são públicos e verificáveis
            </p>
            <p class="text-sm text-slate-500">
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
  AlertCircle 
} from 'lucide-vue-next'

const searchQuery = ref('')

const handleSearch = (e: Event) => {
  e.preventDefault()
  console.log('Buscando por:', searchQuery.value)
}

const features = [
  {
    icon: "💰",
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
    icon: "🗳️",
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
    icon: "🎯",
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
    number: "1",
    icon: Database,
    title: "Coleta Automatizada",
    description: "Extração diária via APIs oficiais da Câmara dos Deputados e Senado Federal. Dados brutos em JSON, CSV e XML são capturados com total integridade."
  },
  {
    number: "2",
    icon: BarChart3,
    title: "Processamento Inteligente",
    description: "Algoritmos convertem dados técnicos em estatísticas consolidadas, identificam tendências, calculam índices e geram métricas comparativas objetivas."
  },
  {
    number: "3",
    icon: Eye,
    title: "Visualização Acessível",
    description: "Dashboards intuitivos, gráficos interativos e relatórios compreensíveis. Sem jargão técnico, sem barreiras de acesso."
  }
]
</script>

<style scoped>
/* Garantir centralização em todas as seções */
section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* Centralizar container principal */
.container-center {
  margin-left: auto;
  margin-right: auto;
  text-align: center;
}

/* Forçar centralização do header */
header nav {
  justify-content: center !important;
}

@media (min-width: 768px) {
  header nav {
    justify-content: space-between !important;
  }
}

/* Centralizar elementos flexbox */
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Grid centralizado */
.grid-center {
  display: grid;
  place-items: center;
}
</style>