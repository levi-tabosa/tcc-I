import { defineStore } from "pinia"
import { ref, computed } from "vue"

export interface Deputado {
  id: number
  nome: string
  partido: string
  estado: string
  foto: string
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

export const useDeputadosStore = defineStore("deputados", () => {
  const filters = ref<Filters>({
    search: "",
    partido: "",
    estado: "",
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
    setFilter,
    setPage,
    resetFilters,
  }
})
