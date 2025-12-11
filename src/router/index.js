// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

// Carga de las vistas
import  LoginView from '../views/LoginView.vue';
import RegisterView from '../views/RegisterView.vue';
import PortalJuegos from '../views/PortalJuegos.vue';
import TicTacToe from '../views/TicTacToe.vue';
import GameEditView from '../views/GameEditView.vue';
import GameFormView from '../views/GamesForm.vue'  // <- nombre correcto del archivo


const routes = [
  // Entrada: redirige al login
  { path: '/', redirect: '/login' },

  // Rutas públicas
  { name: 'login',    path: '/login',    component: LoginView,    meta: { public: true } },
  { name: 'register', path: '/register', component: RegisterView, meta: { public: true } },

  // Rutas protegidas (requieren JWT)
  { name: 'games',     path: '/games',              component: PortalJuegos, meta: { requiresAuth: true } },
  { name: 'tictactoe', path: '/jugar/tictactoe',    component: TicTacToe,    meta: { requiresAuth: true } },
  { name: 'game-new', path: '/games/new', component: GameFormView, meta: { requiresAuth: true } },
  { name: 'game-edit', path: '/games/:id/edit', component: GameEditView, meta: { requiresAuth: true } }, ]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

/**
 * Guardia global
 * - Si la ruta requiere auth y NO hay token → redirige a /login guardando la ruta destino.
 * - Si la ruta es pública y SÍ hay token (ya logueado) → manda al portal de juegos.
 */
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    // intenta volver a donde quería ir tras loguear
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.public && token && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'games' })
  } else {
    next()
  }
})

export default router;
