import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'   // ⬅️ aquí está la magia
  // ⬅️ importa el router

createApp(App)
  .use(router)                  // ⬅️ activa el router
  .mount('#app')
