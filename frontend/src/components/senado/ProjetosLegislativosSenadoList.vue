<template>
  <div>
    <!-- Results count -->
    <p class="text-sm text-muted-foreground mb-4">
      {{ store.filteredProjetosLegislativos.length }} projetos legislativos encontrados
    </p>

    <!-- Loading -->
    <div v-if="store.loadingProjetosLegislativos && store.projetosLegislativosList.length === 0" class="py-12">
      <div class="space-y-4">
        <div v-for="i in 3" :key="i" class="card-default p-6">
          <div class="flex items-start gap-4">
            <div class="skeleton-rect h-12 w-12 flex-shrink-0"></div>
            <div class="flex-1 space-y-2">
              <div class="flex gap-2">
                <div class="skeleton-text w-24"></div>
                <div class="skeleton-text-sm w-16"></div>
              </div>
              <div class="skeleton-text w-full"></div>
              <div class="skeleton-text w-3/4"></div>
              <div class="skeleton-text-sm w-32 mt-2"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="store.filteredProjetosLegislativos.length === 0" class="text-center py-12">
      <FileText class="h-12 w-12 text-muted-foreground mx-auto mb-4" />
      <p class="text-muted-foreground">Nenhum projeto legislativo encontrado com os filtros atuais.</p>
    </div>

    <!-- Lista -->
    <div v-else class="space-y-4">
      <BaseCard
        v-for="projeto in store.filteredProjetosLegislativos"
        :key="projeto.id"
        hover
        class="overflow-hidden"
      >
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-lg bg-primary/10">
            <FileText class="h-6 w-6 text-primary" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1 flex-wrap">
              <BaseBadge>{{ projeto.siglaTipo }} {{ projeto.numero }}/{{ projeto.ano }}</BaseBadge>
              <span v-if="projeto.dataApresentacao" class="text-xs text-muted-foreground">
                {{ formatDate(projeto.dataApresentacao) }}
              </span>
            </div>
            <p class="text-sm text-foreground line-clamp-2">{{ projeto.ementa }}</p>
            <div class="flex items-center gap-2 mt-2">
              <User class="h-3 w-3 text-muted-foreground" />
              <span class="text-xs text-muted-foreground">{{ projeto.autor_principal }}</span>
            </div>
          </div>
          <div class="flex items-center gap-3 flex-shrink-0">
            <a
              :href="`https://www25.senado.leg.br/web/atividade/materias/-/materia/${projeto.id}`"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-1 text-sm text-primary hover:underline group"
            >
              Ver no Senado
              <ExternalLink class="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
            </a>
          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FileText, User, ExternalLink } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { useSenadoresStore } from '@/stores/senadores'

const store = useSenadoresStore()

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('pt-BR')
}
</script>
