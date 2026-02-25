// Mock data kept only for EmendasCamaraView (no real backend endpoint for emendas yet)

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

const partidos = [
  { sigla: "PL", bloco: "direita" as const },
  { sigla: "PT", bloco: "esquerda" as const },
  { sigla: "UNIÃO", bloco: "centro" as const },
  { sigla: "PP", bloco: "centro" as const },
  { sigla: "MDB", bloco: "centro" as const },
  { sigla: "PSD", bloco: "centro" as const },
  { sigla: "REPUBLICANOS", bloco: "direita" as const },
  { sigla: "PDT", bloco: "esquerda" as const },
  { sigla: "PSDB", bloco: "centro" as const },
  { sigla: "PSB", bloco: "esquerda" as const },
]

const estados = ["SP", "MG", "RJ", "BA", "RS", "PR", "PE", "CE", "MA", "GO", "PA", "SC"]

const nomes = [
  "Pastor Sargento Isidório", "Carla Zambelli", "Nikolas Ferreira",
  "Guilherme Boulos", "Eduardo Bolsonaro", "Kim Kataguiri",
  "Tabata Amaral", "Marina Silva", "Marco Feliciano", "Alexandre Frota",
  "Joice Hasselmann", "Marcel van Hattem", "Gleisi Hoffmann",
  "Paulo Pimenta", "Jorge Solla", "Erika Hilton",
  "Sâmia Bomfim", "Fernanda Melchionna", "Talíria Petrone", "Luiza Erundina",
  "Ricardo Barros", "Arthur Lira", "Hugo Motta", "Ciro Nogueira",
  "Valdemar Costa Neto", "Marcos Pereira", "Baleia Rossi",
  "Elmar Nascimento", "Celso Sabino", "Luciano Bivar",
  "Paulinho da Força", "Renildo Calheiros",
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
    estado,
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


