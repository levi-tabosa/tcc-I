<template>
  <section class="py-16 pt-24">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Distribuição por Região</h2>
        <p class="mt-2 text-muted-foreground">Representação dos 2010 deputados federais por região do Brasil</p>
      </div>

      <div class="grid lg:grid-cols-2 gap-8 items-center">
        <!-- Map -->
        <BaseCard class="relative z-0">
          <div ref="mapContainer" class="w-full h-[500px] rounded-lg overflow-hidden relative z-0" />
        </BaseCard>

        <!-- Region stats -->
        <div class="space-y-4">
          <BaseCard
            v-for="regiao in regioes"
            :key="regiao.nome"
            hover
            clickable
            :class="selectedRegion === regiao.nome ? 'ring-2 ring-primary shadow-lg' : ''"
            @mouseenter="highlightRegion(regiao.nome)"
            @mouseleave="unhighlightRegion()"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div :class="`w-4 h-4 rounded-full ${getRegionBgColor(regiao.nome)}`" />
                <span class="font-medium text-foreground">{{ regiao.nome }}</span>
              </div>
              <div class="text-right">
                <span class="text-2xl font-bold text-foreground">{{ regiao.deputados }}</span>
                <span class="text-sm text-muted-foreground ml-2">({{ regiao.percentual }}%)</span>
              </div>
            </div>
            <div class="mt-2 h-2 bg-muted rounded-full overflow-hidden">
              <div
                :class="`h-full rounded-full transition-all duration-500 ${getRegionBgColor(regiao.nome)}`"
                :style="{ width: `${regiao.percentual}%` }"
              />
            </div>
          </BaseCard>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { useDeputadosStore } from '@/stores/deputados'

const store = useDeputadosStore()
const mapContainer = ref<HTMLElement | null>(null)
const selectedRegion = ref<string | null>(null)
let map: L.Map | null = null
const regionLayers: Record<string, L.GeoJSON> = {}

// Fetch stats on mount
onMounted(() => {
  store.fetchEstatisticasGerais()
})

// Calculate percentages dynamically
const regioes = computed(() => {
    if (!store.generalStats || !store.generalStats.deputados_por_regiao) return []
    
    const total = store.generalStats.total_deputados || 1
    
    return store.generalStats.deputados_por_regiao.map(r => ({
        nome: r.name,
        deputados: r.value,
        percentual: ((r.value / total) * 100).toFixed(1)
    }))
})

const regionColors: Record<string, string> = {
  Norte: "#168976",
  Nordeste: "#f0b429",
  "Centro-Oeste": "#34a853",
  Sudeste: "#3b82f6",
  Sul: "#ef4444",
}

const getRegionBgColor = (nome: string) => {
  switch (nome) {
    case 'Norte': return 'bg-chart-5'
    case 'Nordeste': return 'bg-chart-2'
    case 'Centro-Oeste': return 'bg-chart-1'
    case 'Sudeste': return 'bg-chart-3'
    case 'Sul': return 'bg-chart-4'
    default: return 'bg-muted'
  }
}

const highlightRegion = (nome: string) => {
  selectedRegion.value = nome
  if (regionLayers[nome]) {
    regionLayers[nome].setStyle({
      fillOpacity: 0.8,
      weight: 3
    })
  }
}

const unhighlightRegion = () => {
  selectedRegion.value = null
  Object.values(regionLayers).forEach(layer => {
    layer.setStyle({
      fillOpacity: 0.5,
      weight: 2
    })
  })
}

// Coordenadas centrais e raios das regiões brasileiras
const regionData = {
  Sul: {
    center: [-28, -52] as [number, number],
    radius: 250000 // raio em metros
  },
  Sudeste: {
    center: [-19.5, -45] as [number, number],
    radius: 280000
  },
  "Centro-Oeste": {
    center: [-15.5, -53.5] as [number, number],
    radius: 350000
  },
  Nordeste: {
    center: [-9.5, -41] as [number, number],
    radius: 350000
  },
  Norte: {
    center: [-5, -61.5] as [number, number],
    radius: 450000
  }
}

onMounted(() => {
  if (mapContainer.value) {
    // Inicializar mapa centralizado no Brasil
    map = L.map(mapContainer.value, {
      zoomControl: true,
      scrollWheelZoom: false
    }).setView([-14.2350, -51.9253], 4)

    // Adicionar camada do OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18
    }).addTo(map)

    // Adicionar regiões ao mapa como círculos
    Object.entries(regionData).forEach(([name, data]) => {
      const circle = L.circle(data.center, {
        radius: data.radius,
        fillColor: regionColors[name],
        fillOpacity: 0.5,
        color: '#fff',
        weight: 2
      }).addTo(map!)

      circle.on({
        mouseover: () => highlightRegion(name),
        mouseout: () => unhighlightRegion()
      })

      regionLayers[name] = circle as any
    })
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
/* Garante que o mapa fique abaixo do header sticky */
:deep(.leaflet-container) {
  z-index: 1 !important;
}

:deep(.leaflet-pane),
:deep(.leaflet-tile-pane),
:deep(.leaflet-overlay-pane),
:deep(.leaflet-map-pane) {
  z-index: 1 !important;
}

:deep(.leaflet-control) {
  z-index: 10 !important;
}
</style>
