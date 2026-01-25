export interface Deputado {
  id: number
  nome: string
  nomeCompleto: string
  partido: string
  estado: string
  foto: string
  email: string
  telefone: string
  gastoTotal: number
  emendasTotal: number
  blocoIdeologico: "direita" | "esquerda" | "centro"
  auxilioMoradia: boolean
  valorAuxilio: number
}

export interface Empresa {
  id: number
  nome: string
  cnpj: string
  valorTotal: number
  contratos: number
  partidosPrincipais: string[]
}


export const partidos = [
  { sigla: "PL", nome: "Partido Liberal", deputados: 99, bloco: "direita" as const },
  { sigla: "PT", nome: "Partido dos Trabalhadores", deputados: 68, bloco: "esquerda" as const },
  { sigla: "UNIÃO", nome: "União Brasil", deputados: 59, bloco: "centro" as const },
  { sigla: "PP", nome: "Progressistas", deputados: 50, bloco: "centro" as const },
  { sigla: "MDB", nome: "Movimento Democrático Brasileiro", deputados: 42, bloco: "centro" as const },
  { sigla: "PSD", nome: "Partido Social Democrático", deputados: 42, bloco: "centro" as const },
  { sigla: "REPUBLICANOS", nome: "Republicanos", deputados: 41, bloco: "direita" as const },
  { sigla: "PDT", nome: "Partido Democrático Trabalhista", deputados: 17, bloco: "esquerda" as const },
  { sigla: "PSDB", nome: "Partido da Social Democracia Brasileira", deputados: 13, bloco: "centro" as const },
  { sigla: "PSB", nome: "Partido Socialista Brasileiro", deputados: 14, bloco: "esquerda" as const },
  { sigla: "PSOL", nome: "Partido Socialismo e Liberdade", deputados: 12, bloco: "esquerda" as const },
  { sigla: "PODE", nome: "Podemos", deputados: 12, bloco: "centro" as const },
  { sigla: "NOVO", nome: "Partido Novo", deputados: 3, bloco: "direita" as const },
  { sigla: "PCdoB", nome: "Partido Comunista do Brasil", deputados: 6, bloco: "esquerda" as const },
  { sigla: "PV", nome: "Partido Verde", deputados: 4, bloco: "esquerda" as const },
  { sigla: "AVANTE", nome: "Avante", deputados: 7, bloco: "centro" as const },
  { sigla: "SOLIDARIEDADE", nome: "Solidariedade", deputados: 6, bloco: "centro" as const },
  { sigla: "CIDADANIA", nome: "Cidadania", deputados: 5, bloco: "centro" as const },
  { sigla: "REDE", nome: "Rede Sustentabilidade", deputados: 2, bloco: "esquerda" as const },
]

export const estados = [
  { sigla: "SP", nome: "São Paulo", deputados: 70, regiao: "Sudeste" },
  { sigla: "MG", nome: "Minas Gerais", deputados: 53, regiao: "Sudeste" },
  { sigla: "RJ", nome: "Rio de Janeiro", deputados: 46, regiao: "Sudeste" },
  { sigla: "BA", nome: "Bahia", deputados: 39, regiao: "Nordeste" },
  { sigla: "RS", nome: "Rio Grande do Sul", deputados: 31, regiao: "Sul" },
  { sigla: "PR", nome: "Paraná", deputados: 30, regiao: "Sul" },
  { sigla: "PE", nome: "Pernambuco", deputados: 25, regiao: "Nordeste" },
  { sigla: "CE", nome: "Ceará", deputados: 22, regiao: "Nordeste" },
  { sigla: "MA", nome: "Maranhão", deputados: 18, regiao: "Nordeste" },
  { sigla: "GO", nome: "Goiás", deputados: 17, regiao: "Centro-Oeste" },
  { sigla: "PA", nome: "Pará", deputados: 17, regiao: "Norte" },
  { sigla: "SC", nome: "Santa Catarina", deputados: 16, regiao: "Sul" },
  { sigla: "PB", nome: "Paraíba", deputados: 12, regiao: "Nordeste" },
  { sigla: "PI", nome: "Piauí", deputados: 10, regiao: "Nordeste" },
  { sigla: "AL", nome: "Alagoas", deputados: 9, regiao: "Nordeste" },
  { sigla: "RN", nome: "Rio Grande do Norte", deputados: 8, regiao: "Nordeste" },
  { sigla: "AM", nome: "Amazonas", deputados: 8, regiao: "Norte" },
  { sigla: "MT", nome: "Mato Grosso", deputados: 8, regiao: "Centro-Oeste" },
  { sigla: "MS", nome: "Mato Grosso do Sul", deputados: 8, regiao: "Centro-Oeste" },
  { sigla: "ES", nome: "Espírito Santo", deputados: 10, regiao: "Sudeste" },
  { sigla: "SE", nome: "Sergipe", deputados: 8, regiao: "Nordeste" },
  { sigla: "DF", nome: "Distrito Federal", deputados: 8, regiao: "Centro-Oeste" },
  { sigla: "RO", nome: "Rondônia", deputados: 8, regiao: "Norte" },
  { sigla: "TO", nome: "Tocantins", deputados: 8, regiao: "Norte" },
  { sigla: "AC", nome: "Acre", deputados: 8, regiao: "Norte" },
  { sigla: "AP", nome: "Amapá", deputados: 8, regiao: "Norte" },
  { sigla: "RR", nome: "Roraima", deputados: 8, regiao: "Norte" },
]

const nomes = [
  "Pastor Sargento Isidório",
  "Carla Zambelli",
  "Nikolas Ferreira",
  "Guilherme Boulos",
  "Eduardo Bolsonaro",
  "Kim Kataguiri",
  "Tabata Amaral",
  "Marina Silva",
  "Marco Feliciano",
  "Alexandre Frota",
  "Joice Hasselmann",
  "Marcel van Hattem",
  "Gleisi Hoffmann",
  "Paulo Pimenta",
  "Jorge Solla",
  "Erika Hilton",
  "Sâmia Bomfim",
  "Fernanda Melchionna",
  "Talíria Petrone",
  "Luiza Erundina",
  "Ricardo Barros",
  "Arthur Lira",
  "Hugo Motta",
  "Ciro Nogueira",
  "Valdemar Costa Neto",
  "Marcos Pereira",
  "Baleia Rossi",
  "Elmar Nascimento",
  "Celso Sabino",
  "Luciano Bivar",
  "Paulinho da Força",
  "Renildo Calheiros",
]

export const deputados: Deputado[] = Array.from({ length: 100 }, (_, i) => {
  const partido = partidos[Math.floor(Math.random() * partidos.length)]
  const estado = estados[Math.floor(Math.random() * estados.length)]
  const nome = nomes[i % nomes.length] + (i >= nomes.length ? ` ${Math.floor(i / nomes.length) + 1}` : "")

  return {
    id: i + 1,
    nome,
    nomeCompleto: nome,
    partido: partido.sigla,
    estado: estado.sigla,
    foto: `/placeholder-user.jpg`,
    email: `dep.${nome.toLowerCase().replace(/ /g, ".")}@camara.leg.br`,
    telefone: `(61) 3215-${String(1000 + i).padStart(4, "0")}`,
    gastoTotal: Math.floor(Math.random() * 500000) + 100000,
    emendasTotal: Math.floor(Math.random() * 20000000) + 1000000,
    blocoIdeologico: partido.bloco,
    auxilioMoradia: Math.random() > 0.7,
    valorAuxilio: 4253,
  }
})

export const categoriasDespesas = [
  { nome: "Divulgação de Atividade Parlamentar", total: 127000000 },
  { nome: "Passagens Aéreas", total: 98000000 },
  { nome: "Consultorias e Assessorias", total: 87000000 },
  { nome: "Combustíveis e Lubrificantes", total: 45000000 },
  { nome: "Telefonia e Internet", total: 32000000 },
  { nome: "Alimentação", total: 28000000 },
  { nome: "Hospedagem", total: 25000000 },
  { nome: "Locação de Veículos", total: 22000000 },
  { nome: "Serviços Postais", total: 18000000 },
  { nome: "Outros", total: 15000000 },
]

export const areasEmendas = [
  { nome: "Segurança Pública", percentual: 12.3, valor: 159900000 },
  { nome: "Saúde", percentual: 25.8, valor: 335400000 },
  { nome: "Educação", percentual: 18.5, valor: 240500000 },
  { nome: "Infraestrutura", percentual: 15.2, valor: 197600000 },
  { nome: "Assistência Social", percentual: 10.7, valor: 139100000 },
  { nome: "Agricultura", percentual: 8.3, valor: 107900000 },
  { nome: "Cultura", percentual: 4.2, valor: 54600000 },
  { nome: "Esporte", percentual: 3.1, valor: 40300000 },
  { nome: "Meio Ambiente", percentual: 1.9, valor: 24700000 },
]

export const statsGerais = {
  totalDeputados: 2010,
  totalEmendas: 1300000000,
  totalGastos: 497000000,
  deputadosComAuxilio: 113,
  valorAuxilioMensal: 4253,
  totalEmpresas: 12847,
  mediaGastoDeputado: 968000,
}

export const gastosPorBloco = [
  { bloco: "Direita", valor: 309000000, cor: "#2563eb" },
  { bloco: "Centro", valor: 189000000, cor: "#ffd700" },
  { bloco: "Esquerda", valor: 149000000, cor: "#dc2626" },
]

export const regioes = [
  { nome: "Sudeste", percentual: 34.9, deputados: 179 },
  { nome: "Nordeste", percentual: 29.6, deputados: 152 },
  { nome: "Sul", percentual: 15.0, deputados: 77 },
  { nome: "Norte", percentual: 12.9, deputados: 66 },
  { nome: "Centro-Oeste", percentual: 7.6, deputados: 39 },
]

export const topEmpresas: Empresa[] = [
  {
    id: 1,
    nome: "TAM Linhas Aéreas S.A.",
    cnpj: "02.012.862/0001-60",
    valorTotal: 59000000,
    contratos: 8234,
    partidosPrincipais: ["PL", "PT", "UNIÃO"]
  },
  {
    id: 2,
    nome: "GOL Linhas Aéreas Inteligentes S.A.",
    cnpj: "07.575.651/0001-59",
    valorTotal: 47500000,
    contratos: 6892,
    partidosPrincipais: ["PT", "MDB", "PP"]
  },
  {
    id: 3,
    nome: "Azul Linhas Aéreas Brasileiras S.A.",
    cnpj: "09.296.295/0001-60",
    valorTotal: 38200000,
    contratos: 5421,
    partidosPrincipais: ["UNIÃO", "PSD", "REPUBLICANOS"]
  },
  {
    id: 4,
    nome: "Petrobras Distribuidora S.A.",
    cnpj: "34.274.233/0001-02",
    valorTotal: 35800000,
    contratos: 12456,
    partidosPrincipais: ["PL", "PP", "MDB"]
  },
  {
    id: 5,
    nome: "Ipiranga Produtos de Petróleo S.A.",
    cnpj: "33.337.122/0001-97",
    valorTotal: 28900000,
    contratos: 9876,
    partidosPrincipais: ["PT", "PDT", "PSB"]
  },
  {
    id: 6,
    nome: "Localiza Rent a Car S.A.",
    cnpj: "16.670.085/0001-55",
    valorTotal: 24300000,
    contratos: 7234,
    partidosPrincipais: ["UNIÃO", "REPUBLICANOS", "PODE"]
  },
  {
    id: 7,
    nome: "Movida Locação de Veículos S.A.",
    cnpj: "04.548.776/0001-73",
    valorTotal: 21700000,
    contratos: 6543,
    partidosPrincipais: ["PL", "PSDB", "CIDADANIA"]
  },
  {
    id: 8,
    nome: "Vivo S.A.",
    cnpj: "02.558.157/0001-62",
    valorTotal: 19800000,
    contratos: 8932,
    partidosPrincipais: ["PT", "MDB", "PP"]
  },
  {
    id: 9,
    nome: "Claro S.A.",
    cnpj: "40.432.544/0001-47",
    valorTotal: 18500000,
    contratos: 8234,
    partidosPrincipais: ["UNIÃO", "PSD", "REPUBLICANOS"]
  },
  {
    id: 10,
    nome: "TIM S.A.",
    cnpj: "02.421.421/0001-11",
    valorTotal: 17200000,
    contratos: 7865,
    partidosPrincipais: ["PL", "PT", "PSOL"]
  },
  {
    id: 11,
    nome: "Magazine Luiza S.A.",
    cnpj: "47.960.950/0001-21",
    valorTotal: 15800000,
    contratos: 5432,
    partidosPrincipais: ["PP", "MDB", "PSDB"]
  },
  {
    id: 12,
    nome: "Americanas S.A.",
    cnpj: "00.776.574/0001-56",
    valorTotal: 14600000,
    contratos: 4987,
    partidosPrincipais: ["PT", "PDT", "PSB"]
  },
  {
    id: 13,
    nome: "Grupo Pão de Açúcar",
    cnpj: "59.281.253/0001-50",
    valorTotal: 13200000,
    contratos: 4321,
    partidosPrincipais: ["UNIÃO", "REPUBLICANOS", "PODE"]
  },
  {
    id: 14,
    nome: "Carrefour Comércio e Indústria Ltda",
    cnpj: "45.543.915/0001-81",
    valorTotal: 12100000,
    contratos: 3876,
    partidosPrincipais: ["PL", "PSDB", "NOVO"]
  },
  {
    id: 15,
    nome: "Grupo Casas Bahia",
    cnpj: "33.530.486/0001-07",
    valorTotal: 11400000,
    contratos: 3654,
    partidosPrincipais: ["PT", "MDB", "PP"]
  },
  {
    id: 16,
    nome: "Rede de Hotéis Accor Brasil S.A.",
    cnpj: "34.640.833/0001-04",
    valorTotal: 10800000,
    contratos: 3298,
    partidosPrincipais: ["UNIÃO", "PSD", "REPUBLICANOS"]
  },
  {
    id: 17,
    nome: "Atlantica Hospitality International",
    cnpj: "08.667.881/0001-15",
    valorTotal: 9900000,
    contratos: 2987,
    partidosPrincipais: ["PL", "PT", "PODE"]
  },
  {
    id: 18,
    nome: "Bristol Hotéis Brasil S.A.",
    cnpj: "60.558.491/0001-99",
    valorTotal: 9200000,
    contratos: 2765,
    partidosPrincipais: ["PP", "MDB", "PSDB"]
  },
  {
    id: 19,
    nome: "Gráfica Mundo Digital Ltda",
    cnpj: "12.345.678/0001-90",
    valorTotal: 8700000,
    contratos: 2543,
    partidosPrincipais: ["PT", "PDT", "PSB"]
  },
  {
    id: 20,
    nome: "Editora Nacional S.A.",
    cnpj: "09.876.543/0001-21",
    valorTotal: 8100000,
    contratos: 2321,
    partidosPrincipais: ["UNIÃO", "REPUBLICANOS", "CIDADANIA"]
  }
]


