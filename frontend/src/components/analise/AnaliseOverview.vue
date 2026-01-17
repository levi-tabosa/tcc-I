<template>
  <div class="space-y-6">
    <div class="grid gap-4 md:grid-cols-3">
      <BaseCard>
        <div class="p-6">
          <div class="text-sm font-medium text-muted-foreground">Mais Presente</div>
          <div class="text-2xl font-bold mt-2">João Silva</div>
          <p class="text-xs text-muted-foreground mt-1">98.5% de presença</p>
        </div>
      </BaseCard>
      <BaseCard>
        <div class="p-6">
          <div class="text-sm font-medium text-muted-foreground">Mais Econômico</div>
          <div class="text-2xl font-bold mt-2">Maria Santos</div>
          <p class="text-xs text-muted-foreground mt-1">R$ 45K em despesas</p>
        </div>
      </BaseCard>
      <BaseCard>
        <div class="p-6">
          <div class="text-sm font-medium text-muted-foreground">Mais Emendas</div>
          <div class="text-2xl font-bold mt-2">Carlos Lima</div>
          <p class="text-xs text-muted-foreground mt-1">234 emendas aprovadas</p>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
</script>
