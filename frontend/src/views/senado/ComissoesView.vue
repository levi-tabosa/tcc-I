<template>
  <div class="min-h-screen flex flex-col bg-background">
    <main class="flex-1">
      <!-- Hero Section with Dynamic Purple Background -->
      <section class="relative overflow-hidden pt-16 pb-20 lg:pt-24 lg:pb-32">
        <div class="absolute inset-0 -z-10 overflow-hidden">
          <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-purple-500/20 blur-[120px] animate-pulse" />
          <div class="absolute top-[20%] -right-[10%] w-[35%] h-[35%] rounded-full bg-accent/20 blur-[100px] animate-pulse" style="animation-delay: 2s" />
        </div>
        
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex flex-col items-center text-center">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-600 dark:text-purple-400 text-xs font-bold uppercase tracking-widest mb-6 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <Landmark class="h-4 w-4" />
              <span>Senado Federal</span>
            </div>
            
            <h1 class="text-4xl font-extrabold tracking-tight text-foreground sm:text-6xl mb-6 animate-in fade-in slide-in-from-bottom-6 duration-1000">
              Comissões do <span class="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-purple-400">Senado</span>
            </h1>
            
            <p class="max-w-2xl text-lg text-muted-foreground mb-10 animate-in fade-in slide-in-from-bottom-8 duration-1000 delay-200">
              Monitore a atuação do Senado Federal através de suas comissões. Descubra lideranças, composições e o impacto das decisões nas comissões permanentes e especiais.
            </p>
          </div>
        </div>
      </section>

      <!-- Stats Cards with Glassmorphism -->
      <section class="-mt-16 relative z-10">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-6 sm:grid-cols-3">
            <div 
              v-for="(stat, idx) in statsData" 
              :key="idx"
              class="group relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 p-8 transition-all hover:bg-white/10 hover:shadow-2xl hover:shadow-purple-500/5 active:scale-[0.98] backdrop-blur-md animate-in fade-in zoom-in duration-700"
              :style="{ 'animation-delay': `${idx * 150}ms` }"
            >
              <div class="absolute top-0 right-0 -mr-4 -mt-4 h-24 w-24 rounded-full opacity-10 transition-transform group-hover:scale-150" :class="stat.colorClass" />
              <div class="flex items-center gap-5 relative z-10">
                <div class="flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br shadow-lg transition-transform group-hover:rotate-6" :class="stat.gradientClass">
                  <component :is="stat.icon" class="h-7 w-7 text-white" />
                </div>
                <div>
                  <p class="text-sm font-semibold text-muted-foreground uppercase tracking-wider">{{ stat.label }}</p>
                  <p v-if="!loading" class="text-3xl font-black text-foreground mt-1">{{ stat.value }}</p>
                  <div v-else class="h-9 w-20 bg-white/10 animate-pulse rounded-lg mt-1" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Search & Filters -->
      <section class="py-16">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex flex-col gap-6 p-8 rounded-[40px] bg-muted/20 border border-border/50 backdrop-blur-sm">
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-4">
              <!-- Search Commissions -->
              <div class="lg:col-span-2 relative group">
                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                  <Search class="h-5 w-5 text-muted-foreground group-focus-within:text-purple-500 transition-colors" />
                </div>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Nome ou sigla da comissão..."
                  class="block w-full pl-14 pr-6 py-4 bg-background border-2 border-border/50 rounded-2xl text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all text-base font-medium shadow-sm"
                />
              </div>

              <!-- Search Members -->
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                  <UserSearch class="h-5 w-5 text-muted-foreground group-focus-within:text-accent transition-colors" />
                </div>
                <input
                  v-model="searchMemberQuery"
                  type="text"
                  placeholder="Filtrar por senador..."
                  class="block w-full pl-14 pr-6 py-4 bg-background border-2 border-border/50 rounded-2xl text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-accent/50 focus:ring-4 focus:ring-accent/10 transition-all text-base font-medium shadow-sm"
                />
              </div>

              <!-- Legislatura -->
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
                  <CalendarRange class="h-5 w-5 text-muted-foreground group-focus-within:text-purple-500 transition-colors" />
                </div>
                <select
                  v-model="filterLegislatura"
                  class="block w-full pl-14 pr-12 py-4 bg-background border-2 border-border/50 rounded-2xl text-foreground font-bold focus:outline-none focus:border-purple-500/50 focus:ring-4 focus:ring-purple-500/10 transition-all appearance-none cursor-pointer shadow-sm"
                >
                  <option :value="0">Todas as Legislaturas</option>
                  <option v-for="leg in availableLegislaturas" :key="leg" :value="leg">{{ leg }}ª Legislatura</option>
                </select>
                <div class="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                  <ChevronDown class="h-5 w-5 text-muted-foreground" />
                </div>
              </div>
            </div>

            <!-- More Filters (Tipo) -->
            <div class="flex flex-wrap gap-2 pt-2">
              <button
                v-for="tipo in ['Todos', ...tiposDisponiveis]"
                :key="tipo"
                @click="filterTipo = (tipo === 'Todos' ? '' : tipo)"
                class="px-5 py-2 rounded-full text-sm font-bold transition-all border-2"
                :class="[
                  (filterTipo === (tipo === 'Todos' ? '' : tipo))
                    ? 'bg-purple-600 border-purple-600 text-white shadow-lg shadow-purple-500/20 scale-105'
                    : 'bg-background border-border/60 text-muted-foreground hover:border-purple-500/40 hover:text-foreground'
                ]"
              >
                {{ tipo }}
              </button>
            </div>
          </div>

          <!-- Main List Content -->
          <div class="mt-12">
            <!-- Results Feedback -->
            <div class="flex items-center justify-between mb-8 px-4">
              <div class="flex items-baseline gap-2">
                <span class="text-3xl font-black text-foreground">{{ comissoesFiltradas.length }}</span>
                <span class="text-muted-foreground font-medium uppercase tracking-widest text-xs">Resultados encontrados</span>
              </div>
            </div>

            <!-- Error State -->
            <div v-if="error" class="bg-destructive/10 border-2 border-destructive/20 rounded-3xl p-8 text-center">
              <div class="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-destructive/10 text-destructive mb-4">
                <AlertCircle class="h-8 w-8" />
              </div>
              <h3 class="text-lg font-bold text-foreground mb-2">Ops! Ocorreu um erro</h3>
              <p class="text-muted-foreground mb-6">{{ error }}</p>
              <button @click="fetchComissoes" class="px-6 py-2 bg-destructive text-white rounded-xl font-bold hover:opacity-90 transition-opacity">
                Tentar novamente
              </button>
            </div>

            <!-- Skeleton Loading -->
            <div v-else-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div v-for="i in 9" :key="i" class="h-64 bg-muted animate-pulse rounded-[32px] border border-border/50" />
            </div>

            <!-- Empty State -->
            <div v-else-if="comissoesFiltradas.length === 0" class="py-20 text-center bg-muted/10 rounded-[40px] border-2 border-dashed border-border/50">
              <div class="inline-flex h-20 w-20 items-center justify-center rounded-[30px] bg-muted/20 text-muted-foreground mb-6">
                <LayoutGrid class="h-10 w-10 opacity-50" />
              </div>
              <h3 class="text-2xl font-bold text-foreground mb-2">Sem resultados</h3>
              <p class="text-muted-foreground">Não encontramos comissões para sua busca atual.</p>
            </div>

            <!-- Grid List of Commissions -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div
                v-for="(comissao, idx) in displayedComissoes"
                :key="comissao.id"
                class="group relative flex flex-col bg-card border border-border/50 rounded-[40px] shadow-sm hover:shadow-2xl hover:shadow-purple-500/5 transition-all duration-500 overflow-hidden animate-in fade-in slide-in-from-bottom-8"
                :style="{ 'animation-delay': `${(idx % 9) * 100}ms` }"
              >
                <!-- Card Header -->
                <div class="p-8 pb-4">
                  <div class="flex justify-between items-start mb-6">
                    <div class="h-16 w-16 flex items-center justify-center rounded-[24px] bg-gradient-to-br from-purple-500/10 to-purple-500/5 border border-purple-500/20 group-hover:scale-110 transition-transform duration-500">
                      <span class="text-sm font-black text-purple-600 dark:text-purple-400">{{ comissao.sigla }}</span>
                    </div>
                    <div class="flex flex-col items-end gap-2">
                       <span
                        v-if="comissao.tipo"
                        :class="[
                          'text-[10px] px-3 py-1 rounded-full font-black uppercase tracking-widest border',
                          comissao.tipo.toLowerCase().includes('permanente') ? 'bg-purple-500/5 text-purple-600 border-purple-500/20' :
                          comissao.tipo.toLowerCase().includes('cpi') || comissao.tipo.toLowerCase().includes('inquérito') ? 'bg-red-500/5 text-red-600 border-red-500/20' :
                          'bg-muted text-muted-foreground border-border'
                        ]"
                      >{{ comissao.tipo }}</span>
                      <a
                        :href="`https://www25.senado.leg.br/web/comissoes/comissao/-/comissao/${comissao.id}`"
                        target="_blank"
                        rel="noopener noreferrer"
                        class="p-2 rounded-xl bg-muted hover:bg-purple-600 hover:text-white transition-all"
                        title="Ver no site oficial"
                      >
                        <ExternalLink class="h-4 w-4" />
                      </a>
                    </div>
                  </div>
                  
                  <h3 class="text-xl font-bold text-foreground leading-tight line-clamp-2 min-h-[3.5rem] group-hover:text-purple-600 transition-colors">
                    {{ comissao.nome }}
                  </h3>
                </div>

                <!-- Card Body (Stats) -->
                <div class="px-8 py-6 bg-muted/30 grid grid-cols-2 gap-4 border-y border-border/50">
                  <div class="flex flex-col">
                    <span class="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1">Membros</span>
                    <div class="flex items-center gap-2">
                      <Users class="h-4 w-4 text-purple-600" />
                      <span class="text-lg font-black">{{ comissao.total_membros || 0 }}</span>
                    </div>
                  </div>
                  <div class="flex flex-col">
                    <span class="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-1">Presidente</span>
                    <div class="flex items-center gap-2 overflow-hidden">
                      <Crown class="h-4 w-4 text-accent" />
                      <span class="text-sm font-bold truncate">{{ comissao.presidente || 'Vago' }}</span>
                    </div>
                  </div>
                </div>

                <!-- Members Quick View -->
                <div class="p-8 pt-6 flex-1 flex flex-col justify-between">
                  <div>
                    <span class="text-[10px] font-bold text-muted-foreground uppercase tracking-widest mb-4 block">Destaque Partidário</span>
                    <div class="flex flex-wrap gap-2 mb-6">
                      <span
                        v-for="partido in comissao.partidos_destaque"
                        :key="partido"
                        class="text-xs px-3 py-1 bg-white dark:bg-muted font-black border border-border/50 rounded-lg"
                      >{{ partido }}</span>
                      <span v-if="!comissao.partidos_destaque?.length" class="text-xs text-muted-foreground italic">Informação indisponível</span>
                    </div>
                  </div>

                  <button
                    @click="selectedComissao = selectedComissao?.id === comissao.id ? null : comissao"
                    class="w-full py-4 rounded-2xl bg-foreground text-background font-bold transition-all hover:translate-y-[-2px] hover:shadow-xl active:scale-95 flex items-center justify-center gap-2"
                  >
                    <span>{{ selectedComissao?.id === comissao.id ? 'Fechar Detalhes' : 'Ver Composição' }}</span>
                    <ChevronDown class="h-5 w-5 transition-transform duration-300" :class="{ 'rotate-180': selectedComissao?.id === comissao.id }" />
                  </button>
                </div>

                <!-- Expanded Member Panel -->
                <transition
                  enter-active-class="transition duration-500 ease-out"
                  enter-from-class="transform opacity-0 -translate-y-4"
                  enter-to-class="transform opacity-100 translate-y-0"
                  leave-active-class="transition duration-300 ease-in"
                  leave-from-class="transform opacity-100 translate-y-0"
                  leave-to-class="transform opacity-0 -translate-y-4"
                >
                  <div v-if="selectedComissao?.id === comissao.id" class="px-8 pb-8 animate-in fade-in duration-500 overflow-y-auto max-h-[400px] scrollbar-hide">
                    <div class="space-y-4">
                      <div
                        v-for="membro in comissao.membros"
                        :key="membro.id"
                        @click="goToMember(membro.id)"
                        class="flex items-center gap-4 p-4 rounded-3xl bg-muted/40 hover:bg-muted border border-border/50 transition-all cursor-pointer group/member"
                      >
                        <div class="h-12 w-12 rounded-2xl overflow-hidden bg-background border-2 border-border shadow-sm group-hover/member:border-purple-500 transition-colors">
                          <img
                            v-if="membro.foto"
                            :src="membro.foto"
                            :alt="membro.nome"
                            class="h-full w-full object-cover scale-110 group-hover/member:scale-125 transition-transform duration-500"
                          />
                          <img
                            v-else
                            :src="`https://www.senado.leg.br/senadores/img/fotos-oficiais/senador${membro.id}.jpg`"
                            :alt="membro.nome"
                            class="h-full w-full object-cover scale-110 group-hover/member:scale-125 transition-transform duration-500"
                            @error="($event.target as HTMLImageElement).src = '/placeholder-user.svg'"
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-bold text-foreground truncate group-hover/member:text-purple-600 transition-colors">{{ membro.nome }}</p>
                          <p class="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">{{ membro.partido }} · {{ membro.uf }}</p>
                        </div>
                        <div v-if="membro.cargo" class="px-2 py-1 rounded-lg bg-purple-500/10 text-[10px] font-black text-purple-600 border border-purple-500/20 uppercase whitespace-nowrap">
                          {{ membro.cargo }}
                        </div>
                      </div>
                    </div>
                  </div>
                </transition>
              </div>
            </div>

            <!-- Modern Pagination/Load More -->
            <div v-if="comissoesFiltradas.length > displayedCount" class="flex justify-center mt-20 pb-20">
              <button
                @click="loadMore"
                class="group relative px-10 py-5 bg-background border-2 border-purple-500/30 text-foreground font-black rounded-3xl hover:bg-purple-600 hover:text-white hover:border-purple-600 transition-all duration-300 shadow-xl shadow-purple-500/5 active:scale-95 overflow-hidden"
              >
                <div class="absolute inset-0 bg-purple-600 opacity-0 group-hover:opacity-100 transition-opacity" />
                <div class="relative flex items-center gap-3">
                  <span>Carregar Comissões Adicionais</span>
                  <ArrowDown class="h-5 w-5 animate-bounce" />
                </div>
              </button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Landmark, 
  Users, 
  LayoutGrid, 
  ShieldCheck, 
  Crown, 
  ChevronDown, 
  AlertCircle, 
  Search, 
  ExternalLink,
  UserSearch,
  CalendarRange,
  ArrowDown
} from 'lucide-vue-next'
import { useLoadingStore } from '@/stores/loading'

interface Membro {
  id: number
  nome: string
  partido: string
  uf: string
  cargo?: string | null
  foto?: string | null
}

interface Comissao {
  id: number
  sigla: string
  nome: string
  tipo: string
  total_membros: number
  presidente: string | null
  partidos_destaque: string[]
  membros: Membro[]
}

const router = useRouter()
const searchQuery = ref('')
const searchMemberQuery = ref('')
const filterTipo = ref('')
const filterLegislatura = ref(57)
const availableLegislaturas = ref<number[]>([])

const displayedCount = ref(15)
const loadMoreCount = 15
const selectedComissao = ref<Comissao | null>(null)
const comissoes = ref<Comissao[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const loadingStore = useLoadingStore()

// Fancy Stats Data for the Hero Stats Cards
const statsData = computed(() => [
  {
    label: 'Comissões Ativas',
    value: comissoesFiltradas.value.length,
    icon: LayoutGrid,
    gradientClass: 'from-purple-600 to-purple-500',
    colorClass: 'bg-purple-600'
  },
  {
    label: 'Total de Membros',
    value: comissoesFiltradas.value.reduce((s, c) => s + (c.total_membros || 0), 0).toLocaleString('pt-BR'),
    icon: Users,
    gradientClass: 'from-accent to-accent/80',
    colorClass: 'bg-accent'
  },
  {
    label: 'Permanentes',
    value: comissoes.value.filter(c => c.tipo?.toLowerCase().includes('permanente')).length,
    icon: ShieldCheck,
    gradientClass: 'from-green-500 to-emerald-600',
    colorClass: 'bg-green-500'
  }
])

const fetchComissoes = async () => {
  loadingStore.startLoading('Experiência Fiscaliza Brasil...')
  loading.value = true
  error.value = null
  try {
    const params = new URLSearchParams()
    if (filterLegislatura.value) params.append('legislatura', filterLegislatura.value.toString())
    
    const res = await fetch(`${apiUrl}/api/senado/comissoes?${params.toString()}`)
    if (!res.ok) throw new Error(`Erro ${res.status}: Não foi possível carregar os dados`)
    const data = await res.json()
    comissoes.value = data.comissoes ?? []
  } catch (err: any) {
    console.error('Erro ao buscar comissões:', err)
    error.value = err.message || 'Erro de conexão com o servidor.'
  } finally {
    await nextTick()
    setTimeout(() => {
      loading.value = false
      loadingStore.stopLoading()
    }, 800)
  }
}

onMounted(async () => {
  try {
    const resLeg = await fetch(`${apiUrl}/api/senado/legislaturas`)
    if (resLeg.ok) {
      availableLegislaturas.value = await resLeg.json()
    }
  } catch (e) {
    console.error('Erro ao buscar legislaturas:', e)
  }
  await fetchComissoes()
})

watch(filterLegislatura, () => {
  displayedCount.value = 15
  selectedComissao.value = null
  fetchComissoes()
})

watch([searchQuery, searchMemberQuery, filterTipo], () => {
  displayedCount.value = 15
  selectedComissao.value = null
})

const tiposDisponiveis = computed(() => {
  const set = new Set(comissoes.value.map(c => c.tipo).filter(Boolean))
  return Array.from(set).sort()
})

const comissoesFiltradas = computed(() => {
  return comissoes.value.filter(c => {
    const matchTipo = !filterTipo.value || c.tipo === filterTipo.value
    const q = searchQuery.value.toLowerCase()
    const matchComissao = !q ||
      (c.nome ?? '').toLowerCase().includes(q) ||
      (c.sigla ?? '').toLowerCase().includes(q)

    const mq = searchMemberQuery.value.toLowerCase()
    const matchMembro = !mq || c.membros.some(m => 
      m.nome.toLowerCase().includes(mq) || 
      m.partido.toLowerCase().includes(mq)
    )
    return matchTipo && matchComissao && matchMembro
  })
})

const displayedComissoes = computed(() => {
  return comissoesFiltradas.value.slice(0, displayedCount.value)
})

const loadMore = () => {
  displayedCount.value += loadMoreCount
}

const goToMember = (id: number) => {
  router.push(`/senado/senadores/${id}`)
}
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

@keyframes pulse {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.1); }
}

.animate-pulse {
  animation: pulse 8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
