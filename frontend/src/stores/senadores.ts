import { defineStore } from "pinia"
import { ref, computed } from "vue"

export interface Senador {
    id: number
    nome: string
    partido: string
    estado: string
    foto: string
}

export interface SenadorDetail {
    id: number
    nome_civil: string
    nome_parlamentar: string
    cpf: string
    sexo: string
    email: string
    data_nascimento: string | null
    escolaridade: string
    uf_nascimento: string
    municipio_nascimento: string
    sigla_partido: string
    uf: string
    foto: string
}

export interface EstatisticasSenadoGerais {
    total_senadores: number
    total_gastos: number
}

export interface EstatisticasSenado {
    total_gastos: number
    media_por_senador: number
    partidos: { partido: string; total: number; percentual: number }[]
    categorias: { categoria: string; total: number }[]
    top_10: { codigo: number; nome: string; partido: string; uf: string; foto: string; total: number }[]
}

export interface SenadoresFilters {
    search: string
    partido: string
    estado: string
}

export const useSenadoresStore = defineStore("senadores", () => {
    const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

    const filters = ref<SenadoresFilters>({
        search: "",
        partido: "",
        estado: "",
    })

    // List state
    const senadoresList = ref<Senador[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)
    const currentPage = ref(1)
    const itemsPerPage = 12

    // Detail state
    const currentSenador = ref<SenadorDetail | null>(null)
    const currentDespesas = ref<any[]>([])
    const currentCategorias = ref<any[]>([])
    const totalDespesas = ref(0)
    const loadingDetail = ref(false)

    // General Stats state
    const generalStats = ref<EstatisticasSenado | null>(null)
    const senadorStats = ref<EstatisticasSenadoGerais | null>(null)

    const fetchSenadores = async () => {
        loading.value = true
        error.value = null
        try {
            const response = await fetch(apiUrl + "/api/senado/lista")
            if (!response.ok) throw new Error("Falha ao buscar senadores")

            const data = await response.json()
            senadoresList.value = data.senadores.map((s: any) => ({
                id: s.codigo,
                nome: s.nomeParlamentar,
                partido: s.siglaPartido,
                estado: s.uf,
                foto: s.urlFoto
            }))
        } catch (e: any) {
            console.error("Erro ao buscar senadores:", e)
            error.value = "Erro ao carregar lista de senadores."
        } finally {
            loading.value = false
        }
    }

    const fetchSenador = async (id: number) => {
        loadingDetail.value = true
        error.value = null
        currentSenador.value = null
        currentDespesas.value = []
        currentCategorias.value = []
        totalDespesas.value = 0
        try {
            const response = await fetch(`${apiUrl}/api/senado/${id}`)
            if (!response.ok) throw new Error("Falha ao buscar detalhes do senador")
            const data = await response.json()
            const s = data.senador
            currentSenador.value = {
                id: s.codigo,
                nome_civil: s.nomeCompleto || s.nomeParlamentar,
                nome_parlamentar: s.nomeParlamentar,
                cpf: "N/A",
                sexo: s.sexo,
                email: s.email,
                data_nascimento: s.dataNascimento,
                escolaridade: "N/A",
                uf_nascimento: "N/A",
                municipio_nascimento: "N/A",
                sigla_partido: s.siglaPartido,
                uf: s.uf,
                foto: s.urlFoto
            }

            // Buscar despesas logo após
            await fetchDespesasSenador(id)
        } catch (e: any) {
            console.error("Erro ao buscar detalhes do senador:", e)
            error.value = "Erro ao carregar perfil do senador."
        } finally {
            loadingDetail.value = false
        }
    }

    const fetchDespesasSenador = async (id: number) => {
        loadingDetail.value = true
        try {
            const response = await fetch(`${apiUrl}/api/senado/${id}/despesas`)
            if (!response.ok) throw new Error("Falha ao buscar despesas do senador")
            const data = await response.json()
            currentDespesas.value = data.despesas
            currentCategorias.value = data.categorias || []
            totalDespesas.value = data.total_despesas
        } catch (e: any) {
            console.error("Erro ao buscar despesas:", e)
        } finally {
            loadingDetail.value = false
        }
    }

    const fetchEstatisticasGerais = async () => {
        try {
            const response = await fetch(`${apiUrl}/api/senado/despesas/estatisticas`)
            if (!response.ok) throw new Error('Falha ao buscar estatísticas do Senado')
            generalStats.value = await response.json()
        } catch (e: any) {
            console.error('Erro ao buscar estatísticas do senado:', e)
        }
    }

    const fetchEstatisticasSenadores = async () => {
        try {
            const response = await fetch(`${apiUrl}/api/senado/estatisticas`)
            if (!response.ok) throw new Error('Falha ao buscar estatísticas gerais do Senado')
            senadorStats.value = await response.json()
        } catch (e: any) {
            console.error('Erro ao buscar estatísticas gerais do senado:', e)
        }
    }

    const partidosUnicos = computed(() => {
        const set = new Set(senadoresList.value.map(s => s.partido).filter(Boolean))
        return Array.from(set).sort()
    })

    const estadosUnicos = computed(() => {
        const set = new Set(senadoresList.value.map(s => s.estado).filter(Boolean))
        return Array.from(set).sort()
    })

    const filteredSenadores = computed(() => {
        return senadoresList.value.filter((sen) => {
            if (filters.value.search && !sen.nome.toLowerCase().includes(filters.value.search.toLowerCase())) {
                return false
            }
            if (filters.value.partido && sen.partido !== filters.value.partido) {
                return false
            }
            if (filters.value.estado && sen.estado !== filters.value.estado) {
                return false
            }
            return true
        })
    })

    const totalPages = computed(() => Math.ceil(filteredSenadores.value.length / itemsPerPage))

    const paginatedSenadores = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage
        return filteredSenadores.value.slice(start, start + itemsPerPage)
    })

    const setFilter = (key: keyof SenadoresFilters, value: string) => {
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
        senadoresList,
        filteredSenadores,
        paginatedSenadores,
        partidosUnicos,
        estadosUnicos,
        totalPages,
        currentPage,
        loading,
        error,
        currentSenador,
        currentDespesas,
        currentCategorias,
        totalDespesas,
        loadingDetail,
        generalStats,
        senadorStats,
        fetchSenadores,
        fetchSenador,
        fetchDespesasSenador,
        fetchEstatisticasGerais,
        fetchEstatisticasSenadores,
        setFilter,
        setPage,
        resetFilters
    }
})
