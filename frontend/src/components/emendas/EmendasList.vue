<template>
  <BaseCard>
    <div class="p-6">
      <h3 class="text-lg font-semibold mb-4">Emendas Recentes</h3>
      <div class="space-y-4">
        <div v-for="emenda in emendas" :key="emenda.id" class="flex items-start gap-4 pb-4 border-b last:border-0">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <h4 class="font-semibold">{{ emenda.titulo }}</h4>
              <BaseBadge :variant="emenda.status === 'Aprovada' ? 'success' : 'warning'">
                {{ emenda.status }}
              </BaseBadge>
            </div>
            <p class="text-sm text-muted-foreground mb-2">{{ emenda.descricao }}</p>
            <div class="flex items-center gap-4 text-sm text-muted-foreground">
              <span>Autor: {{ emenda.autor }}</span>
              <span>•</span>
              <span>{{ emenda.municipio }}</span>
              <span>•</span>
              <span>{{ emenda.area }}</span>
            </div>
          </div>
          <div class="text-right">
            <p class="font-semibold text-lg">{{ emenda.valor }}</p>
          </div>
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'

const emendas = ref([
  {
    id: 1,
    titulo: 'Construção de UBS',
    descricao: 'Emenda para construção de Unidade Básica de Saúde no município',
    autor: 'João Silva',
    municipio: 'São Paulo - SP',
    area: 'Saúde',
    valor: 'R$ 2.5M',
    status: 'Aprovada'
  },
  {
    id: 2,
    titulo: 'Reforma de Escola Municipal',
    descricao: 'Reforma completa da Escola Municipal Professora Maria',
    autor: 'Maria Santos',
    municipio: 'Rio de Janeiro - RJ',
    area: 'Educação',
    valor: 'R$ 1.8M',
    status: 'Em análise'
  },
  {
    id: 3,
    titulo: 'Pavimentação de Via',
    descricao: 'Pavimentação asfáltica da Rua Principal',
    autor: 'Carlos Lima',
    municipio: 'Belo Horizonte - MG',
    area: 'Infraestrutura',
    valor: 'R$ 3.2M',
    status: 'Aprovada'
  }
])
</script>
