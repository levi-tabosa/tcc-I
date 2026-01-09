<template>
  <div class="stat-card">
    <div class="stat-card-header">
      <div class="stat-card-icon">
        <component :is="icon" />
      </div>
      <h3 class="stat-card-title">{{ title }}</h3>
    </div>
    
    <div class="stat-card-content">
      <div class="stat-card-value">
        {{ formattedValue }}
      </div>
      <p class="stat-card-subtitle">{{ subtitle }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, type Component } from 'vue'

interface Props {
  title: string
  value: string | number
  format?: 'currency' | 'percentage' | 'number'
  subtitle?: string
  icon: Component
}

const props = withDefaults(defineProps<Props>(), {
  format: 'number',
  subtitle: ''
})

const formattedValue = computed(() => {
  if (typeof props.value === 'string') {
    return props.value
  }
  
  switch (props.format) {
    case 'currency':
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(props.value)
    
    case 'percentage':
      return `${props.value}%`
    
    default:
      return props.value.toLocaleString('pt-BR')
  }
})
</script>

<style scoped>
.stat-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
  background: var(--card-hover-bg);
}

.stat-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stat-card-icon {
  padding: 0.5rem;
  background-color: var(--bg-secondary);
  border-radius: 0.5rem;
  color: var(--color-primary);
}

.dark .stat-card-icon {
  background-color: var(--surface-secondary);
}

.stat-card-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.stat-card-title {
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  font-size: 1rem;
}

.stat-card-content {
  text-align: left;
}

.stat-card-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.stat-card-subtitle {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin: 0;
}
</style>