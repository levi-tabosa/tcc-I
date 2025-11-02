import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Perfil from '../views/Perfil.vue'
import Parlamentares from '../views/Parlamentares.vue'
import Dashboard from '../views/Dashboard.vue'
import Metodologia from '../views/Metodologia.vue'
import Contato from '../views/Contato.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    // O ":id" é um parâmetro dinâmico. Qualquer valor ali corresponderá a esta rota.
    // Ex: /perfil/123, /perfil/abc, etc.
    path: '/perfil/:id',
    name: 'Perfil',
    component: Perfil
  },
  {
    path: '/parlamentares',
    name: 'Parlamentares',
    component: Parlamentares
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  }, 
  {
    path: '/metodologia',
    name: 'Metodologia',
    component: Metodologia
  },
  {
    path: '/contato',
    name: 'Contato',
    component: Contato
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router