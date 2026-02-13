import { defineStore } from "pinia"
import { ref, computed } from "vue"

export interface Proposicao {
  id: number
  siglaTipo: string
  numero: number
  ano: number
  ementa: string
  dataApresentacao: string | null
  autor_principal: string
}

export interface ProposicoesFilters {
  search: string
  siglaTipo: string
  ano: string
}

export const useProposicoesStore = defineStore("proposicoes", () => {
  const filters = ref<ProposicoesFilters>({
    search: "",
    siglaTipo: "",
    ano: "",
  })

  const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

  // List state
  const proposicoesList = ref<Proposicao[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const hasMore = ref(true)

  const fetchProposicoes = async (pagina = 1) => {
    loading.value = true
    error.value = null

    try {
      const params = new URLSearchParams()
      params.append("pagina", String(pagina))

      if (filters.value.siglaTipo) {
        params.append("siglaTipo", filters.value.siglaTipo)
      }
      if (filters.value.ano) {
        params.append("ano", filters.value.ano)
      }
      if (filters.value.search) {
        params.append("ementa", filters.value.search)
      }

      const response = await fetch(`${apiUrl}/api/deputados/proposicoes?${params.toString()}`)
      if (!response.ok) throw new Error("Falha ao buscar proposições")

      const data: Proposicao[] = await response.json()

      if (pagina === 1) {
        proposicoesList.value = data
      } else {
        proposicoesList.value = [...proposicoesList.value, ...data]
      }

      currentPage.value = pagina
      hasMore.value = data.length === 15
    } catch (e: any) {
      console.error("Erro ao buscar proposições:", e)
      error.value = "Erro ao carregar proposições."
    } finally {
      loading.value = false
    }
  }

  const loadMore = async () => {
    if (!loading.value && hasMore.value) {
      await fetchProposicoes(currentPage.value + 1)
    }
  }

  const tiposUnicos = computed(() => {
    const tipos = new Set(proposicoesList.value.map((p) => p.siglaTipo))
    return Array.from(tipos).sort()
  })

  const anosUnicos = computed(() => {
    const anos = new Set(proposicoesList.value.map((p) => p.ano))
    return Array.from(anos).sort((a, b) => b - a)
  })

  const totalProposicoes = computed(() => proposicoesList.value.length)

  const proposicoesPorTipo = computed(() => {
    const contagem: Record<string, number> = {}
    proposicoesList.value.forEach((p) => {
      contagem[p.siglaTipo] = (contagem[p.siglaTipo] || 0) + 1
    })
    return Object.entries(contagem)
      .map(([tipo, quantidade]) => ({ tipo, quantidade }))
      .sort((a, b) => b.quantidade - a.quantidade)
  })

  const setFilter = (key: keyof ProposicoesFilters, value: string) => {
    filters.value[key] = value
    fetchProposicoes(1)
  }

  const resetFilters = () => {
    filters.value = { search: "", siglaTipo: "", ano: "" }
    fetchProposicoes(1)
  }

  return {
    filters,
    proposicoesList,
    loading,
    error,
    currentPage,
    hasMore,
    tiposUnicos,
    anosUnicos,
    totalProposicoes,
    proposicoesPorTipo,
    fetchProposicoes,
    loadMore,
    setFilter,
    resetFilters,
  }
})
