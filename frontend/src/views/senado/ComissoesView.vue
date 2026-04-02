<template>
  <div class="min-h-screen flex flex-col">
    <main class="flex-1">
      <section class="bg-gradient-to-br from-primary/10 via-background to-accent/10 py-12">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-foreground sm:text-4xl">Comissões do Senado</h1>
          <p class="mt-2 text-muted-foreground max-w-2xl">
            Consulte a composição, presidência e membros das comissões permanentes e temporárias do Senado Federal.
          </p>
        </div>
      </section>

      <section class="py-8 bg-muted/30">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div
              v-for="(stat, idx) in statsData"
              :key="idx"
              class="rounded-xl border border-border bg-background p-5"
            >
              <div class="flex items-center gap-4">
                <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <component :is="stat.icon" class="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p class="text-sm text-muted-foreground">{{ stat.label }}</p>
                  <p v-if="!loading" class="text-2xl font-bold text-foreground">{{ stat.value }}</p>
                  <div v-else class="h-8 w-20 rounded bg-muted animate-pulse" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="py-8">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="mb-6 space-y-4 rounded-xl border border-border bg-background p-4 sm:p-6">
            <div class="flex flex-col sm:flex-row gap-4">
              <div class="relative flex-1">
                <Search class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Buscar por nome ou sigla..."
                  class="w-full rounded-full border border-gray-300 bg-background px-4 py-3 pl-11 text-foreground placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div class="relative flex-1">
                <UserSearch class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <input
                  v-model="searchMemberQuery"
                  type="text"
                  placeholder="Buscar por senador..."
                  class="w-full rounded-full border border-gray-300 bg-background px-4 py-3 pl-11 text-foreground placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div class="relative">
                <CalendarRange class="absolute left-4 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <select
                  v-model="filterLegislatura"
                  class="w-full sm:w-auto appearance-none rounded-lg border border-purple-600/30 bg-purple-50 px-4 py-3 sm:py-2 pl-11 pr-10 font-semibold text-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option :value="0">Todas as Legislaturas</option>
                  <option v-for="leg in availableLegislaturas" :key="leg" :value="leg">{{ leg }}ª Legislatura</option>
                </select>
                <ChevronDown class="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground pointer-events-none" />
              </div>
            </div>
          </div>

          <p class="text-sm text-muted-foreground mb-4">
            {{ comissoesFiltradas.length.toLocaleString('pt-BR') }} comissões encontradas
          </p>

          <div v-if="error" class="rounded-lg border border-destructive/20 bg-destructive/10 p-6 text-center">
            <AlertCircle class="h-6 w-6 text-destructive mx-auto mb-2" />
            <p class="text-destructive mb-4">{{ error }}</p>
            <button
              @click="fetchComissoes"
              class="px-4 py-2 rounded-lg bg-destructive text-white font-medium hover:opacity-90"
            >
              Tentar novamente
            </button>
          </div>

          <div v-else-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="i in 9" :key="i" class="h-56 rounded-lg border border-border bg-muted animate-pulse" />
          </div>

          <div v-else-if="comissoesFiltradas.length === 0" class="rounded-lg border border-border bg-muted/20 py-12 text-center">
            <LayoutGrid class="h-8 w-8 text-muted-foreground mx-auto mb-2" />
            <p class="text-muted-foreground">Nenhuma comissão encontrada com os filtros atuais.</p>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div
              v-for="comissao in displayedComissoes"
              :key="comissao.id"
              class="rounded-xl border border-border bg-background overflow-hidden"
            >
              <div class="p-5">
                <div class="flex items-start justify-between gap-3">
                  <div class="min-w-0">
                    <div class="inline-flex items-center rounded-full bg-primary/10 px-2.5 py-1 text-xs font-semibold text-primary">
                      {{ comissao.sigla }}
                    </div>
                    <h3 class="mt-2 text-base font-semibold text-foreground line-clamp-2">{{ comissao.nome }}</h3>
                  </div>
                  <a
                    :href="`https://www25.senado.leg.br/web/comissoes/comissao/-/comissao/${comissao.id}`"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="inline-flex items-center justify-center rounded-md border border-border p-2 text-muted-foreground hover:text-foreground"
                    title="Ver no site oficial"
                  >
                    <ExternalLink class="h-4 w-4" />
                  </a>
                </div>

                <div class="mt-3">
                  <span
                    v-if="comissao.tipo"
                    class="inline-flex rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide"
                    :class="[
                      comissao.tipo.toLowerCase().includes('permanente')
                        ? 'bg-primary/10 text-primary border-primary/20'
                        : comissao.tipo.toLowerCase().includes('cpi') || comissao.tipo.toLowerCase().includes('inquérito')
                          ? 'bg-red-500/10 text-red-600 border-red-500/20'
                          : 'bg-muted text-muted-foreground border-border'
                    ]"
                  >
                    {{ comissao.tipo }}
                  </span>
                </div>
              </div>

              <div class="border-y border-border bg-muted/20 px-5 py-3 grid grid-cols-2 gap-3">
                <div>
                  <p class="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">Membros</p>
                  <p class="mt-1 flex items-center gap-1 text-sm font-semibold text-foreground">
                    <Users class="h-4 w-4 text-primary" />
                    {{ comissao.total_membros || 0 }}
                  </p>
                </div>
                <div>
                  <p class="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground">Presidente</p>
                  <p class="mt-1 flex items-center gap-1 text-sm font-semibold text-foreground truncate">
                    <Crown class="h-4 w-4 text-accent" />
                    {{ comissao.presidente || 'Vago' }}
                  </p>
                </div>
              </div>

              <div class="p-5">
                <p class="text-[10px] font-semibold uppercase tracking-wide text-muted-foreground mb-2">Destaques partidários</p>
                <div class="flex flex-wrap gap-2 mb-4">
                  <span
                    v-for="partido in comissao.partidos_destaque"
                    :key="partido"
                    class="rounded-full border border-border px-2.5 py-1 text-xs text-foreground"
                  >
                    {{ partido }}
                  </span>
                  <span v-if="!comissao.partidos_destaque?.length" class="text-xs text-muted-foreground italic">Informação indisponível</span>
                </div>

                <button
                  @click="selectedComissao = selectedComissao?.id === comissao.id ? null : comissao"
                  class="w-full inline-flex items-center justify-center gap-2 rounded-lg bg-foreground px-4 py-2 text-sm font-semibold text-background"
                >
                  {{ selectedComissao?.id === comissao.id ? 'Fechar composição' : 'Ver composição' }}
                  <ChevronDown class="h-4 w-4 transition-transform" :class="{ 'rotate-180': selectedComissao?.id === comissao.id }" />
                </button>
              </div>

              <div v-if="selectedComissao?.id === comissao.id" class="border-t border-border px-5 py-4 max-h-80 overflow-y-auto">
                <div class="space-y-3">
                  <div
                    v-for="membro in comissao.membros"
                    :key="membro.id"
                    @click="goToMember(membro.id)"
                    class="flex items-center gap-3 rounded-lg border border-border bg-muted/20 p-3 cursor-pointer hover:bg-muted"
                  >
                    <div class="h-10 w-10 overflow-hidden rounded-md border border-border bg-background">
                      <img
                        v-if="membro.foto"
                        :src="membro.foto"
                        :alt="membro.nome"
                        class="h-full w-full object-cover"
                      />
                      <img
                        v-else
                        :src="`https://www.senado.leg.br/senadores/img/fotos-oficiais/senador${membro.id}.jpg`"
                        :alt="membro.nome"
                        class="h-full w-full object-cover"
                        @error="($event.target as HTMLImageElement).src = '/placeholder-user.svg'"
                      />
                    </div>
                    <div class="min-w-0 flex-1">
                      <p class="truncate text-sm font-medium text-foreground">{{ membro.nome }}</p>
                      <p class="text-xs text-muted-foreground">{{ membro.partido }} · {{ membro.uf }}</p>
                    </div>
                    <span
                      v-if="membro.cargo"
                      class="rounded-full border border-primary/20 bg-primary/10 px-2 py-0.5 text-[10px] font-semibold text-primary"
                    >
                      {{ membro.cargo }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="comissoesFiltradas.length > displayedCount" class="flex justify-center mt-8">
            <button
              @click="loadMore"
              class="inline-flex items-center gap-2 rounded-lg border border-border bg-background px-6 py-3 text-sm font-medium text-foreground hover:bg-muted"
            >
              Carregar mais
              <ArrowDown class="h-4 w-4" />
            </button>
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

watch([searchQuery, searchMemberQuery], () => {
  displayedCount.value = 15
  selectedComissao.value = null
})

const comissoesFiltradas = computed(() => {
  return comissoes.value.filter(c => {
    const q = searchQuery.value.toLowerCase()
    const matchComissao = !q ||
      (c.nome ?? '').toLowerCase().includes(q) ||
      (c.sigla ?? '').toLowerCase().includes(q)

    const mq = searchMemberQuery.value.toLowerCase()
    const matchMembro = !mq || c.membros.some(m => 
      m.nome.toLowerCase().includes(mq) || 
      m.partido.toLowerCase().includes(mq)
    )
    return matchComissao && matchMembro
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
