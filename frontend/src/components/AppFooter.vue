<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <!-- Branding -->
        <div class="footer-brand">
          <div class="footer-brand-header">
            <Shield class="footer-icon" />
            <span class="footer-brand-name">
              Fiscaliza Brasil
            </span>
          </div>
          <p class="footer-brand-description">
            Transparência na atuação parlamentar através de dados oficiais e análises acessíveis.
          </p>
        </div>

        <!-- Links -->
        <div class="footer-section">
          <h3 class="footer-section-title">Links</h3>
          <div class="footer-links">
            <RouterLink to="/" class="footer-link">
              Início
            </RouterLink>
            <RouterLink to="/" class="footer-link">
              Parlamentares
            </RouterLink>
            <RouterLink to="/dashboard" class="footer-link">
              Dashboard
            </RouterLink>
            <RouterLink to="/metodologia" class="footer-link">
              Metodologia
            </RouterLink>
          </div>
        </div>

        <!-- Informações -->
        <div class="footer-section">
          <h3 class="footer-section-title">Informações</h3>
          <div class="footer-links">
            <RouterLink to="/contato" class="footer-link">
              Enviar Feedback
            </RouterLink>
            <RouterLink to="/sobre" class="footer-link">
              Sobre o Projeto
            </RouterLink>
            <RouterLink to="/privacidade" class="footer-link">
              Política de Privacidade
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p class="footer-copyright">
          © {{ new Date().getFullYear() }} Fiscaliza Brasil. Dados oficiais da Câmara dos Deputados e Senado Federal.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { Shield } from 'lucide-vue-next'
</script>

<style scoped>
.footer {
  background-color: var(--footer-bg);
  padding: 3rem 0 1.5rem;
  border-top: 1px solid var(--border-primary);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

@media (min-width: 768px) {
  .footer-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.footer-brand-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.footer-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-primary);
}

.footer-brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-primary);
}

.footer-brand-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
}

.footer-section-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  font-size: 1rem;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--color-primary);
}

.footer-bottom {
  border-top: 1px solid var(--border-primary);
  padding-top: 1.5rem;
  text-align: center;
}

.footer-copyright {
  color: var(--text-tertiary);
  font-size: 0.875rem;
  margin: 0;
}
</style>