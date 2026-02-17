import { defineStore } from "pinia"
import { ref } from "vue"

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

export interface EstatisticasSenado {
    total_gastos_12_meses: number
    total_senadores: number
}

export interface SenadoresFilters {
    search: string
    partido: string
    estado: string
}

export const useSenadoresStore = defineStore("senadores", () => {
    // const apiUrl = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

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
    // const itemsPerPage = 12

    // Detail state
    const currentSenador = ref<SenadorDetail | null>(null)
    const currentDespesas = ref<any[]>([]) // Placeholder for despesas
    const totalDespesas = ref(0)
    const loadingDetail = ref(false)

    // General Stats state
    const generalStats = ref<EstatisticasSenado | null>({
        total_gastos_12_meses: 0,
        total_senadores: 81
    })

    const fetchSenadores = async () => {
        loading.value = true
        error.value = null
        try {
            // Endpoint em breve
            // const response = await fetch(apiUrl + "/api/senadores/")
            senadoresList.value = []
        } catch (e: any) {
            console.error("Erro ao buscar senadores:", e)
            error.value = "Erro ao carregar lista de senadores."
        } finally {
            loading.value = false
        }
    }

    const fetchSenador = async (_id: number) => {
        loadingDetail.value = true
        error.value = null
        currentSenador.value = null
        try {
            // const response = await fetch(`${apiUrl}/api/senadores/${id}`)
        } catch (e: any) {
            console.error("Erro ao buscar detalhes do senador:", e)
        } finally {
            loadingDetail.value = false
        }
    }

    const fetchEstatisticasGerais = async () => {
        loading.value = true
        try {
            // const response = await fetch(`${apiUrl}/api/senadores/estatisticas/geral`)
        } catch (e: any) {
            console.error("Erro ao buscar estatísticas do Senado:", e)
        } finally {
            loading.value = false
        }
    }

    return {
        filters,
        senadoresList,
        loading,
        error,
        currentPage,
        currentSenador,
        currentDespesas,
        totalDespesas,
        loadingDetail,
        generalStats,
        fetchSenadores,
        fetchSenador,
        fetchEstatisticasGerais
    }
})
