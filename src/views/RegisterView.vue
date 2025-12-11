<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/axios.js";  // o "../services/axios"

const email = ref("");
const password = ref("");
const confirm = ref("");
const error = ref("");
const ok = ref("");
const loading = ref(false);
const router = useRouter();

function validate() {
  if (!email.value.trim() || !password.value.trim()) return "email y password son obligatorios";
  if (password.value.length < 8) return "la contraseña debe tener al menos 8 caracteres";
  if (password.value !== confirm.value) return "las contraseñas no coinciden";
  return null;
}

async function submit() {
  error.value = ""; ok.value = "";
  const msg = validate();
  if (msg) { error.value = msg; return; }
  loading.value = true;
  try {
    const body = { email: email.value.trim().toLowerCase(), password: password.value };
    const r = await api.post("/auth/register", body);
    if (r.status === 201) {
      ok.value = "Usuario creado. Ve al login.";
      // Redirige al login y pre-rellena el email
      router.replace({ name: "login", query: { email: email.value } });
    }
  } catch (e) {
    // tu backend devuelve 409 si el email existe
    error.value = e?.response?.data?.msg || "No se pudo registrar";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <h1>🎮CREAR CUENTA🎮</h1>

  <form @submit.prevent="submit">
    <label>Email</label>
    <input v-model="email" type="email" required />

    <label style="margin-top:8px">Contraseña</label>
    <input v-model="password" type="password" minlength="8" required />

    <label style="margin-top:8px">Repite contraseña</label>
    <input v-model="confirm" type="password" minlength="8" required />

    <button style="margin-top:12px" :disabled="loading">
      {{ loading ? "Creando..." : "Registrarme" }}
    </button>
  </form>

  <p v-if="error" style="color:crimson; margin-top:10px">{{ error }}</p>
  <p v-if="ok" style="color:seagreen; margin-top:10px">{{ ok }}</p>


  <div class="inicio">
      <p style="margin-top:10px">
        ¿Ya tienes cuenta?
        <router-link :to="{ name: 'login' }">Inicia sesión</router-link>
      </p>
  </div>
</template>

<style scoped>


form {
  display: flex;
  flex-direction: column;
  align-items: center;  /* Centra los elementos horizontalmente */
  justify-content: center; /* Centra los elementos verticalmente */
  width: 100%;  /* Usa el 100% del ancho disponible */
  max-width: 300px;  /* Limita el ancho máximo de los inputs */
  margin: 0 auto;  /* Centra el formulario horizontalmente */
  padding: 40px;
  background-color: rgba(255, 255, 255, 0.8); /* Fondo blanco semi-transparente */
  border-radius: 8px; /* Bordes redondeados */

}


input {
  width: 100%;  /* Ensure inputs take up the full width */
  max-width: 350px;  /* Limit the width of the inputs */
  padding: 12px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
}

button {
  width: 100%;  /* Ensure the button takes up the full width */
  max-width: 350px;  /* Limit the button width */
  padding: 12px;
  border-radius: 8px;
  background-color: #161e62;
  color: white;
  font-size: 18px;
  margin-top: 10px;
  cursor: pointer;
  border: none;
}

button:hover {
  background-color: #00043a;
  transform: translateY(-3px); /* Hover effect */
}


h1{
  text-align: center;
  font-size: 80px;
  font-family: 'Segoe UI';
  color: rgb(13, 28, 72);
  margin-top: 20px;
  font-weight: 800;
  -webkit-text-stroke: 4px rgb(255, 255, 255);
}



.inicio p{
  text-align: center;
  color: white;
  font-size: 20px;

}


.inicio a {
  color: white; /* Color blanco para el enlace */
  text-decoration: none; /* Sin subrayado */
}

.inicio a:hover {
  text-decoration: underline; /* Subrayado al pasar el ratón */
}

label {
  font-size: 20px;
  text-align: left;
  width: 100%;  /* Make labels take full width */

}

</style>
