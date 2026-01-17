<template>
  <section class="py-16">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-foreground">Distribuição por Região</h2>
        <p class="mt-2 text-muted-foreground">Representação dos 513 deputados federais por região do Brasil</p>
      </div>

      <div class="grid lg:grid-cols-2 gap-8 items-center">
        <!-- Map -->
        <BaseCard>
          <div ref="mapContainer" class="w-full h-[500px] rounded-lg overflow-hidden" />
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
                <div :class="`w-4 h-4 rounded ${getRegionBgColor(regiao.nome)}`" />
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
import { ref, onMounted, onBeforeUnmount } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import { regioes } from '@/data/mock-data'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const mapContainer = ref<HTMLElement | null>(null)
const selectedRegion = ref<string | null>(null)
let map: L.Map | null = null
const regionLayers: Record<string, L.GeoJSON> = {}

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

// Coordenadas aproximadas das regiões brasileiras
const regionData = {
  Sul: {
    type: "Feature",
    properties: { name: "Sul" },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [-57, -34], [-48, -34], [-48, -22], [-54, -22], [-57, -27], [-57, -34]
      ]]
    }
  },
  Sudeste: {
    type: "Feature",
    properties: { name: "Sudeste" },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [-51, -25], [-39, -25], [-39, -14], [-51, -14], [-51, -25]
      ]]
    }
  },
  "Centro-Oeste": {
    type: "Feature",
    properties: { name: "Centro-Oeste" },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [-61, -24], [-46, -24], [-46, -7], [-61, -7], [-61, -24]
      ]]
    }
  },
  Nordeste: {
    type: "Feature",
    properties: { name: "Nordeste" },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [-48, -18], [-34, -18], [-34, -1], [-48, -1], [-48, -18]
      ]]
    }
  },
  Norte: {
    type: "Feature",
    properties: { name: "Norte" },
    geometry: {
      type: "Polygon",
      coordinates: [[
        [-74, 5], [-49, 5], [-49, -18], [-74, -18], [-74, 5]
      ]]
    }
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

    // Adicionar regiões ao mapa
    Object.entries(regionData).forEach(([name, data]) => {
      const layer = L.geoJSON(data as any, {
        style: {
          fillColor: regionColors[name],
          fillOpacity: 0.5,
          color: '#fff',
          weight: 2
        },
        onEachFeature: (_feature, layer) => {
          layer.on({
            mouseover: () => highlightRegion(name),
            mouseout: () => unhighlightRegion()
          })
        }
      }).addTo(map!)

      regionLayers[name] = layer
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
