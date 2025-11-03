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
      const response = await fetch('http://localhost:8000/api/deputados/')
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
        estado: deputado.uf,
        partido: deputado.sigla_partido || 'S/P',
        // Estes campos não estão sendo usados no perfil, então removidos
        gastoTotal: 0,
        presenca: 0,
        fidelidadePartidaria: 0
      }))
    } catch (err: any) {
      console.error('Erro ao carregar parlamentares:', err)
      error.value = err.message
      parlamentares.value = []
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