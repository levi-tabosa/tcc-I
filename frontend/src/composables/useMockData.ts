import { ref, onMounted } from 'vue'

interface Parlamentar {
  id: string
  nome: string
  cargo: string
  uf: string
  estado: string
  partido: string
  gastoTotal: number
  presenca: number
  fidelidadePartidaria: number
}

export function useMockData() {
  const parlamentares = ref<Parlamentar[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Lista de partidos brasileiros
  const partidos = [
    'Todos', 'PT', 'PSDB', 'PL', 'PP', 'MDB', 'PSD', 'REPUBLICANOS', 'UNIÃO', 'PSB', 
    'PDT', 'PSOL', 'PODE', 'AVANTE', 'PCdoB', 'CIDADANIA', 'PSC', 'PATRIOTA', 'PROS', 'SOLIDARIEDADE'
  ]

  // Lista de estados brasileiros
  const estados = [
    'Todos', 'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 
    'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
  ]

  // Função para buscar dados reais do backend
  const fetchParlamentares = async () => {
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/deputados/')
      if (!response.ok) {
        throw new Error('Falha ao carregar dados dos parlamentares')
      }
      
      const data = await response.json()
      
      // Transformar os dados do backend para o formato esperado
      parlamentares.value = data.map((deputado: any) => ({
        id: deputado.id.toString(),
        nome: deputado.nome_civil,
        cargo: 'Deputado Federal',
        uf: deputado.uf,
        estado: deputado.uf, // Usar UF como estado por ora
        partido: deputado.sigla_partido || 'S/P',
        // Valores mockados para funcionalidades ainda não implementadas no backend
        gastoTotal: Math.floor(Math.random() * 100000) + 50000,
        presenca: Math.floor(Math.random() * 30) + 70,
        fidelidadePartidaria: Math.floor(Math.random() * 20) + 80
      }))
    } catch (err: any) {
      console.error('Erro ao carregar parlamentares:', err)
      error.value = err.message
      
      // Fallback com dados mockados em caso de erro
      parlamentares.value = [
        {
          id: '1',
          nome: "João Silva",
          cargo: 'Deputado Federal',
          uf: "SP",
          estado: "SP",
          partido: "PT",
          gastoTotal: 85000,
          presenca: 85,
          fidelidadePartidaria: 92
        },
        {
          id: '2',
          nome: "Maria Santos",
          cargo: 'Deputada Federal',
          uf: "RJ",
          estado: "RJ",
          partido: "PSDB",
          gastoTotal: 72000,
          presenca: 78,
          fidelidadePartidaria: 88
        },
        {
          id: '3',
          nome: "Pedro Costa",
          cargo: 'Deputado Federal',
          uf: "MG",
          estado: "MG",
          partido: "PL",
          gastoTotal: 95000,
          presenca: 92,
          fidelidadePartidaria: 85
        },
        {
          id: '4',
          nome: "Ana Oliveira",
          cargo: 'Deputada Federal',
          uf: "RS",
          estado: "RS",
          partido: "PP",
          gastoTotal: 68000,
          presenca: 88,
          fidelidadePartidaria: 94
        },
        {
          id: '5',
          nome: "Carlos Mendes",
          cargo: 'Deputado Federal',
          uf: "BA",
          estado: "BA",
          partido: "MDB",
          gastoTotal: 79000,
          presenca: 82,
          fidelidadePartidaria: 87
        },
        {
          id: '6',
          nome: "Lucia Ferreira",
          cargo: 'Deputada Federal',
          uf: "PR",
          estado: "PR",
          partido: "PSD",
          gastoTotal: 91000,
          presenca: 95,
          fidelidadePartidaria: 89
        }
      ]
    } finally {
      isLoading.value = false
    }
  }

  // Carregar dados automaticamente quando o composable for usado
  onMounted(() => {
    fetchParlamentares()
  })

  return {
    parlamentares,
    partidos,
    estados,
    isLoading,
    error,
    refetch: fetchParlamentares
  }
}