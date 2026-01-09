<template>
  <div class="min-h-screen flex flex-col bg-background text-foreground">
    <main class="flex-1 py-8">
      <div class="container mx-auto px-4 max-w-6xl">
        
        <div class="header-section text-center mb-10">
          <h1 class="text-3xl font-bold text-primary mb-2">Comparativo de Parlamentares</h1>
          <p class="text-secondary">Selecione dois deputados para comparar gastos e indicadores lado a lado</p>
        </div>

        <!-- Área de Seleção -->
        <div class="selection-area grid md:grid-cols-2 gap-8 mb-12 relative">
          
          <!-- VS Badge no meio -->
          <div class="vs-badge">VS</div>

          <!-- Slot 1 -->
          <div class="selector-card">
            <div v-if="!deputado1" class="search-mode">
              <div class="icon-circle mb-4">
                <UserPlus class="w-8 h-8 text-primary" />
              </div>
              <h3 class="font-semibold mb-4 text-primary">Selecionar Parlamentar A</h3>
              <div class="relative w-full">
                <input 
                  v-model="termoBusca1"
                  @input="buscar(1)"
                  type="text" 
                  placeholder="Digite o nome..." 
                  class="search-input"
                />
                <!-- Lista de Resultados 1 -->
                <div v-if="resultados1.length > 0" class="search-results">
                  <div 
                    v-for="dep in resultados1" 
                    :key="dep.id"
                    @click="selecionarDeputado(1, dep)"
                    class="search-item"
                  >
                    <span class="font-medium text-primary">{{ dep.nome_civil }}</span>
                    <span class="text-xs text-secondary">{{ dep.uf }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="selected-mode">
              <button @click="removerDeputado(1)" class="remove-btn">
                <X class="w-4 h-4" />
              </button>
              <img :src="deputado1.foto" class="selected-foto" />
              <h2 class="text-xl font-bold mt-2 text-primary">{{ deputado1.nome }}</h2>
              <div class="flex gap-2 mt-2">
                <span class="tag tag-primary">{{ deputado1.partido }}</span>
                <span class="tag tag-secondary">{{ deputado1.estado }}</span>
              </div>
            </div>
          </div>

          <!-- Slot 2 -->
          <div class="selector-card">
            <div v-if="!deputado2" class="search-mode">
              <div class="icon-circle mb-4">
                <UserPlus class="w-8 h-8 text-primary" />
              </div>
              <h3 class="font-semibold mb-4 text-primary">Selecionar Parlamentar B</h3>
              <div class="relative w-full">
                <input 
                  v-model="termoBusca2"
                  @input="buscar(2)"
                  type="text" 
                  placeholder="Digite o nome..." 
                  class="search-input"
                />
                <!-- Lista de Resultados 2 -->
                <div v-if="resultados2.length > 0" class="search-results">
                  <div 
                    v-for="dep in resultados2" 
                    :key="dep.id"
                    @click="selecionarDeputado(2, dep)"
                    class="search-item"
                  >
                    <span class="font-medium text-primary">{{ dep.nome_civil }}</span>
                    <span class="text-xs text-secondary">{{ dep.uf }}</span>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="selected-mode">
              <button @click="removerDeputado(2)" class="remove-btn">
                <X class="w-4 h-4" />
              </button>
              <img :src="deputado2.foto" class="selected-foto" />
              <h2 class="text-xl font-bold mt-2 text-primary">{{ deputado2.nome }}</h2>
              <div class="flex gap-2 mt-2">
                <span class="tag tag-primary">{{ deputado2.partido }}</span>
                <span class="tag tag-secondary">{{ deputado2.estado }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Conteúdo da Comparação (Só aparece se tiver os 2) -->
        <div v-if="deputado1 && deputado2" class="comparison-content space-y-8 fade-in">
          
          <!-- 1. Indicadores Financeiros -->
          <div class="section-card">
            <h3 class="section-title mb-6 flex items-center justify-center gap-2 text-primary font-bold"><DollarSign class="w-5 h-5" /> Indicadores Financeiros</h3>
            
            <!-- Total Gasto -->
            <div class="metric-row">
              <div class="text-center mb-2 font-medium text-secondary">Total Gasto (Legislatura)</div>
              <div class="flex items-center justify-between gap-4">
                
                <!-- Barra Esq -->
                <div class="flex-1 flex flex-col items-end">
                  <span class="text-lg font-bold" :class="{'text-blue-600': dadosDep1.total > dadosDep2.total, 'text-foreground': dadosDep1.total <= dadosDep2.total}">
                    {{ formatCurrency(dadosDep1.total) }}
                  </span>
                  <div class="bar-container w-full flex justify-end">
                    <div class="bar-fill left" :style="{ width: getPorcentagem(dadosDep1.total) + '%' }"></div>
                  </div>
                </div>

                <div class="text-xs text-tertiary font-bold">VS</div>

                <!-- Barra Dir -->
                <div class="flex-1 flex flex-col items-start">
                  <span class="text-lg font-bold" :class="{'text-blue-600': dadosDep2.total > dadosDep1.total, 'text-foreground': dadosDep2.total <= dadosDep1.total}">
                    {{ formatCurrency(dadosDep2.total) }}
                  </span>
                  <div class="bar-container w-full flex justify-start">
                    <div class="bar-fill right" :style="{ width: getPorcentagem(dadosDep2.total) + '%' }"></div>
                  </div>
                </div>

              </div>
            </div>

            <!-- Média Mensal -->
            <div class="metric-row mt-6 pt-6 border-t border-border">
              <div class="text-center mb-2 font-medium text-secondary">Média Mensal</div>
              <div class="flex justify-between text-lg px-4">
                <span class="font-semibold text-foreground">{{ formatCurrency(dadosDep1.media) }}</span>
                <span class="font-semibold text-foreground">{{ formatCurrency(dadosDep2.media) }}</span>
              </div>
            </div>
            
             <!-- Quantidade de Despesas -->
            <div class="metric-row mt-4">
               <div class="text-center mb-2 font-medium text-secondary">Qtd. Notas Fiscais</div>
               <div class="flex justify-between text-lg px-4">
                 <span class="text-foreground">{{ dadosDep1.qtd }} notas</span>
                 <span class="text-foreground">{{ dadosDep2.qtd }} notas</span>
               </div>
            </div>
          </div>

          <!-- 2. Comparativo de Categorias (Top 3) -->
          <div class="grid md:grid-cols-2 gap-8">
            <!-- Dep 1 Categorias -->
            <div class="section-card">
              <h4 class="font-semibold text-primary mb-4 text-center">Top Gastos: {{ deputado1.nome }}</h4>
              <div class="space-y-4">
                <div v-for="cat in dadosDep1.topCategorias" :key="cat.tipo" class="relative">
                  <div class="flex justify-between text-sm mb-1">
                    <span class="truncate pr-2 text-foreground">{{ cat.tipo }}</span>
                    <span class="font-medium text-foreground">{{ formatCurrency(cat.total) }}</span>
                  </div>
                  <div class="h-2 bg-surface-secondary rounded-full overflow-hidden">
                    <div class="h-full bg-blue-500" :style="{ width: (cat.total / dadosDep1.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dep 2 Categorias -->
            <div class="section-card">
              <h4 class="font-semibold text-primary mb-4 text-center">Top Gastos: {{ deputado2.nome }}</h4>
              <div class="space-y-4">
                <div v-for="cat in dadosDep2.topCategorias" :key="cat.tipo" class="relative">
                  <div class="flex justify-between text-sm mb-1">
                    <span class="truncate pr-2 text-foreground">{{ cat.tipo }}</span>
                    <span class="font-medium text-foreground">{{ formatCurrency(cat.total) }}</span>
                  </div>
                  <div class="h-2 bg-surface-secondary rounded-full overflow-hidden">
                    <div class="h-full bg-green-500" :style="{ width: (cat.total / dadosDep2.total * 100) + '%' }"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

        <div v-else class="text-center py-12 text-tertiary">
          <p>Selecione dois parlamentares acima para gerar o relatório comparativo.</p>
        </div>

      </div>
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { UserPlus, X, DollarSign } from 'lucide-vue-next'
import AppFooter from '@/components/AppFooter.vue'

// --- Interfaces ---
interface DeputadoBusca {
  id: number
  nome_civil: string
  uf: string
}

interface DeputadoCompleto {
  id: number
  nome: string
  foto: string
  partido: string
  estado: string
}

// --- Estado ---
const termoBusca1 = ref('')
const termoBusca2 = ref('')
const resultados1 = ref<DeputadoBusca[]>([])
const resultados2 = ref<DeputadoBusca[]>([])

const deputado1 = ref<DeputadoCompleto | null>(null)
const deputado2 = ref<DeputadoCompleto | null>(null)

// Dados processados das despesas
const dadosDep1 = ref({ total: 0, media: 0, qtd: 0, topCategorias: [] as any[] })
const dadosDep2 = ref({ total: 0, media: 0, qtd: 0, topCategorias: [] as any[] })

// --- Funções de Busca ---
const buscar = async (slot: number) => {
  const termo = slot === 1 ? termoBusca1.value : termoBusca2.value
  if (termo.length < 2) {
    if (slot === 1) resultados1.value = []
    else resultados2.value = []
    return
  }

  try {
    const res = await fetch(`http://localhost:8000/api/deputados/buscar?nome=${termo}`)
    const data = await res.json()
    if (slot === 1) resultados1.value = data.resultados
    else resultados2.value = data.resultados
  } catch (err) {
    console.error(err)
  }
}

// --- Selecionar e Carregar Dados Completos ---
const selecionarDeputado = async (slot: number, depBasic: DeputadoBusca) => {
  // 1. Limpa busca
  if (slot === 1) { termoBusca1.value = ''; resultados1.value = [] }
  else { termoBusca2.value = ''; resultados2.value = [] }

  try {
    // 2. Busca Perfil Completo
    const resPerfil = await fetch(`http://localhost:8000/api/deputados/${depBasic.id}`)
    const perfil = await resPerfil.json()
    
    const objDeputado = {
      id: perfil.id,
      nome: perfil.nome_civil,
      foto: perfil.foto,
      partido: perfil.sigla_partido,
      estado: perfil.uf_nascimento
    }

    if (slot === 1) deputado1.value = objDeputado
    else deputado2.value = objDeputado

    // 3. Busca e Processa Despesas
    carregarDespesas(slot, depBasic.id)

  } catch (err) {
    console.error("Erro ao carregar detalhes", err)
  }
}

const carregarDespesas = async (slot: number, id: number) => {
  try {
    const res = await fetch(`http://localhost:8000/api/deputados/${id}/despesas`)
    const data = await res.json()
    const despesas = data.despesas || []

    // Cálculos
    const total = despesas.reduce((acc: number, d: any) => acc + d.valor, 0)
    const meses = new Set(despesas.map((d: any) => `${d.ano}-${d.mes}`)).size
    const media = meses > 0 ? total / meses : 0

    // Categorias
    const cats = despesas.reduce((acc: any, d: any) => {
      acc[d.tipo_despesa] = (acc[d.tipo_despesa] || 0) + d.valor
      return acc
    }, {})
    
    const topCategorias = Object.entries(cats)
      .map(([tipo, val]) => ({ tipo, total: Number(val) }))
      .sort((a, b) => b.total - a.total)
      .slice(0, 5)

    const stats = { total, media, qtd: despesas.length, topCategorias }

    if (slot === 1) dadosDep1.value = stats
    else dadosDep2.value = stats

  } catch (err) {
    console.error(err)
  }
}

const removerDeputado = (slot: number) => {
  if (slot === 1) deputado1.value = null
  else deputado2.value = null
}

// --- Utilitários de Visualização ---
const getPorcentagem = (valor: number) => {
  // Pega o maior valor entre os dois para usar como base 100%
  const max = Math.max(dadosDep1.value.total, dadosDep2.value.total)
  if (max === 0) return 0
  return (valor / max) * 100
}

const formatCurrency = (val: number) => {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val)
}
</script>

<style scoped>
/* Estilos Específicos da Página de Comparação */

.search-input {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--surface-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-primary);
  border-radius: 0.5rem;
  outline: none;
  transition: border-color 0.2s;
}
.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
}

.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--surface-primary);
  border: 1px solid var(--border-primary);
  border-radius: 0.5rem;
  margin-top: 4px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: var(--shadow-md);
}

.search-item {
  padding: 0.5rem 1rem;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.search-item:hover {
  background-color: var(--card-hover-bg);
}

.selector-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 1rem;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-sm);
}

.search-mode, .selected-mode {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.selected-foto {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--surface-primary);
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}

.vs-badge {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  background: #0f172a;
  color: white;
  font-weight: 900;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  z-index: 5;
  border: 4px solid var(--surface-primary);
  box-shadow: var(--shadow-md);
}

@media (max-width: 768px) {
  .vs-badge { top: 48%; } /* Ajuste fino para mobile */
}

.section-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: var(--shadow-sm);
}

.bar-container {
  height: 0.75rem;
  background-color: var(--surface-secondary);
  border-radius: 999px;
  overflow: hidden;
  margin-top: 0.25rem;
}

.bar-fill {
  height: 100%;
  transition: width 1s ease;
}
.bar-fill.left { background-color: var(--color-primary); border-radius: 999px 0 0 999px; }
.bar-fill.right { background-color: var(--color-success); border-radius: 0 999px 999px 0; }

.remove-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(254, 226, 226, 0.8);
  color: #ef4444;
  padding: 0.5rem;
  border-radius: 50%;
  cursor: pointer;
  border: none;
  transition: background 0.2s;
}
.remove-btn:hover { background: #fecaca; }

.tag {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}
.tag-primary { background: var(--color-primary-light); color: var(--text-white); }
.tag-secondary { background: var(--surface-secondary); color: var(--text-secondary); }

.fade-in { animation: fadeIn 0.5s ease-in-out; }
@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

/* Utilitários de texto e fundo substituídos por variáveis globais */
.text-primary { color: var(--text-primary); }
.text-secondary { color: var(--text-secondary); }
.text-tertiary { color: var(--text-tertiary); }
.bg-background { background-color: var(--bg-secondary); }
.text-foreground { color: var(--text-primary); }
.border-border { border-color: var(--border-primary); }
</style>