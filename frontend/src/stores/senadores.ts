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

export interface ProjetoLegislativoSenado {
    id: number
    siglaTipo: string
    numero: number
    ano: number
    ementa: string
    dataApresentacao: string | null
    autor_principal: string
}

export interface ProjetosLegislativosSenadoFilters {
    search: string
    siglaTipo: string
    ano: string
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

    // Projetos Legislativos state
    const projetosLegislativosFilters = ref<ProjetosLegislativosSenadoFilters>({
        search: "",
        siglaTipo: "",
        ano: "",
    })
    const projetosLegislativosList = ref<ProjetoLegislativoSenado[]>([])
    const loadingProjetosLegislativos = ref(false)

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

    // ========== Projetos Legislativos Mock Data ==========
    const mockProjetosLegislativosSenado: ProjetoLegislativoSenado[] = [
        { id: 1001, siglaTipo: "PLS", numero: 123, ano: 2024, ementa: "Dispõe sobre a regulamentação do uso de inteligência artificial em processos judiciais.", dataApresentacao: "2024-03-15", autor_principal: "Senador Rodrigo Pacheco" },
        { id: 1002, siglaTipo: "PEC", numero: 45, ano: 2023, ementa: "Altera dispositivos da Constituição Federal para estabelecer piso salarial nacional para enfermeiros.", dataApresentacao: "2023-06-20", autor_principal: "Senadora Simone Tebet" },
        { id: 1003, siglaTipo: "PLS", numero: 567, ano: 2024, ementa: "Institui o Programa Nacional de Combate ao Desperdício de Alimentos.", dataApresentacao: "2024-05-10", autor_principal: "Senador Flávio Dino" },
        { id: 1004, siglaTipo: "PLC", numero: 89, ano: 2023, ementa: "Regulamenta o teletrabalho no serviço público federal, estabelecendo diretrizes para sua implementação.", dataApresentacao: "2023-09-01", autor_principal: "Senadora Eliziane Gama" },
        { id: 1005, siglaTipo: "MPV", numero: 1200, ano: 2024, ementa: "Abre crédito extraordinário em favor do Ministério da Integração e do Desenvolvimento Regional.", dataApresentacao: "2024-01-22", autor_principal: "Poder Executivo" },
        { id: 1006, siglaTipo: "PEC", numero: 12, ano: 2024, ementa: "Propõe a redução da jornada de trabalho semanal de 44 para 36 horas sem redução de salário.", dataApresentacao: "2024-02-14", autor_principal: "Senador Randolfe Rodrigues" },
        { id: 1007, siglaTipo: "PLS", numero: 890, ano: 2023, ementa: "Estabelece normas gerais para a proteção de dados pessoais de crianças e adolescentes.", dataApresentacao: "2023-11-05", autor_principal: "Senador Eduardo Braga" },
        { id: 1008, siglaTipo: "PLC", numero: 234, ano: 2024, ementa: "Altera a Lei de Diretrizes e Bases da Educação para incluir educação financeira no currículo escolar.", dataApresentacao: "2024-04-18", autor_principal: "Senadora Soraya Thronicke" },
        { id: 1009, siglaTipo: "REQ", numero: 456, ano: 2024, ementa: "Requer a realização de audiência pública para debater a reforma tributária.", dataApresentacao: "2024-03-28", autor_principal: "Senador Omar Aziz" },
        { id: 1010, siglaTipo: "PLS", numero: 321, ano: 2023, ementa: "Dispõe sobre incentivos fiscais para empresas que investirem em energia renovável.", dataApresentacao: "2023-08-12", autor_principal: "Senador Jaques Wagner" },
        { id: 1011, siglaTipo: "MPV", numero: 1185, ano: 2023, ementa: "Institui o Programa de Aceleração da Transição Energética e estabelece o marco regulatório do hidrogênio verde.", dataApresentacao: "2023-07-15", autor_principal: "Poder Executivo" },
        { id: 1012, siglaTipo: "PEC", numero: 8, ano: 2023, ementa: "Altera o art. 5º da Constituição Federal para incluir a proteção de dados pessoais como direito fundamental.", dataApresentacao: "2023-04-10", autor_principal: "Senador Alessandro Vieira" },
        { id: 1013, siglaTipo: "PLS", numero: 742, ano: 2024, ementa: "Cria o Fundo Nacional de Segurança Cibernética para proteção de infraestruturas críticas.", dataApresentacao: "2024-06-05", autor_principal: "Senador Marcos Rogério" },
        { id: 1014, siglaTipo: "REQ", numero: 102, ano: 2023, ementa: "Requer a convocação do Ministro da Fazenda para prestar esclarecimentos sobre a política fiscal.", dataApresentacao: "2023-10-20", autor_principal: "Senador Rogério Marinho" },
        { id: 1015, siglaTipo: "PLC", numero: 55, ano: 2024, ementa: "Regulamenta o mercado de créditos de carbono no Brasil.", dataApresentacao: "2024-07-01", autor_principal: "Senadora Leila Barros" },
    ]

    const loadMockProjetosLegislativos = () => {
        loadingProjetosLegislativos.value = true
        // Simulate async loading
        setTimeout(() => {
            projetosLegislativosList.value = mockProjetosLegislativosSenado
            loadingProjetosLegislativos.value = false
        }, 300)
    }

    const filteredProjetosLegislativos = computed(() => {
        return projetosLegislativosList.value.filter((p) => {
            if (projetosLegislativosFilters.value.search && !p.ementa.toLowerCase().includes(projetosLegislativosFilters.value.search.toLowerCase())) {
                return false
            }
            if (projetosLegislativosFilters.value.siglaTipo && p.siglaTipo !== projetosLegislativosFilters.value.siglaTipo) {
                return false
            }
            if (projetosLegislativosFilters.value.ano && p.ano !== Number(projetosLegislativosFilters.value.ano)) {
                return false
            }
            return true
        })
    })

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
        filteredProjetosLegislativos.value.forEach((p) => {
            contagem[p.siglaTipo] = (contagem[p.siglaTipo] || 0) + 1
        })
        return Object.entries(contagem)
            .map(([tipo, quantidade]) => ({ tipo, quantidade }))
            .sort((a, b) => b.quantidade - a.quantidade)
    })

    const setProjetosLegislativosFilter = (key: keyof ProjetosLegislativosSenadoFilters, value: string) => {
        projetosLegislativosFilters.value[key] = value
    }

    const resetProjetosLegislativosFilters = () => {
        projetosLegislativosFilters.value = { search: "", siglaTipo: "", ano: "" }
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
        resetFilters,
        // Projetos Legislativos
        projetosLegislativosFilters,
        projetosLegislativosList,
        loadingProjetosLegislativos,
        filteredProjetosLegislativos,
        tiposUnicosProjetosLegislativos,
        anosUnicosProjetosLegislativos,
        projetosLegislativosPorTipo,
        loadMockProjetosLegislativos,
        setProjetosLegislativosFilter,
        resetProjetosLegislativosFilters,
    }
})
