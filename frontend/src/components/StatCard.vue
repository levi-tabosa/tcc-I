<template>
  <div class="stat-card">
    <div class="stat-card-header">
      <div class="stat-card-icon">
        <DollarSign v-if="icon === 'DollarSign'" />
        <Users v-else-if="icon === 'Users'" />
        <Award v-else-if="icon === 'Award'" />
        <TrendingUp v-else-if="icon === 'TrendingUp'" />
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
import { computed } from 'vue'
import { DollarSign, Users, Award, TrendingUp } from 'lucide-vue-next'

interface Props {
  title: string
  value: string | number
  format?: 'currency' | 'percentage' | 'number'
  subtitle?: string
  icon: string
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
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.stat-card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}

.stat-card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.stat-card-icon {
  padding: 0.5rem;
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
  color: var(--color-primary);
}

.stat-card-icon svg {
  width: 1.5rem;
  height: 1.5rem;
}

.stat-card-title {
  font-weight: 600;
  color: var(--color-gray-900);
  margin: 0;
  font-size: 1rem;
}

.stat-card-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-card-value {
  font-size: 1.875rem;
  font-weight: 700;
  color: var(--color-gray-900);
  line-height: 1;
}

.stat-card-subtitle {
  font-size: 0.875rem;
  color: var(--color-gray-600);
  margin: 0;
}
</style>