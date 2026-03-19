<template>
  <section class="py-20 bg-background overflow-hidden relative">
    <!-- Subtle Background pattern -->
    <div class="absolute inset-0 opacity-[0.03] pointer-events-none">
      <svg class="h-full w-full" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="currentColor" stroke-width="1" />
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)" />
      </svg>
    </div>

    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 relative">
      <div class="bg-card rounded-3xl border border-border p-8 lg:p-16 shadow-2xl overflow-hidden">
        <div class="grid lg:grid-cols-2 gap-12 items-center">
          <div>
            <span class="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary mb-6">
              <ShieldCheck class="h-4 w-4" />
              Compromisso com a Transparência
            </span>
            <h2 class="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
              Como garantimos a <span class="text-primary italic">veracidade</span> dos dados?
            </h2>
            <p class="mt-6 text-lg text-muted-foreground leading-relaxed">
              O Fiscaliza Brasil não cria dados. Nós consumimos informações diretamente das <strong>APIs Oficiais</strong> 
              da Câmara dos Deputados, do Senado Federal e do Portal da Transparência.
            </p>
            
            <div class="mt-10 space-y-6">
              <div v-for="point in points" :key="point.title" class="flex gap-4">
                <div class="p-2 h-fit rounded-lg bg-muted text-primary">
                  <component :is="point.icon" class="h-5 w-5" />
                </div>
                <div>
                  <h3 class="font-bold text-foreground">{{ point.title }}</h3>
                  <p class="text-sm text-muted-foreground mt-1">{{ point.description }}</p>
                </div>
              </div>
            </div>

            <div class="mt-10">
              <BaseButton to="/metodologia" size="lg" variant="default" class="group">
                Conhecer Metodologia Completa
                <ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
              </BaseButton>
            </div>
          </div>

          <div class="relative hidden lg:block">
            <div class="absolute -inset-4 bg-gradient-to-tr from-primary/20 to-secondary/20 rounded-full blur-3xl opacity-30 animate-pulse" />
            <div class="relative bg-muted/50 rounded-2xl border border-border/50 p-8">
              <div class="space-y-4">
                <div v-for="i in 3" :key="i" class="h-4 bg-muted-foreground/10 rounded-full w-full animate-pulse" :style="{ width: 100 - (i * 15) + '%' }" />
              </div>
              <div class="mt-8 flex justify-center">
                <Database class="h-32 w-32 text-primary/20" />
              </div>
              <div class="mt-8 grid grid-cols-2 gap-4">
                <div class="h-10 bg-primary/10 rounded-lg border border-primary/20" />
                <div class="h-10 bg-muted rounded-lg" />
              </div>
            </div>
            <!-- Decorative Badge -->
            <div class="absolute -bottom-6 -right-6 bg-background rounded-2xl border border-border p-4 shadow-xl animate-bounce">
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 rounded-full bg-green-500/10 flex items-center justify-center">
                  <RefreshCcw class="h-5 w-5 text-green-500" />
                </div>
                <div>
                  <p class="text-[10px] uppercase tracking-wider font-bold text-muted-foreground">Atualização</p>
                  <p class="text-sm font-bold text-foreground">Diária Automática</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ShieldCheck, Database, RefreshCcw, Search, Code, ArrowRight } from 'lucide-vue-next'
import BaseButton from '@/components/ui/BaseButton.vue'

const points = [
  {
    title: 'Fontes Oficiais',
    description: 'Conectamos diretamente com os portais de Dados Abertos do Governo Federal.',
    icon: Database
  },
  {
    title: 'Código Aberto',
    description: 'Nossa metodologia de processamento é pública e pode ser auditada por qualquer um.',
    icon: Code
  },
  {
    title: 'Sem Interferência',
    description: 'Apresentamos os números brutos, sem filtros partidários ou edições ideológicas.',
    icon: Search
  }
]
</script>
