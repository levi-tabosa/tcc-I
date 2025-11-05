<template>
  <header class="mvp-header">
    <div class="container">
      <nav class="nav">
        <RouterLink to="/" class="brand">
          Transparência BR
        </RouterLink>
        
        <div class="nav-links">
          <RouterLink to="/" class="nav-link">Início</RouterLink>
          <RouterLink to="/parlamentares" class="nav-link">Deputados</RouterLink>
          <RouterLink to="/dashboard" class="nav-link">Dashboard</RouterLink>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.mvp-header {
  background: white;
  border-bottom: 1px solid #eee;
  position: sticky;
  top: 0;
  z-index: 100;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.brand {
  font-size: 1.3rem;
  font-weight: 700;
  color: #007bff;
  text-decoration: none;
}

.brand:hover {
  color: #0056b3;
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  padding: 8px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #007bff;
  border-bottom-color: #007bff;
}

.nav-link.router-link-active {
  color: #007bff;
  border-bottom-color: #007bff;
}

@media (max-width: 768px) {
  .nav-links {
    gap: 20px;
  }
  
  .nav-link {
    font-size: 0.9rem;
  }
}

@media (max-width: 640px) {
  .nav {
    flex-direction: column;
    height: auto;
    padding: 15px 0;
  }
  
  .nav-links {
    margin-top: 10px;
    gap: 15px;
  }
}
</style>