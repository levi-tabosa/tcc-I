import { defineStore } from "pinia"
import { ref, computed } from "vue"

export interface Deputado {
  id: number
  nome: string
  partido: string
  estado: string
  foto: string
}

export interface ProjetoLegislativo {
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
  categorias?: { categoria: string; valor: number }[]
  despesas?: Despesa[]
  total_gasto?: number
  total_emendas?: number
}

export interface Emenda {
  codigo: string
  ano: number
  tipo: string
  valorEmpenhado: number
  valorLiquidado: number
  valorPago: number
  funcao: string
  localidade: string
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
  total_empresas_contratadas: number
  gastos_por_categoria: { categoria: string; valor: number }[]
  gastos_por_mes: { ano: number; mes: number; valor: number }[]
  gastos_por_estado: { estado: string; valor: number }[]
  gastos_por_partido: { partido: string; valor: number }[]
  gastos_deputados: {
    deputado_id: number
    nome_civil: string
    sigla_partido: string
    estado: string
    total_gasto: number
  }[]
}

export interface EstatisticasDeputado {
  total_deputados: number
  deputados_por_regiao: { name: string; value: number }[]
}

export interface Filters {
  search: string
  partido: string
  estado: string
}

export interface ProjetosLegislativosFilters {
  search: string
  siglaTipo: string
  ano: string
  deputado: string
}

export interface VotoDeputado {
  deputado_id: number
  nome: string
  voto: string
}

export interface Votacao {
  id_votacao: string
  data: string
  descricao: string
  total_votos: number
  lista_votos: VotoDeputado[]
}

export interface VotosProjetoLegislativo {
  proposicao_id: number
  historico_votacoes: Votacao[]
}

export const useDeputadosStore = defineStore("deputados", () => {
  const filters = ref<Filters>({
    search: "",
    partido: "",
    estado: "",
  })

  const projetosLegislativosFilters = ref<ProjetosLegislativosFilters>({
    search: "",
    siglaTipo: "",
    ano: "",
    deputado: "",
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
  const currentCategorias = ref<Categoria[]>([])
  const totalDespesas = ref(0)
  const currentEmendas = ref<Emenda[]>([])
  const totalEmendas = ref(0)
  const loadingDetail = ref(false)

  // General Stats state
  const generalStats = ref<EstatisticasGerais | null>(null)
  const deputadoStats = ref<EstatisticasDeputado | null>(null)

  // Categories state
  const categorias = ref<Categoria[]>([])
  const loadingCategorias = ref(false)

  // Projetos Legislativos state
  const projetosLegislativosList = ref<ProjetoLegislativo[]>([])
  const loadingProjetosLegislativos = ref(false)
  const projetosLegislativosPage = ref(1)
  const hasMoreProjetosLegislativos = ref(true)

  // Votos state
  const currentVotos = ref<VotosProjetoLegislativo | null>(null)
  const loadingVotos = ref(false)
  const selectedProjetoLegislativoId = ref<number | null>(null)

  const fetchDeputados = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await fetch(apiUrl + "/api/deputados/lista")
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

      const data = await response.json()
      currentDeputado.value = data
      currentDespesas.value = data.despesas || []
      currentCategorias.value = data.categorias || []
      totalDespesas.value = data.total_despesas || 0
      totalEmendas.value = data.total_emendas || 0
      
      // Also fetch the full list of emendas
      await fetchEmendasDeputado(id)
    } catch (e: any) {
      console.error("Erro ao buscar detalhes:", e)
      error.value = "Erro ao carregar detalhes do deputado."
    } finally {
      loadingDetail.value = false
    }
  }


  const fetchEstatisticasGerais = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/deputados/despesas/estatisticas`)
      if (!response.ok) throw new Error("Falha ao buscar estatísticas de despesas")
      generalStats.value = await response.json()
    } catch (e: any) {
      console.error("Erro ao buscar estatísticas gerais de despesas:", e)
    }
  }

  const fetchEstatisticasDeputados = async () => {
    try {
      const response = await fetch(`${apiUrl}/api/deputados/estatisticas`)
      if (!response.ok) throw new Error("Falha ao buscar estatísticas de deputados")
      deputadoStats.value = await response.json()
    } catch (e: any) {
      console.error("Erro ao buscar estatísticas gerais de deputados:", e)
    }
  }


  const fetchProjetosLegislativos = async (pagina = 1) => {
    loadingProjetosLegislativos.value = true
    error.value = null

    try {
      const params = new URLSearchParams()
      params.append("pagina", String(pagina))

      if (projetosLegislativosFilters.value.siglaTipo) {
        params.append("siglaTipo", projetosLegislativosFilters.value.siglaTipo)
      }
      if (projetosLegislativosFilters.value.ano) {
        params.append("ano", projetosLegislativosFilters.value.ano)
      }
      if (projetosLegislativosFilters.value.search) {
        params.append("ementa", projetosLegislativosFilters.value.search)
      }
      if (projetosLegislativosFilters.value.deputado) {
        params.append("deputado", projetosLegislativosFilters.value.deputado)
      }

      const response = await fetch(`${apiUrl}/api/deputados/proposicoes?${params.toString()}`)
      if (!response.ok) throw new Error("Falha ao buscar projetos legislativos")

      const data: ProjetoLegislativo[] = await response.json()

      if (pagina === 1) {
        projetosLegislativosList.value = data
      } else {
        projetosLegislativosList.value = [...projetosLegislativosList.value, ...data]
      }

      projetosLegislativosPage.value = pagina
      hasMoreProjetosLegislativos.value = data.length === 15
    } catch (e: any) {
      console.error("Erro ao buscar projetos legislativos:", e)
      error.value = "Erro ao carregar projetos legislativos."
    } finally {
      loadingProjetosLegislativos.value = false
    }
  }

  const loadMoreProjetosLegislativos = async () => {
    if (!loadingProjetosLegislativos.value && hasMoreProjetosLegislativos.value) {
      await fetchProjetosLegislativos(projetosLegislativosPage.value + 1)
    }
  }

  const tiposUnicosProjetosLegislativos = computed(() => {
    const tipos = new Set(projetosLegislativosList.value.map((p) => p.siglaTipo))
    return Array.from(tipos).sort()
  })

  const anosUnicosProjetosLegislativos = computed(() => {
    const anos = new Set(projetosLegislativosList.value.map((p) => p.ano))
    return Array.from(anos).sort((a, b) => b - a)
  })

  const projetosLegislativosPorTipo = computed(() => {
    const contagem: Record<string, number> = {}
    projetosLegislativosList.value.forEach((p) => {
      contagem[p.siglaTipo] = (contagem[p.siglaTipo] || 0) + 1
    })
    return Object.entries(contagem)
      .map(([tipo, quantidade]) => ({ tipo, quantidade }))
      .sort((a, b) => b.quantidade - a.quantidade)
  })

  const fetchVotosProjetoLegislativo = async (id: number) => {
    loadingVotos.value = true
    currentVotos.value = null
    try {
      const response = await fetch(`${apiUrl}/api/deputados/proposicoes/${id}/votos`)
      if (!response.ok) throw new Error("Falha ao buscar votos")
      currentVotos.value = await response.json()
    } catch (e: any) {
      console.error("Erro ao buscar votos do projeto legislativo:", e)
    } finally {
      loadingVotos.value = false
    }
  }

  const fetchEmendasDeputado = async (id: number) => {
    try {
      const response = await fetch(`${apiUrl}/api/deputados/${id}/emendas`)
      if (!response.ok) throw new Error("Falha ao buscar emendas")
      currentEmendas.value = await response.json()
    } catch (e: any) {
      console.error("Erro ao buscar emendas do deputado:", e)
    }
  }

  const toggleProjetoLegislativoVotos = async (id: number) => {
    if (selectedProjetoLegislativoId.value === id) {
      selectedProjetoLegislativoId.value = null
      currentVotos.value = null
    } else {
      selectedProjetoLegislativoId.value = id
      await fetchVotosProjetoLegislativo(id)
    }
  }

  const setProjetosLegislativosFilter = (key: keyof ProjetosLegislativosFilters, value: string) => {
    projetosLegislativosFilters.value[key] = value
    fetchProjetosLegislativos(1)
  }

  const resetProjetosLegislativosFilters = () => {
    projetosLegislativosFilters.value = { search: "", siglaTipo: "", ano: "", deputado: "" }
    fetchProjetosLegislativos(1)
  }

  const partidosUnicos = computed(() => {
    const set = new Set(deputadosList.value.map(d => d.partido))
    return Array.from(set).sort()
  })

  const estadosUnicos = computed(() => {
    const set = new Set(deputadosList.value.map(d => d.estado))
    return Array.from(set).sort()
  })

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
    partidosUnicos,
    estadosUnicos,
    deputadosList,
    filteredDeputados,
    paginatedDeputados,
    totalPages,
    loading,
    error,
    currentDeputado,
    currentDespesas,
    currentCategorias,
    totalDespesas,
    currentEmendas,
    totalEmendas,
    loadingDetail,
    generalStats,
    deputadoStats,
    categorias,
    loadingCategorias,
    fetchDeputados,
    fetchDeputado,
    fetchEstatisticasGerais,
    fetchEstatisticasDeputados,
    projetosLegislativosList,
    loadingProjetosLegislativos,
    projetosLegislativosPage,
    hasMoreProjetosLegislativos,
    projetosLegislativosFilters,
    fetchProjetosLegislativos,
    loadMoreProjetosLegislativos,
    tiposUnicosProjetosLegislativos,
    anosUnicosProjetosLegislativos,
    projetosLegislativosPorTipo,
    setProjetosLegislativosFilter,
    resetProjetosLegislativosFilters,
    currentVotos,
    loadingVotos,
    selectedProjetoLegislativoId,
    fetchVotosProjetoLegislativo,
    toggleProjetoLegislativoVotos,
    setFilter,
    setPage,
    resetFilters,
  }
})
