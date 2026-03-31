<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <!-- Hero -->
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="flex items-center gap-3 mb-3">
            <div class="p-2 rounded-lg bg-primary/15">
              <Landmark class="h-6 w-6 text-primary" />
            </div>
            <span class="text-sm font-medium text-primary uppercase tracking-wider">Câmara dos Deputados</span>
          </div>
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
            <div>
              <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Comissões Parlamentares</h1>
              <p class="mt-2 text-muted-foreground max-w-2xl">
                Explore as comissões permanentes e temporárias da Câmara dos Deputados. Saiba quem são os membros, presidentes e relatores de cada uma.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Stats -->
      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-4 sm:grid-cols-3">
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-primary/10">
                  <LayoutGrid class="h-6 w-6 text-primary" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total de Comissões</p>
                  <p v-if="!loading" class="text-2xl font-bold text-foreground">{{ comissoesFiltradas.length }}</p>
                  <div v-else class="h-8 w-16 bg-muted animate-pulse rounded mt-1" />
                </div>
              </div>
            </BaseCard>
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-chart-2/10">
                  <Users class="h-6 w-6 text-chart-2" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Total de Membros</p>
                  <p v-if="!loading" class="text-2xl font-bold text-foreground">
                    {{ comissoesFiltradas.reduce((s, c) => s + (c.total_membros || 0), 0).toLocaleString('pt-BR') }}
                  </p>
                  <div v-else class="h-8 w-16 bg-muted animate-pulse rounded mt-1" />
                </div>
              </div>
            </BaseCard>
            <BaseCard hover>
              <div class="flex items-center gap-4">
                <div class="p-3 rounded-xl bg-chart-3/10">
                  <ShieldCheck class="h-6 w-6 text-chart-3" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">Comissões Permanentes</p>
                  <p v-if="!loading" class="text-2xl font-bold text-foreground">
                    {{ comissoes.filter(c => c.tipo?.toLowerCase().includes('permanente')).length }}
                  </p>
                  <div v-else class="h-8 w-16 bg-muted animate-pulse rounded mt-1" />
                </div>
              </div>
            </BaseCard>
          </div>
        </div>
      </section>

      <!-- Search + List -->
      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="mb-6 space-y-4">
            <div class="flex flex-col sm:flex-row gap-4">
              <!-- Buscas (Ementa/Comissão vs Membro) -->
              <div class="relative flex-1">
                <Search class="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar por comissão ou sigla..."
                  class="w-full pl-12 pr-6 py-4 rounded-full border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-black/20 hover:shadow-md transition-shadow text-base"
                />
              </div>
              <div class="relative flex-1">
                <Users class="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                <input
                  v-model="searchMemberQuery"
                  type="text"
                  placeholder="Buscar por membro (deputado)..."
                  class="w-full pl-12 pr-6 py-4 rounded-full border border-border bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-black/20 hover:shadow-md transition-shadow text-base"
                />
              </div>

              <!-- Legislatura -->
              <select
                v-model="filterLegislatura"
                class="w-full sm:w-auto sm:min-w-[220px] px-6 py-4 sm:py-3.5 rounded-full border border-foreground/20 bg-background font-semibold text-foreground focus:outline-none focus:ring-2 focus:ring-black/20 text-sm"
              >
                <option :value="0">Todas as legislaturas</option>
                <option v-for="leg in availableLegislaturas" :key="leg" :value="leg">{{ leg }}ª</option>
              </select>
            </div>

            <!-- Segunda linha: Filtros dropdown -->
            <div class="flex flex-col sm:flex-row gap-4">
              <select
                v-model="filterTipo"
                class="w-full sm:w-auto sm:min-w-[180px] px-6 py-4 sm:py-3.5 rounded-full border border-border bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-black/20 text-sm"
              >
                <option value="">Todos os tipos</option>
                <option v-for="tipo in tiposDisponiveis" :key="tipo" :value="tipo">{{ tipo }}</option>
              </select>
            </div>
          </div>

          <!-- Error -->
          <div v-if="error" class="mb-4 px-4 py-3 rounded-lg bg-destructive/10 border border-destructive/30 text-destructive text-sm flex items-center gap-2">
            <AlertCircle class="h-4 w-4 flex-shrink-0" />
            {{ error }}
          </div>

          <!-- Loading skeleton -->
          <div v-if="loading" class="space-y-3">
            <div v-for="i in 6" :key="i" class="h-20 bg-muted animate-pulse rounded-xl" />
          </div>

          <!-- Empty -->
          <div v-else-if="comissoesFiltradas.length === 0" class="text-center py-16 text-muted-foreground">
            Nenhuma comissão encontrada com os filtros aplicados.
          </div>

          <!-- List -->
          <div v-else class="space-y-3">
            <BaseCard
              v-for="comissao in displayedComissoes"
              :key="comissao.id"
              hover
              class="transition-all cursor-pointer"
              @click="selectedComissao = selectedComissao?.id === comissao.id ? null : comissao"
            >
              <div class="flex items-center gap-4">
                <div class="flex-shrink-0 w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center overflow-hidden p-1">
                  <span class="text-[10px] font-bold text-primary text-center leading-tight break-all line-clamp-3">{{ comissao.sigla }}</span>
                </div>

                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 flex-wrap">
                    <a
                      v-if="comissao.sigla"
                      :href="comissao.url_website || `https://www.camara.leg.br/comissoes/orgao-detalhes?id=${comissao.id}`"
                      target="_blank"
                      rel="noopener noreferrer"
                      @click.stop
                      class="inline-flex items-center gap-1 text-xs text-primary hover:underline group ml-1"
                    >
                      <span class="hidden sm:inline">Ver na Câmara</span>
                      <ExternalLink class="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
                    </a>
                    <span
                      v-if="comissao.tipo"
                      :class="[
                        'text-[10px] px-2 py-0.5 rounded-full font-medium whitespace-nowrap',
                        comissao.tipo.toLowerCase().includes('permanente') ? 'bg-black/5 text-black/70 border border-black/10' :
                        comissao.tipo.toLowerCase().includes('cpi') || comissao.tipo.toLowerCase().includes('inquérito') ? 'bg-red-500/10 text-red-600' :
                        'bg-muted text-muted-foreground border border-border'
                      ]"
                    >{{ comissao.tipo }}</span>
                  </div>
                  <h3 class="text-sm font-semibold text-foreground line-clamp-1 mt-0.5">{{ comissao.nome }}</h3>
                  <div class="flex items-center gap-4 mt-1 text-xs text-muted-foreground">
                    <span class="flex items-center gap-1">
                      <Users class="h-3 w-3" /> {{ comissao.total_membros || 0 }} membros
                    </span>
                    <span v-if="comissao.presidente" class="flex items-center gap-1 truncate">
                      <Crown class="h-3 w-3" /> Pres: {{ comissao.presidente }}
                    </span>
                  </div>
                </div>

                <!-- Partidos dominantes -->
                <div class="hidden md:flex gap-1 flex-wrap max-w-[160px] justify-end">
                  <span
                    v-for="partido in comissao.partidos_destaque"
                    :key="partido"
                    class="text-[10px] px-1.5 py-0.5 bg-muted rounded font-mono"
                  >{{ partido }}</span>
                </div>

                <ChevronDown
                  class="h-4 w-4 text-muted-foreground flex-shrink-0 transition-transform"
                  :class="{ 'rotate-180': selectedComissao?.id === comissao.id }"
                />
              </div>

              <!-- Expandido: membros -->
              <transition name="expand">
                <div v-if="selectedComissao?.id === comissao.id" class="mt-4 pt-4 border-t border-border">
                  <p class="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3">Membros</p>
                  <div v-if="comissao.membros?.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                    <div
                      v-for="membro in comissao.membros"
                      :key="membro.id"
                      class="flex items-center gap-2 p-2 rounded-lg bg-muted/50 hover:bg-muted transition-colors cursor-pointer group"
                      @click.stop="goToMember(membro.id)"
                    >
                      <div class="w-8 h-8 rounded-full border border-border overflow-hidden bg-background flex-shrink-0 relative">
                        <img
                          :src="`https://www.camara.leg.br/internet/deputado/bandep/${membro.id}.jpg`"
                          :alt="membro.nome"
                          class="w-full h-full object-cover relative z-10"
                          @error="($event.target as HTMLImageElement).src = '/placeholder-user.svg'"
                        />
                        <User class="h-4 w-4 text-muted-foreground absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-20" />
                      </div>
                      <div class="min-w-0">
                        <p class="text-xs font-medium text-foreground truncate group-hover:text-primary transition-colors">{{ membro.nome }}</p>
                        <p class="text-[10px] text-muted-foreground">{{ membro.partido }} · {{ membro.uf }}</p>
                      </div>
                      <span
                        v-if="membro.cargo"
                        class="ml-auto text-[10px] px-1 py-0.5 rounded bg-black/5 text-black/70 font-medium flex-shrink-0"
                      >{{ membro.cargo }}</span>
                    </div>
                  </div>
                  <p v-else class="text-xs text-muted-foreground italic">Nenhum membro registrado.</p>
                </div>
              </transition>
            </BaseCard>

            <!-- Load more -->
            <div v-if="comissoesFiltradas.length > displayedCount" class="flex justify-center mt-8 pb-4">
              <button
                @click="loadMore"
                class="px-6 py-3 rounded-xl border border-border bg-background text-foreground font-medium hover:bg-muted transition-all active:scale-95 inline-flex items-center gap-2 shadow-sm"
              >
                <span>Carregar mais</span>
                <ChevronDown class="h-4 w-4" />
              </button>
            </div>
          </div>

        </div>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Landmark, Users, LayoutGrid, ShieldCheck, Crown, User, ChevronDown, AlertCircle, Search, ExternalLink } from 'lucide-vue-next'
import { useLoadingStore } from '@/stores/loading'
import BaseCard from '@/components/ui/BaseCard.vue'

interface Membro {
  id: number
  nome: string
  partido: string
  uf: string
  cargo?: string | null
}

interface Comissao {
  id: number
  sigla: string
  nome: string
  tipo: string
  total_membros: number
  url_website?: string | null
  presidente: string | null
  partidos_destaque: string[]
  membros: Membro[]
}

const router = useRouter()
const searchQuery = ref('')
const searchMemberQuery = ref('')
const filterTipo = ref('')
const filterLegislatura = ref(57) // Default to 57
const availableLegislaturas = ref<number[]>([])

const displayedCount = ref(15)
const loadMoreCount = 15
const selectedComissao = ref<Comissao | null>(null)
const comissoes = ref<Comissao[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

const apiUrl = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
const loadingStore = useLoadingStore()

const fetchComissoes = async () => {
  loadingStore.startLoading('Carregando comissões...')
  loading.value = true
  try {
    const params = new URLSearchParams()
    if (filterLegislatura.value) params.append('legislatura', filterLegislatura.value.toString())
    
    const res = await fetch(`${apiUrl}/api/camara/comissoes?${params.toString()}`)
    if (!res.ok) throw new Error(`Erro ${res.status}: ${res.statusText}`)
    const data = await res.json()
    comissoes.value = data.comissoes ?? []
  } catch (err: any) {
    console.error('Erro ao buscar comissões:', err)
    error.value = err.message || 'Não foi possível carregar as comissões.'
  } finally {
    await nextTick()
    setTimeout(() => {
      loading.value = false
      loadingStore.stopLoading()
    }, 500)
  }
}

onMounted(async () => {
  // Fetch Legislaturas
  try {
    const resLeg = await fetch(`${apiUrl}/api/camara/legislaturas`)
    if (resLeg.ok) {
      availableLegislaturas.value = await resLeg.json()
    }
  } catch (e) {
    console.error('Erro ao buscar legislaturas:', e)
  }

  await fetchComissoes()
})

import { watch } from 'vue'
watch(filterLegislatura, () => {
  displayedCount.value = 15
  selectedComissao.value = null
  fetchComissoes()
})

const tiposDisponiveis = computed(() => {
  const set = new Set(comissoes.value.map(c => c.tipo).filter(Boolean))
  return Array.from(set).sort()
})

const comissoesFiltradas = computed(() => {
  return comissoes.value.filter(c => {
    // Filtro por Tipo
    const matchTipo = !filterTipo.value || c.tipo === filterTipo.value
    
    // Filtro por nome/sigla da comissão
    const q = searchQuery.value.toLowerCase()
    const matchComissao = !q ||
      (c.nome ?? '').toLowerCase().includes(q) ||
      (c.sigla ?? '').toLowerCase().includes(q)

    // Filtro por membro
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

watch([searchQuery, searchMemberQuery, filterTipo], () => {
  displayedCount.value = 15
  selectedComissao.value = null
})

const goToMember = (id: number) => {
  router.push(`/camara/deputados/${id}`)
}
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition: all 0.2s ease;
  overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}
.expand-enter-to,
.expand-leave-from {
  opacity: 1;
  max-height: 500px;
}
</style>
