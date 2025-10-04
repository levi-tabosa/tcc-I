import { Button } from "@/components/ui/button"
import { Scale } from "lucide-react"

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/80 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Scale className="h-6 w-6 text-primary" />
          <span className="text-xl font-bold text-foreground">Fiscaliza Brasil</span>
        </div>

        <nav className="hidden items-center gap-6 md:flex">
          <a href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Parlamentares
          </a>
          <a href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Partidos
          </a>
          <a href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
            Sobre
          </a>
        
        </nav>
      </div>
    </header>
  )
}
