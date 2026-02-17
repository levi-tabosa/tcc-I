<template>
  <div>
    <!-- Results count -->
    <p class="text-sm text-muted-foreground mb-4">
      {{ store.proposicoesList.length }} proposições encontradas
    </p>

    <!-- Loading State -->
    <div v-if="store.loadingProposicoes && store.proposicoesList.length === 0" class="text-center py-12">
      <p class="text-muted-foreground">Carregando proposições...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="store.error" class="text-center py-12">
      <p class="text-destructive">{{ store.error }}</p>
    </div>

    <!-- Lista -->
    <div v-else class="space-y-4">
      <BaseCard
        v-for="proposicao in store.proposicoesList"
        :key="proposicao.id"
        hover
        class="overflow-hidden"
      >
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-lg bg-primary/10">
            <FileText class="h-6 w-6 text-primary" />
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1 flex-wrap">
              <BaseBadge>{{ proposicao.siglaTipo }} {{ proposicao.numero }}/{{ proposicao.ano }}</BaseBadge>
              <span v-if="proposicao.dataApresentacao" class="text-xs text-muted-foreground">
                {{ formatDate(proposicao.dataApresentacao) }}
              </span>
            </div>
            <p class="text-sm text-foreground line-clamp-2">{{ proposicao.ementa }}</p>
            <div class="flex items-center gap-2 mt-2">
              <User class="h-3 w-3 text-muted-foreground" />
              <span class="text-xs text-muted-foreground">{{ proposicao.autor_principal }}</span>
            </div>
          </div>
          <a
            :href="`https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=${proposicao.id}`"
            target="_blank"
            rel="noopener noreferrer"
            class="flex-shrink-0 inline-flex items-center gap-1 text-sm text-primary hover:underline group"
          >
            Ver na Câmara
            <ExternalLink class="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
          </a>
        </div>
      </BaseCard>
    </div>

    <!-- Empty state -->
    <div v-if="!store.loadingProposicoes && !store.error && store.proposicoesList.length === 0" class="text-center py-12">
      <FileText class="h-12 w-12 text-muted-foreground mx-auto mb-4" />
      <p class="text-muted-foreground">Nenhuma proposição encontrada com os filtros selecionados.</p>
    </div>

    <!-- Load more -->
    <div v-if="store.hasMoreProposicoes && store.proposicoesList.length > 0" class="flex justify-center mt-8">
      <button
        @click="store.loadMoreProposicoes()"
        :disabled="store.loadingProposicoes"
        class="px-6 py-3 rounded-lg border border-border bg-background text-foreground font-medium hover:bg-muted transition-colors disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center gap-2"
      >
        <span v-if="store.loadingProposicoes">Carregando...</span>
        <span v-else>Carregar mais</span>
        <ChevronDown v-if="!store.loadingProposicoes" class="h-4 w-4" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { FileText, User, ExternalLink, ChevronDown } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { useDeputadosStore } from '@/stores/deputados'

const store = useDeputadosStore()

onMounted(() => {
  if (store.proposicoesList.length === 0) {
    store.fetchProposicoes()
  }
})

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}
</script>
