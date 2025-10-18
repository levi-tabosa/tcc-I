import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Perfil from '../views/Perfil.vue' // Corrigido para corresponder ao seu nome de arquivo

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
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router