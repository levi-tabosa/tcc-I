<template>
  <header class="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
    <nav class="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8">
      <div class="flex lg:flex-1">
        <router-link to="/" class="-m-1.5 p-1.5 flex items-center gap-2">
          <div class="flex h-10 w-10 items-center justify-center">
            <img src="/logo.svg" alt="Logo" class="h-10 w-10 object-contain" />
          </div>
          <span class="hidden sm:block font-bold text-lg text-foreground">Fiscaliza Brasil</span>
        </router-link>
      </div>

      <!-- Mobile menu button -->
      <div class="flex lg:hidden">
        <button
          type="button"
          class="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-foreground"
          @click="mobileMenuOpen = true"
        >
          <span class="sr-only">Abrir menu</span>
          <Menu class="h-6 w-6" />
        </button>
      </div>

      <!-- Desktop nav -->
      <div class="hidden lg:flex lg:gap-x-8">
        <router-link
          v-for="item in navigation"
          :key="item.name"
          :to="item.href"
          class="text-sm font-semibold leading-6 transition-colors hover:text-primary"
          :class="$route.path === item.href ? 'text-primary' : 'text-muted-foreground'"
        >
          {{ item.name }}
        </router-link>
      </div>

      <div class="hidden lg:flex lg:flex-1 lg:justify-end lg:gap-x-4">
      </div>
    </nav>

    <!-- Mobile menu -->
    <Transition name="slide">
      <div v-if="mobileMenuOpen" class="lg:hidden fixed inset-0 z-50">
        <div class="fixed inset-0 bg-black/50" @click="mobileMenuOpen = false" />
        <div class="fixed inset-y-0 right-0 w-full max-w-sm bg-background px-6 py-6 overflow-y-auto">
          <div class="flex items-center justify-between">
            <router-link to="/" class="-m-1.5 p-1.5 flex items-center gap-2">
              <div class="flex h-10 w-10 items-center justify-center">
                <img src="/logo.svg" alt="Logo" class="h-10 w-10 object-contain" />
              </div>
            </router-link>
            <button type="button" class="-m-2.5 rounded-md p-2.5 text-foreground" @click="mobileMenuOpen = false">
              <X class="h-6 w-6" />
            </button>
          </div>
          <div class="mt-6 flow-root">
            <div class="-my-6 divide-y divide-border">
              <div class="space-y-2 py-6">
                <router-link
                  v-for="item in navigation"
                  :key="item.name"
                  :to="item.href"
                  class="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 transition-colors hover:bg-muted"
                  :class="$route.path === item.href ? 'text-primary bg-muted' : 'text-foreground'"
                  @click="mobileMenuOpen = false"
                >
                  {{ item.name }}
                </router-link>
              </div>
              <div class="py-6 flex items-center gap-4">
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Menu, X } from 'lucide-vue-next'

const navigation = [
  { name: 'Home', href: '/' },
  { name: 'Deputados', href: '/deputados' },
  { name: 'Despesas', href: '/despesas' },
  { name: 'Emendas', href: '/emendas' },
  { name: 'Rankings', href: '/rankings' },
  { name: 'Metodologia', href: '/metodologia' },
]

const mobileMenuOpen = ref(false)
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.2s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
}
</style>
