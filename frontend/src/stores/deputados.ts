import { defineStore } from "pinia"
import { ref, computed } from "vue"
import { deputados } from "@/data/mock-data"

export interface Filters {
  search: string
  partido: string
  estado: string
  bloco: string
}

export const useDeputadosStore = defineStore("deputados", () => {
  const filters = ref<Filters>({
    search: "",
    partido: "",
    estado: "",
    bloco: "",
  })

  const currentPage = ref(1)
  const itemsPerPage = 12

  const filteredDeputados = computed(() => {
    return deputados.filter((dep) => {
      if (filters.value.search && !dep.nome.toLowerCase().includes(filters.value.search.toLowerCase())) {
        return false
      }
      if (filters.value.partido && dep.partido !== filters.value.partido) {
        return false
      }
      if (filters.value.estado && dep.estado !== filters.value.estado) {
        return false
      }
      if (filters.value.bloco && dep.blocoIdeologico !== filters.value.bloco) {
        return false
      }
      return true
    })
  })

  const totalPages = computed(() => Math.ceil(filteredDeputados.value.length / itemsPerPage))

  const paginatedDeputados = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage
    return filteredDeputados.value.slice(start, start + itemsPerPage)
  })

  const setFilter = (key: keyof Filters, value: string) => {
    filters.value[key] = value
    currentPage.value = 1
  }

  const setPage = (page: number) => {
    currentPage.value = page
  }

  const resetFilters = () => {
    filters.value = { search: "", partido: "", estado: "", bloco: "" }
    currentPage.value = 1
  }

  return {
    filters,
    currentPage,
    filteredDeputados,
    paginatedDeputados,
    totalPages,
    setFilter,
    setPage,
    resetFilters,
  }
})
