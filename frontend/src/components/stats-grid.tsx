import { TrendingUp, Users, Vote, DollarSign } from "lucide-react"

const stats = [
  {
    label: "Parlamentares",
    value: "594",
    description: "Câmara e Senado",
    icon: Users,
  },
  {
    label: "Votações",
    value: "2.847",
    description: "Registradas em 2024",
    icon: Vote,
  },
  {
    label: "Gastos",
    value: "R$ 1,2B",
    description: "Cota parlamentar 2024",
    icon: DollarSign,
  },
  {
    label: "Transparência",
    value: "100%",
    description: "Dados públicos",
    icon: TrendingUp,
  },
]

export function StatsGrid() {
  return (
    <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
      {stats.map((stat) => {
        const Icon = stat.icon
        return (
          <div key={stat.label} className="flex flex-col gap-3 rounded-lg border border-border bg-card p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                <Icon className="h-5 w-5 text-primary" />
              </div>
              <div className="text-sm font-medium text-muted-foreground">{stat.label}</div>
            </div>
            <div className="text-3xl font-bold text-foreground">{stat.value}</div>
            <div className="text-sm text-muted-foreground">{stat.description}</div>
          </div>
        )
      })}
    </div>
  )
}
