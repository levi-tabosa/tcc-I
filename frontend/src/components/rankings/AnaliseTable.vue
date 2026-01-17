<template>
  <BaseCard>
    <div class="p-6">
      <h3 class="text-lg font-semibold mb-4">Ranking Geral</h3>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b">
              <th class="text-left py-3 px-2">Posição</th>
              <th class="text-left py-3 px-2">Deputado</th>
              <th class="text-left py-3 px-2">Partido</th>
              <th class="text-right py-3 px-2">Presença</th>
              <th class="text-right py-3 px-2">Despesas</th>
              <th class="text-right py-3 px-2">Emendas</th>
              <th class="text-right py-3 px-2">Pontuação</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(deputado, index) in ranking" :key="deputado.id" class="border-b hover:bg-muted/50">
              <td class="py-3 px-2">
                <span class="font-semibold">{{ index + 1 }}º</span>
              </td>
              <td class="py-3 px-2">{{ deputado.nome }}</td>
              <td class="py-3 px-2">
                <BaseBadge>{{ deputado.partido }}</BaseBadge>
              </td>
              <td class="text-right py-3 px-2">{{ deputado.presenca }}%</td>
              <td class="text-right py-3 px-2">{{ deputado.despesas }}</td>
              <td class="text-right py-3 px-2">{{ deputado.emendas }}</td>
              <td class="text-right py-3 px-2">
                <span class="font-bold">{{ deputado.pontuacao }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'

const ranking = ref([
  { id: 1, nome: 'João Silva', partido: 'PT', presenca: 98.5, despesas: 'R$ 45K', emendas: 234, pontuacao: 9.5 },
  { id: 2, nome: 'Maria Santos', partido: 'PSDB', presenca: 97.2, despesas: 'R$ 52K', emendas: 198, pontuacao: 9.3 },
  { id: 3, nome: 'Carlos Lima', partido: 'MDB', presenca: 96.8, despesas: 'R$ 48K', emendas: 212, pontuacao: 9.2 },
  { id: 4, nome: 'Ana Costa', partido: 'PP', presenca: 95.5, despesas: 'R$ 58K', emendas: 187, pontuacao: 9.0 },
  { id: 5, nome: 'Pedro Oliveira', partido: 'PL', presenca: 94.2, despesas: 'R$ 62K', emendas: 165, pontuacao: 8.8 },
])
</script>
