import { BarChart3, Eye, FileText } from "lucide-react"
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

const features = [
  {
    title: "Gastos Parlamentares",
    description: "Visualize e analise todos os gastos da cota parlamentar de forma detalhada e transparente",
    icon: FileText,
  },
  {
    title: "Histórico de Votações",
    description: "Acompanhe como cada parlamentar votou em projetos de lei e propostas importantes",
    icon: Eye,
  },
  {
    title: "Fidelidade Partidária",
    description: "Métricas consolidadas sobre alinhamento partidário e coerência nas votações",
    icon: BarChart3,
  },
]

export function FeaturesSection() {
  return (
    <div className="space-y-12">
      <div className="text-center">
        <h2 className="text-balance text-3xl font-bold tracking-tight text-foreground md:text-4xl">
          Dados públicos, análises claras
        </h2>
        <p className="mt-4 text-pretty text-lg text-muted-foreground">
          Transformamos dados complexos em informações acessíveis para todos
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-3">
        {features.map((feature) => {
          const Icon = feature.icon
          return (
            <Card key={feature.title} className="border-border">
              <CardHeader>
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <Icon className="h-6 w-6 text-primary" />
                </div>
                <CardTitle className="text-xl">{feature.title}</CardTitle>
                <CardDescription className="text-base">{feature.description}</CardDescription>
              </CardHeader>
            </Card>
          )
        })}
      </div>
    </div>
  )
}
