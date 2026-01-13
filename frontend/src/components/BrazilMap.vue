<template>
  <div class="map-container">
    <h3 class="map-title">Explore Parlamentares por Estado</h3>
    <div ref="mapContainer" class="leaflet-map"></div>
    
    <!-- Legenda -->
    <div class="map-legend">
      <div class="legend-title">Número de Deputados</div>
      <div class="legend-items">
        <div class="legend-item">
          <span class="legend-color" style="background: #fee5d9"></span>
          <span>1-8</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background: #fcae91"></span>
          <span>9-20</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background: #fb6a4a"></span>
          <span>21-40</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background: #de2d26"></span>
          <span>41-60</span>
        </div>
        <div class="legend-item">
          <span class="legend-color" style="background: #a50f15"></span>
          <span>60+</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

interface Props {
  parlamentaresPorEstado?: Record<string, number>
}

const props = withDefaults(defineProps<Props>(), {
  parlamentaresPorEstado: () => ({})
})

const router = useRouter()
const mapContainer = ref<HTMLElement | null>(null)
let map: L.Map | null = null
let geoJsonLayer: L.GeoJSON | null = null

// Coordenadas dos centros dos estados brasileiros
const estadosCoordenadas: Record<string, [number, number]> = {
  AC: [-9.0238, -70.812],
  AL: [-9.5713, -36.782],
  AP: [0.9020, -52.003],
  AM: [-3.4168, -65.8561],
  BA: [-12.5797, -41.7007],
  CE: [-5.4984, -39.3206],
  DF: [-15.7998, -47.8645],
  ES: [-19.1834, -40.3089],
  GO: [-15.8270, -49.8362],
  MA: [-4.9609, -45.2744],
  MT: [-12.6819, -56.9211],
  MS: [-20.7722, -54.7852],
  MG: [-18.5122, -44.5550],
  PA: [-1.9981, -54.9306],
  PB: [-7.2400, -36.7820],
  PR: [-25.2521, -52.0215],
  PE: [-8.8137, -36.9541],
  PI: [-7.7183, -42.7289],
  RJ: [-22.9099, -43.2095],
  RN: [-5.4026, -36.9541],
  RS: [-30.0346, -51.2177],
  RO: [-10.8300, -63.3458],
  RR: [2.7376, -62.0751],
  SC: [-27.2423, -50.2189],
  SP: [-23.5505, -46.6333],
  SE: [-10.5741, -37.3857],
  TO: [-10.1753, -48.2982]
}

const stateNames: Record<string, string> = {
  AC: 'Acre', AL: 'Alagoas', AP: 'Amapá', AM: 'Amazonas',
  BA: 'Bahia', CE: 'Ceará', DF: 'Distrito Federal', ES: 'Espírito Santo',
  GO: 'Goiás', MA: 'Maranhão', MT: 'Mato Grosso', MS: 'Mato Grosso do Sul',
  MG: 'Minas Gerais', PA: 'Pará', PB: 'Paraíba', PR: 'Paraná',
  PE: 'Pernambuco', PI: 'Piauí', RJ: 'Rio de Janeiro', RN: 'Rio Grande do Norte',
  RS: 'Rio Grande do Sul', RO: 'Rondônia', RR: 'Roraima', SC: 'Santa Catarina',
  SP: 'São Paulo', SE: 'Sergipe', TO: 'Tocantins'
}

// Função para determinar cor baseada na quantidade
const getColor = (count: number) => {
  if (count === 0) return '#f0f0f0'
  if (count <= 8) return '#fee5d9'
  if (count <= 20) return '#fcae91'
  if (count <= 40) return '#fb6a4a'
  if (count <= 60) return '#de2d26'
  return '#a50f15'
}

// GeoJSON simplificado dos estados brasileiros (você pode usar um arquivo mais completo)
const brazilStatesGeoJSON = {
  type: 'FeatureCollection',
  features: Object.keys(estadosCoordenadas).map(uf => ({
    type: 'Feature',
    properties: {
      sigla: uf,
      nome: stateNames[uf]
    },
    geometry: {
      type: 'Point',
      coordinates: [estadosCoordenadas[uf][1], estadosCoordenadas[uf][0]]
    }
  }))
}

const style = (feature: any) => {
  const uf = feature.properties.sigla
  const count = props.parlamentaresPorEstado[uf] || 0
  return {
    fillColor: getColor(count),
    weight: 2,
    opacity: 1,
    color: 'white',
    fillOpacity: 0.7
  }
}

const onEachFeature = (feature: any, layer: L.Layer) => {
  const uf = feature.properties.sigla
  const nome = feature.properties.nome
  const count = props.parlamentaresPorEstado[uf] || 0

  layer.bindTooltip(
    `<strong>${nome} (${uf})</strong><br/>${count} deputados`,
    { permanent: false, direction: 'top' }
  )

  layer.on({
    mouseover: (e: L.LeafletMouseEvent) => {
      const target = e.target as L.Path
      target.setStyle({
        weight: 3,
        fillOpacity: 0.9
      })
    },
    mouseout: (e: L.LeafletMouseEvent) => {
      const target = e.target as L.Path
      target.setStyle({
        weight: 2,
        fillOpacity: 0.7
      })
    },
    click: () => {
      router.push({ path: '/parlamentares', query: { estado: uf } })
    }
  })
}

const initMap = () => {
  if (!mapContainer.value) return

  // Criar mapa centrado no Brasil
  map = L.map(mapContainer.value, {
    center: [-14.235, -51.9253],
    zoom: 4,
    minZoom: 4,
    maxZoom: 8,
    zoomControl: true
  })

  // Adicionar tile layer do OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 19
  }).addTo(map)

  // Adicionar marcadores circulares para cada estado
  Object.keys(estadosCoordenadas).forEach(uf => {
    const coords = estadosCoordenadas[uf]
    const count = props.parlamentaresPorEstado[uf] || 0
    const color = getColor(count)
    
    const circle = L.circleMarker([coords[0], coords[1]], {
      radius: Math.max(15, Math.min(40, count * 0.5)),
      fillColor: color,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.7
    })
    
    if (map) circle.addTo(map)

    circle.bindTooltip(
      `<strong>${stateNames[uf]} (${uf})</strong><br/>${count} deputados`,
      { permanent: false, direction: 'top' }
    )

    circle.on('click', () => {
      router.push({ path: '/parlamentares', query: { estado: uf } })
    })

    circle.on('mouseover', () => {
      circle.setStyle({ fillOpacity: 0.9, weight: 3 })
    })

    circle.on('mouseout', () => {
      circle.setStyle({ fillOpacity: 0.7, weight: 2 })
    })
  })
}

onMounted(() => {
  initMap()
})

// Atualizar mapa quando os dados mudarem
watch(() => props.parlamentaresPorEstado, () => {
  if (map) {
    map.eachLayer((layer) => {
      if (layer instanceof L.CircleMarker) {
        map?.removeLayer(layer)
      }
    })
    
    Object.keys(estadosCoordenadas).forEach(uf => {
      const coords = estadosCoordenadas[uf]
      const count = props.parlamentaresPorEstado[uf] || 0
      const color = getColor(count)
      
      const circle = L.circleMarker([coords[0], coords[1]], {
        radius: Math.max(15, Math.min(40, count * 0.5)),
        fillColor: color,
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.7
      }).addTo(map!)

      circle.bindTooltip(
        `<strong>${stateNames[uf]} (${uf})</strong><br/>${count} deputados`,
        { permanent: false, direction: 'top' }
      )

      circle.on('click', () => {
        router.push({ path: '/parlamentares', query: { estado: uf } })
      })

      circle.on('mouseover', () => {
        circle.setStyle({ fillOpacity: 0.9, weight: 3 })
      })

      circle.on('mouseout', () => {
        circle.setStyle({ fillOpacity: 0.7, weight: 2 })
      })
    })
  }
}, { deep: true })
</script>

<style scoped>
.map-container {
  background: var(--surface-primary);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid var(--border-primary);
  box-shadow: var(--shadow-md);
  position: relative;
  z-index: 1;
}

.map-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  text-align: center;
}

.leaflet-map {
  height: 600px;
  width: 100%;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 1px solid var(--border-primary);
  position: relative;
  z-index: 1;
}

.map-legend {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--bg-secondary);
  border-radius: 0.5rem;
  border: 1px solid var(--border-primary);
}

.legend-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
  border: 1px solid var(--border-primary);
}

@media (max-width: 768px) {
  .leaflet-map {
    height: 400px;
  }

  .map-title {
    font-size: 1.25rem;
  }
}
</style>
