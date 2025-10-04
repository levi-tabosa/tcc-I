import { SearchBar } from "@/components/search-bar"
import { StatsGrid } from "@/components/stats-grid"
import { FeaturesSection } from "@/components/features-section"
import { Header } from "@/components/header"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main>
        {/* Hero Section */}
        <section className="relative px-4 py-20 md:py-32 lg:py-40">
          <div className="mx-auto max-w-7xl">
            <div className="mx-auto max-w-4xl text-center">
              <h1 className="text-balance text-5xl font-bold tracking-tight text-foreground md:text-6xl lg:text-7xl">
                Transparência parlamentar <span className="text-primary">ao alcance de todos</span>
              </h1>
              <p className="mt-6 text-pretty text-lg text-muted-foreground md:text-xl lg:text-2xl">
                Acompanhe gastos, votações e desempenho dos parlamentares brasileiros de forma clara e objetiva
              </p>

              <div className="mt-10">
                <SearchBar />
              </div>

              <p className="mt-4 text-sm text-muted-foreground">Busque por nome do parlamentar, partido ou estado</p>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="border-y border-border bg-card px-4 py-16">
          <div className="mx-auto max-w-7xl">
            <StatsGrid />
          </div>
        </section>

        {/* Features Section */}
        <section className="px-4 py-20 md:py-32">
          <div className="mx-auto max-w-7xl">
            <FeaturesSection />
          </div>
        </section>

        {/* CTA Section */}
        <section className="px-4 py-20">
          <div className="mx-auto max-w-4xl text-center">
            <h2 className="text-balance text-3xl font-bold tracking-tight text-foreground md:text-4xl lg:text-5xl">
              A fiscalização é um direito de todos
            </h2>
            <p className="mt-4 text-pretty text-lg text-muted-foreground">
              Não deixe que barreiras técnicas impeçam você de acompanhar seus representantes
            </p>
          </div>
        </section>
      </main>

      <footer className="border-t border-border px-4 py-12">
        <div className="mx-auto max-w-7xl">
          <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
            <p className="text-sm text-muted-foreground">Dados públicos da Câmara dos Deputados e Senado Federal</p>
            <p className="text-sm text-muted-foreground">© 2025 Fiscaliza Brasil</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
