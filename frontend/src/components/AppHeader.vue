<template>
  <header class="header">
    <div class="container">
      <nav class="nav">
        <RouterLink to="/" class="nav-brand">
          <Shield class="nav-icon" />
          <span class="nav-title">
            Fiscaliza Brasil
          </span>
        </RouterLink>
        
        <!-- Desktop Navigation -->
        <div class="nav-links">
          <RouterLink to="/parlamentares" class="nav-link">
            Parlamentares
          </RouterLink>
          <RouterLink to="/comparativo" class="nav-link">
            Comparação
          </RouterLink>  
          <RouterLink to="/dashboard" class="nav-link">
           Dashboard
          </RouterLink>

          <RouterLink to="/metodologia" class="nav-link">
         Metodologia
          </RouterLink>
          <RouterLink to="/contato" class="nav-link">
            Contato
          </RouterLink>
                  
        </div>

        <!-- Mobile Menu Button -->
        <button 
          class="mobile-menu-button"
          @click="toggleMobileMenu"
          aria-label="Menu de navegação"
        >
          <Menu class="menu-icon" />
        </button>

        <!-- Mobile Menu -->
        <div 
          v-if="isMobileMenuOpen"
          class="mobile-menu"
        >
          <div class="mobile-menu-content">
            <RouterLink to="/" class="mobile-nav-link" @click="closeMobileMenu">
              Início
            </RouterLink>
            <RouterLink to="/parlamentares" class="mobile-nav-link" @click="closeMobileMenu">
              Parlamentares
            </RouterLink>
            <RouterLink to="/comparativo" class="mobile-nav-link" @click="closeMobileMenu">
              Comparação
            </RouterLink>
            <RouterLink to="/dashboard" class="mobile-nav-link" @click="closeMobileMenu">
              Dashboard
            </RouterLink>
            <RouterLink to="/metodologia" class="mobile-nav-link" @click="closeMobileMenu">
              Metodologia
            </RouterLink>
            <RouterLink to="/contato" class="mobile-nav-link" @click="closeMobileMenu">
              Contato
            </RouterLink>
            <!-- No theme toggle here anymore -->
          </div>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Shield, Menu } from 'lucide-vue-next'
import { useTheme } from '@/composables/useTheme'

const isMobileMenuOpen = ref(false)
const { theme, toggleTheme } = useTheme()

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--header-bg);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--border-primary);
  box-shadow: var(--shadow-sm);
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: inherit;
  transition: opacity 0.2s ease;
}

.nav-brand:hover {
  opacity: 0.8;
}

.nav-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-primary);
}

.nav-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.nav-links {
  display: none;
  gap: 2rem;
}

@media (min-width: 768px) {
  .nav-links {
    display: flex;
  }
}

.nav-link {
  color: var(--color-gray-600);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
  padding: 0.5rem;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-primary);
}

.mobile-menu-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
}

@media (min-width: 768px) {
  .mobile-menu-button {
    display: none;
  }
}

.menu-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--text-secondary);
}

.mobile-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: var(--surface-primary);
  border-bottom: 1px solid var(--border-primary);
  box-shadow: var(--shadow-lg);
}

@media (min-width: 768px) {
  .mobile-menu {
    display: none;
  }
}

.mobile-menu-content {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.mobile-nav-link {
  padding: 0.75rem 0;
  color: var(--color-gray-600);
  text-decoration: none;
  font-weight: 500;
  border-bottom: 1px solid var(--color-gray-100);
}

.mobile-nav-link:last-child {
  border-bottom: none;
}

.mobile-nav-link:hover,
.mobile-nav-link.router-link-active {
  color: var(--color-primary);
}

</style>
