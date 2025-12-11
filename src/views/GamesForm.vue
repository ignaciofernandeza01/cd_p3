<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/axios'   // tu axios preconfigurado

const router = useRouter()
const guardando = ref(false)
const errorForm = ref('')

// Modelo del formulario
const form = reactive({
  nombre: '',
  categoria: '',
  popularidad: 0,
  link: '',
  foto: '',
  trailer: '',
  descripcion: ''
})

async function guardar() {
  errorForm.value = ''
  if (!form.nombre.trim()) {
    errorForm.value = 'El nombre es obligatorio'
    return
  }
  guardando.value = true
  try {
    await api.post('/games', form)         // → crea en el backend
    router.push({ name: 'games' })          // vuelve al listado
  } catch (err) {
    if (err.response?.status === 409) {
      errorForm.value = 'Ese nombre ya existe'
    } else {
      errorForm.value = 'Error al guardar el juego'
    }
  } finally {
    guardando.value = false
  }
}

function cancelar() {
  router.back() // o router.push({ name: 'games' })
}
</script>

<template>
  <section class="form-card page">
    <h2>Crear juego</h2>
    <div class="grid">
      <label>Nombre*       <input v-model="form.nombre" required /></label>
      <label>Categoría     <input v-model="form.categoria" /></label>
      <label>Popularidad   <input v-model.number="form.popularidad" type="number" min="0" max="10" /></label>
      <label>Link          <input v-model="form.link" /></label>
      <label>Foto (URL)    <input v-model="form.foto" /></label>
      <label>Trailer (URL) <input v-model="form.trailer" /></label>
      <label class="full">Descripción <textarea v-model="form.descripcion" rows="4" /></label>
    </div>

    <p v-if="errorForm" class="error">{{ errorForm }}</p>

    <div class="actions">
      <button :disabled="guardando" @click="guardar">
        {{ guardando ? 'Guardando…' : 'Guardar' }}
      </button>
      <button @click="cancelar">Cancelar</button>
    </div>
  </section>
</template>


<style scoped>
.page.form-card{
  max-width: 860px;
  margin: 28px auto;
  padding: 22px 24px;
  background: rgba(255,255,255,.96);
  border: 4px solid #ffffff;
  border-radius: 12px;
  box-shadow: 0 14px 36px rgba(0,0,0,.18);
  backdrop-filter: blur(2px);
}

/* Título dentro de la tarjeta: sin trazo blanco del h2 global */
.page.form-card h2{
  margin: 0 0 14px;
  text-align: center;
  font-size: 34px;
  font-weight: 800;
  color: #0d1c48;         /* azul oscuro para contraste en fondo claro */
  -webkit-text-stroke: 0; /* anula el trazo del h2 global */
  text-shadow: none;
}

/* Grid de campos */
.page.form-card .grid{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px 28px;
  align-items: end;
}

/* Etiquetas y campos */
.page.form-card label{
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-weight: 600;
  color: #0d1c48;
}

.page.form-card input,
.page.form-card textarea{
  appearance: none;
  background: #fff;
  border: 3px solid #e8ecff;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 15px;
  color: #0f0b55;         /* mismo tono que usas en la web */
  outline: none;
  transition: border-color .15s ease, box-shadow .15s ease;
}

.page.form-card input:focus,
.page.form-card textarea:focus{
  border-color: #0f0b55;
  box-shadow: 0 0 0 3px rgba(15,11,85,.15);
}

.page.form-card textarea{
  min-height: 110px;
  resize: vertical;
}

/* Campo ancho (Descripción) */
.page.form-card .full{ grid-column: 1 / -1; }

/* Acciones */
.page.form-card .actions{
  display: flex;
  gap: 12px;
  margin-top: 16px;
  justify-content: flex-start;
}

.page.form-card .actions button{
  background-color: #161e62;
  border: 3px solid #ffffff;
  border-radius: 8px;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
  font-size: 16px;
  padding: 10px 18px;
  transition: .2s ease background-color, .2s ease transform, .2s ease color;
}

.page.form-card .actions button:hover{
  background-color: #00043a;
  transform: translateY(-3px);
}

/* Botón secundario (Cancelar) */
.page.form-card .actions button:nth-child(2){
  background: transparent;
  color: #161e62;
  border-color: #161e62;
}

.page.form-card .actions button:nth-child(2):hover{
  background: #161e62;
  color: #fff;
}

/* Mensaje de error */
.page.form-card .error{
  margin-top: 10px;
  color: #e5534b;
  font-weight: 600;
}

/* Responsive */
@media (max-width: 720px){
  .page.form-card{ margin: 16px; padding: 18px; }
  .page.form-card .grid{ grid-template-columns: 1fr; gap: 12px; }
}
</style>
