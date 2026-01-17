<template>
  <span
    class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium transition-colors"
    :class="variantClasses"
  >
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  variant?: 'default' | 'outline' | 'secondary' | 'destructive' | 'success' | 'warning'
}>(), {
  variant: 'default'
})

const variantClasses = computed(() => {
  switch (props.variant) {
    case 'outline':
      return 'border border-border bg-transparent text-foreground'
    case 'secondary':
      return 'bg-secondary text-secondary-foreground'
    case 'destructive':
      return 'bg-red-500/10 text-red-500'
    case 'success':
      return 'bg-green-500/10 text-green-600'
    case 'warning':
      return 'bg-yellow-500/10 text-yellow-600'
    default:
      return 'bg-primary text-primary-foreground'
  }
})
</script>
