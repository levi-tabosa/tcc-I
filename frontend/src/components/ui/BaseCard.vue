<template>
  <div
    class="rounded-lg border border-border bg-card text-card-foreground shadow-sm transition-all duration-300"
    :class="[
      hover && 'hover:shadow-lg hover:-translate-y-1',
      clickable && 'cursor-pointer'
    ]"
  >
    <div v-if="$slots.header" class="flex flex-col space-y-1.5 p-6">
      <slot name="header" />
    </div>
    <div class="p-6" :class="{ 'pt-0': $slots.header }">
      <slot />
    </div>
    <div v-if="$slots.footer" class="flex items-center p-6 pt-0">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  hover?: boolean
  clickable?: boolean
}>()
</script>
