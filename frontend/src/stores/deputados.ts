import { defineStore } from "pinia"
import { ref, computed } from "vue"

export interface Deputado {
  id: number
  nome: string
  partido: string
  estado: string
  foto: string
}

export interface Proposicao {
  id: number
  siglaTipo: string
  numero: number
  ano: number
  ementa: string
  dataApresentacao: string | null
  autor_principal: string
}

export interface DeputadoDetail {
  id: number
  nome_civil: string
  cpf: string
  sexo: string
  email: string
  data_nascimento: string | null
  escolaridade: string
  uf_nascimento: string
  municipio_nascimento: string
  sigla_partido: string
  foto: string
}

export interface Despesa {
  ano: number
  mes: number
  tipo_despesa: string
  valor: number
  url_documento: string | null
}

export interface Categoria {
  categoria: string
  valor: number
}

export interface EstatisticasGerais {
  total_gastos_12_meses: number
  total_gastos: number
  total_deputados: number
  total_empresas_contratadas: number
  gastos_por_categoria: { categoria: string; valor: number }[]
  gastos_por_mes: { ano: number; mes: number; valor: number }[]
  gastos_por_estado: { estado: string; valor: number }[]
  gastos_por_partido: { partido: string; valor: number }[]
  deputados_por_regiao: { name: string; value: number }[]
}

export interface Filters {
  search: string
  partido: string
  estado: string
}

export interface ProposicoesFilters {
  search: string
  siglaTipo: string
  ano: string
}

export const useDeputadosStore = defineStore("deputados", () => {
  const filters = ref<Filters>({
    search: "",
    partido: "",
    estado: "",
  })

  const proposicoesFilters = ref<ProposicoesFilters>({
    search: "",
    siglaTipo: "",
    ano: "",
  })

  const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

  // List state
  const deputadosList = ref<Deputado[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const currentPage = ref(1)
  const itemsPerPage = 12

  // Detail state
  const currentDeputado = ref<DeputadoDetail | null>(null)
  const currentDespesas = ref<Despesa[]>([])
  const totalDespesas = ref(0)
  const loadingDetail = ref(false)

  // General Stats state
  const generalStats = ref<EstatisticasGerais | null>(null)

  // Categories state
  const categorias = ref<Categoria[]>([])
  const loadingCategorias = ref(false)

  // Propositions state
  const proposicoesList = ref<Proposicao[]>([])
  const loadingProposicoes = ref(false)
  const proposicoesPage = ref(1)
  const hasMoreProposicoes = ref(true)

  const fetchDeputados = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(apiUrl + "/api/deputados/")
      if (!response.ok) throw new Error("Falha ao buscar deputados")

      const data = await response.json()
      deputadosList.value = data.map((d: any) => ({
        id: d.id,
        nome: d.nome_civil,
        partido: d.sigla_partido,
        estado: d.uf,
        foto: `https://www.camara.leg.br/internet/deputado/bandep/${d.id}.jpg`
      }))
    } catch (e: any) {
      console.error("Erro ao buscar deputados:", e)
      error.value = "Erro ao carregar lista de deputados."
    } finally {
      loading.value = false
    }
  }

  const fetchDeputado = async (id: number) => {
    loadingDetail.value = true
    error.value = null
    currentDeputado.value = null
    currentDespesas.value = []
    totalDespesas.value = 0

    try {
      const response = await fetch(`${apiUrl}/api/deputados/${id}`)
      if (!response.ok) throw new Error("Falha ao buscar detalhes do deputado")
      currentDeputado.value = await response.json()

      // Also fetch expenses
      await fetchDespesas(id)
    } catch (e: any) {
      console.error("Erro ao buscar detalhes:", e)
      error.value = "Erro ao carregar detalhes do deputado."
    } finally {
      loadingDetail.value = false
    }
  }

  const fetchDespesas = async (id: number) => {
    try {
      const response = await fetch(`${apiUrl}/api/deputados/${id}/despesas`)
      if (!response.ok) throw new Error("Falha ao buscar despesas")
      const data = await response.json()
      currentDespesas.value = data.despesas
      totalDespesas.value = data.total_despesas || 0
    } catch (e: any) {
      console.error("Erro ao buscar despesas:", e)
    }
  }

  const fetchEstatisticasGerais = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/deputados/estatisticas/geral`)
      if (!response.ok) throw new Error("Falha ao buscar estatísticas")
      generalStats.value = await response.json()
    } catch (e: any) {
      console.error("Erro ao buscar estatísticas gerais:", e)
    }
  }

  const fetchCategorias = async () => {
    loadingCategorias.value = true
    try {
      const response = await fetch(`${apiUrl}/api/deputados/estatisticas/categorias`)
      if (!response.ok) throw new Error("Falha ao buscar categorias")
      categorias.value = await response.json()
    } catch (e: any) {
      console.error("Erro ao buscar categorias:", e)
    } finally {
      loadingCategorias.value = false
    }
  }

  const fetchProposicoes = async (pagina = 1) => {
    loadingProposicoes.value = true
    error.value = null

    try {
      const params = new URLSearchParams()
      params.append("pagina", String(pagina))

      if (proposicoesFilters.value.siglaTipo) {
        params.append("siglaTipo", proposicoesFilters.value.siglaTipo)
      }
      if (proposicoesFilters.value.ano) {
        params.append("ano", proposicoesFilters.value.ano)
      }
      if (proposicoesFilters.value.search) {
        params.append("ementa", proposicoesFilters.value.search)
      }

      const response = await fetch(`${apiUrl}/api/deputados/proposicoes?${params.toString()}`)
      if (!response.ok) throw new Error("Falha ao buscar proposições")

      const data: Proposicao[] = await response.json()

      if (pagina === 1) {
        proposicoesList.value = data
      } else {
        proposicoesList.value = [...proposicoesList.value, ...data]
      }

      proposicoesPage.value = pagina
      hasMoreProposicoes.value = data.length === 15
    } catch (e: any) {
      console.error("Erro ao buscar proposições:", e)
      error.value = "Erro ao carregar proposições."
    } finally {
      loadingProposicoes.value = false
    }
  }

  const loadMoreProposicoes = async () => {
    if (!loadingProposicoes.value && hasMoreProposicoes.value) {
      await fetchProposicoes(proposicoesPage.value + 1)
    }
  }

  const tiposUnicosProposicoes = computed(() => {
    const tipos = new Set(proposicoesList.value.map((p) => p.siglaTipo))
    return Array.from(tipos).sort()
  })

  const anosUnicosProposicoes = computed(() => {
    const anos = new Set(proposicoesList.value.map((p) => p.ano))
    return Array.from(anos).sort((a, b) => b - a)
  })

  const proposicoesPorTipo = computed(() => {
    const contagem: Record<string, number> = {}
    proposicoesList.value.forEach((p) => {
      contagem[p.siglaTipo] = (contagem[p.siglaTipo] || 0) + 1
    })
    return Object.entries(contagem)
      .map(([tipo, quantidade]) => ({ tipo, quantidade }))
      .sort((a, b) => b.quantidade - a.quantidade)
  })

  const setProposicoesFilter = (key: keyof ProposicoesFilters, value: string) => {
    proposicoesFilters.value[key] = value
    fetchProposicoes(1)
  }

  const resetProposicoesFilters = () => {
    proposicoesFilters.value = { search: "", siglaTipo: "", ano: "" }
    fetchProposicoes(1)
  }

  const filteredDeputados = computed(() => {
    return deputadosList.value.filter((dep) => {
      if (filters.value.search && !dep.nome.toLowerCase().includes(filters.value.search.toLowerCase())) {
        return false
      }
      if (filters.value.partido && dep.partido !== filters.value.partido) {
        return false
      }
      if (filters.value.estado && dep.estado !== filters.value.estado) {
        return false
      }
      return true
    })
  })

  const totalPages = computed(() => Math.ceil(filteredDeputados.value.length / itemsPerPage))

  const paginatedDeputados = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    return filteredDeputados.value.slice(start, start + itemsPerPage)
  })

  const setFilter = (key: keyof Filters, value: string) => {
    filters.value[key] = value
    currentPage.value = 1
  }

  const setPage = (page: number) => {
    currentPage.value = page
  }

  const resetFilters = () => {
    filters.value = { search: "", partido: "", estado: "" }
    currentPage.value = 1
  }

  return {
    filters,
    currentPage,
    filteredDeputados,
    paginatedDeputados,
    totalPages,
    loading,
    error,
    currentDeputado,
    currentDespesas,
    totalDespesas,
    loadingDetail,
    generalStats,
    categorias,
    loadingCategorias,
    fetchDeputados,
    fetchDeputado,
    fetchEstatisticasGerais,
    fetchCategorias,
    proposicoesList,
    loadingProposicoes,
    proposicoesPage,
    hasMoreProposicoes,
    proposicoesFilters,
    fetchProposicoes,
    loadMoreProposicoes,
    tiposUnicosProposicoes,
    anosUnicosProposicoes,
    proposicoesPorTipo,
    setProposicoesFilter,
    resetProposicoesFilters,
    setFilter,
    setPage,
    resetFilters,
  }
})
