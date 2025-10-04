"use client"

import type React from "react"

import { useState } from "react"
import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function SearchBar() {
  const [query, setQuery] = useState("")

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("Searching for:", query)
  }

  return (
    <form onSubmit={handleSearch} className="mx-auto flex max-w-2xl gap-2">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
        <Input
          type="text"
          placeholder="Buscar parlamentar, partido ou estado..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="h-14 pl-11 text-base"
        />
      </div>
      <Button type="submit" size="lg" className="h-14 px-8">
        Pesquisar
      </Button>
    </form>
  )
}
