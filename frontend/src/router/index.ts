import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Perfil from '../views/Perfil.vue'
import Dashboard from '../views/Dashboard.vue'
import Metodologia from '../views/Metodologia.vue'
import Contato from '../views/Contato.vue'
import Comparativo from '../views/Comparativo.vue'
import Parlamentares from '../views/Parlamentares.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/parlamentares',
    name: 'Parlamentares',
    component: Parlamentares
  },
  {
    path: '/perfil/:id',
    name: 'Perfil',
    component: Perfil
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
  },
  {
    path: '/comparativo',
    name: 'Comparativo',
    component: Comparativo
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router