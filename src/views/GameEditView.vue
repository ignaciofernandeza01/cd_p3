<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getGame, updateGame } from '@/services/juegos'

const route = useRoute()
const router = useRouter()
const id = Number(route.params.id)

const cargando = ref(true)
const guardando = ref(false)
const errorForm = ref('')
const form = reactive({
  nombre: '',
  categoria: '',
  popularidad: 0,
  link: '',
  foto: '',
  trailer: '',
  descripcion: ''
})

onMounted(async () => {
  try {
    const data = await getGame(id)
    Object.assign(form, data)
  } catch {
    errorForm.value = 'No se pudo cargar el juego'
  } finally {
    cargando.value = false
  }
})

async function guardar() {
  errorForm.value = ''
  if (!form.nombre.trim()) {
    errorForm.value = 'El nombre es obligatorio'
    return
  }
  guardando.value = true
  try {
    await updateGame(id, form)
    router.push({ name: 'games' })
  } catch  {
    errorForm.value = 'Error al guardar los cambios'
  } finally {
    guardando.value = false
  }
}

function cancelar() {
  router.back()
}
</script>

<template>
  <section class="form-card page">
    <h2>Editar juego</h2>

    <div v-if="cargando">Cargando datos...</div>

    <div v-else class="grid">
      <label>Nombre*       <input v-model="form.nombre" required /></label>
      <label>Categoría     <input v-model="form.categoria" /></label>
      <label>Popularidad   <input v-model.number="form.popularidad" type="number" min="0" max="5" /></label>
      <label>Link          <input v-model="form.link" /></label>
      <label>Foto (URL)    <input v-model="form.foto" /></label>
      <label>Trailer (URL) <input v-model="form.trailer" /></label>
      <label class="full">Descripción <textarea v-model="form.descripcion" rows="4" /></label>
    </div>

    <p v-if="errorForm" class="error">{{ errorForm }}</p>

    <div class="actions">
      <button :disabled="guardando" @click="guardar">
        {{ guardando ? 'Guardando…' : 'Guardar cambios' }}
      </button>
      <button @click="cancelar">Cancelar</button>
    </div>
  </section>
</template>

<style scoped>
.page {
  max-width: 760px;
  margin: 1.5rem auto;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.7); /* Fondo semitransparente */
  border-radius: .5rem;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.form-card {
  padding: 1rem;
  background: #ffffff;
  border-radius: .5rem;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.full {
  grid-column: 1 / -1;
}

label {
  font-size: 16px;
  color: #333;
  font-weight: 600;
  margin-bottom: 8px;
}

input, textarea {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 2px solid #e5e7eb;
  font-size: 16px;
  color: #333;
  background-color: #f9fafb;
  box-sizing: border-box;
}

input:focus, textarea:focus {
  border-color: #161e62;
  outline: none;
  background-color: #ffffff;
}

textarea {
  resize: vertical;
}

button {
  background-color: #161e62;
  color: white;
  border-radius: 4px;
  border: none;
  padding: 10px 16px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin: 8px 0;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover {
  background-color: #00043a;
  transform: translateY(-5px);
}

.error {
  color: #e5534b;
  margin-top: 10px;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}

</style>
