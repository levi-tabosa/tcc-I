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
      <div
        v-for="proposicao in store.proposicoesList"
        :key="proposicao.id"
      >
        <BaseCard
          hover
          class="overflow-hidden cursor-pointer transition-all duration-200"
          :class="{ 'ring-2 ring-primary/50': store.selectedProposicaoId === proposicao.id }"
          @click="store.toggleProposicaoVotos(proposicao.id)"
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
            <div class="flex items-center gap-3 flex-shrink-0">
              <a
                :href="`https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=${proposicao.id}`"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-1 text-sm text-primary hover:underline group"
                @click.stop
              >
                Ver na Câmara
                <ExternalLink class="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
              </a>
              <ChevronDown
                class="h-4 w-4 text-muted-foreground transition-transform duration-200"
                :class="{ 'rotate-180': store.selectedProposicaoId === proposicao.id }"
              />
            </div>
          </div>
        </BaseCard>

        <!-- Painel de Votos Expansível -->
        <div
          v-if="store.selectedProposicaoId === proposicao.id"
          class="mt-1 rounded-lg border border-border bg-muted/30 overflow-hidden animate-slideDown"
        >
          <!-- Loading votos -->
          <div v-if="store.loadingVotos" class="py-8 text-center">
            <div class="inline-flex items-center gap-2 text-muted-foreground">
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Buscando votos...
            </div>
          </div>

          <!-- Sem votos -->
          <div
            v-else-if="store.currentVotos && store.currentVotos.historico_votacoes.length === 0"
            class="py-8 text-center"
          >
            <Vote class="h-8 w-8 text-muted-foreground mx-auto mb-2" />
            <p class="text-sm text-muted-foreground">Sem votos nominais registrados para esta proposição.</p>
          </div>

          <!-- Lista de Votações (Accordion) -->
          <div v-else-if="store.currentVotos" class="divide-y divide-border">
            <div
              v-for="votacao in store.currentVotos.historico_votacoes"
              :key="votacao.id_votacao"
              class="transition-colors hover:bg-muted/10"
            >
              <!-- Header da Votação (Clicável) -->
              <button
                @click="toggleVotacao(votacao.id_votacao)"
                class="w-full text-left p-4 flex items-start gap-3 focus:outline-none focus:bg-muted/20"
              >
                <ChevronRight
                  class="h-5 w-5 text-muted-foreground mt-0.5 transition-transform duration-200 flex-shrink-0"
                  :class="{ 'rotate-90': expandedVotacaoIds.has(votacao.id_votacao) }"
                />
                
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between gap-4 mb-2 flex-wrap">
                    <p class="text-sm font-medium text-foreground line-clamp-2">{{ votacao.descricao || 'Votação' }}</p>
                    <BaseBadge variant="outline" class="flex-shrink-0">{{ votacao.total_votos }} votos</BaseBadge>
                  </div>
                  
                  <div class="flex items-center gap-2 mb-2">
                     <span class="text-xs text-muted-foreground">{{ formatDateTime(votacao.data) }}</span>
                  </div>

                  <!-- Resumo (Sempre visível) -->
                  <div class="flex flex-wrap gap-2">
                    <span
                      v-for="(count, tipo) in getVotosSummary(votacao.lista_votos)"
                      :key="tipo"
                      class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium border"
                      :class="getVotoBadgeClass(tipo as string)"
                    >
                      {{ tipo }}: {{ count }}
                    </span>
                  </div>
                </div>
              </button>

              <!-- Tabela de votos (Expansível) -->
              <div
                v-if="expandedVotacaoIds.has(votacao.id_votacao)"
                class="px-4 pb-4 pl-12 animate-slideDown"
              >
                <div class="max-h-60 overflow-y-auto rounded-lg border border-border">
                  <table class="w-full text-sm">
                    <thead class="bg-muted sticky top-0">
                      <tr>
                        <th class="text-left py-2 px-3 font-medium text-muted-foreground">Deputado(a)</th>
                        <th class="text-center py-2 px-3 font-medium text-muted-foreground w-32">Voto</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-border">
                      <tr v-for="voto in votacao.lista_votos" :key="voto.deputado_id" class="hover:bg-muted/50">
                        <td class="py-2 px-3 text-foreground">{{ voto.nome }}</td>
                        <td class="py-2 px-3 text-center">
                          <span
                            class="inline-block px-2 py-0.5 rounded-full text-xs font-medium border"
                            :class="getVotoBadgeClass(voto.voto)"
                          >
                            {{ voto.voto }}
                          </span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
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
import { onMounted, ref, watch } from 'vue'
import { FileText, User, ExternalLink, ChevronDown, Vote, ChevronRight } from 'lucide-vue-next'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import { useDeputadosStore } from '@/stores/deputados'
import type { VotoDeputado } from '@/stores/deputados'

const store = useDeputadosStore()
const expandedVotacaoIds = ref<Set<string>>(new Set())

onMounted(() => {
  if (store.proposicoesList.length === 0) {
    store.fetchProposicoes()
  }
})

// Watch for changes in current votes to expand the first one by default
watch(() => store.currentVotos, (newVotos) => {
  expandedVotacaoIds.value.clear()
  if (newVotos && newVotos.historico_votacoes.length > 0) {
    // Expand the first (most recent) voting by default
    expandedVotacaoIds.value.add(newVotos.historico_votacoes[0].id_votacao)
  }
})

const toggleVotacao = (id: string) => {
  if (expandedVotacaoIds.value.has(id)) {
    expandedVotacaoIds.value.delete(id)
  } else {
    expandedVotacaoIds.value.add(id)
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

const formatDateTime = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getVotosSummary = (votos: VotoDeputado[]) => {
  const summary: Record<string, number> = {}
  votos.forEach(v => {
    summary[v.voto] = (summary[v.voto] || 0) + 1
  })
  return summary
}

const getVotoBadgeClass = (voto: string) => {
  const v = voto.toLowerCase()
  if (v === 'sim') return 'bg-emerald-100 text-emerald-800 border-emerald-200 dark:bg-emerald-900/40 dark:text-emerald-300 dark:border-emerald-800 border'
  if (v.includes('não') || v === 'nao') return 'bg-rose-100 text-rose-800 border-rose-200 dark:bg-rose-900/40 dark:text-rose-300 dark:border-rose-800 border'
  if (v.includes('abstenção') || v.includes('abstencao')) return 'bg-amber-100 text-amber-800 border-amber-200 dark:bg-amber-900/40 dark:text-amber-300 dark:border-amber-800 border'
  if (v.includes('obstrução') || v.includes('obstrucao')) return 'bg-orange-100 text-orange-800 border-orange-200 dark:bg-orange-900/40 dark:text-orange-300 dark:border-orange-800 border'
  return 'bg-slate-100 text-slate-800 border-slate-200 dark:bg-slate-800 dark:text-slate-300 dark:border-slate-700 border'
}
</script>

<style scoped>
@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    max-height: 2000px;
    transform: translateY(0);
  }
}

.animate-slideDown {
  animation: slideDown 0.3s ease-out forwards;
}
</style>
