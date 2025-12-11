<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/axios.js";  // o "../services/axios"

const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();
const route = useRoute();

async function submit() {
  error.value = "";
  try {
    const { data } = await api.post("/auth/login", { email: email.value, password: password.value });
    localStorage.setItem("token", data.access_token);
    router.replace(route.query.redirect?.toString() || "/games");
  } catch (e) {
    error.value = e?.response?.data?.msg || "Error al iniciar sesión";
  }
}
</script>

<template>
  <h1>🎮INICIO DE SESIÓN🎮</h1>

  <form @submit.prevent="submit">
    <div>
      <label>Email</label><br />
      <input v-model="email" type="email" required />
    </div>
    <div style="margin-top: 8px">
      <label>Contraseña</label><br />
      <input v-model="password" type="password" required />
    </div>
    <button style="margin-top: 12px">Entrar</button>
  </form>

  <p v-if="error" style="color:crimson; margin-top:10px; text-align: center;">{{ error }}</p>

  <div class="register">
      <p style="margin-top:10px">
      ¿No tienes cuenta?
      <router-link :to="{ name: 'register' }">Regístrate aqui!</router-link>
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
  width: 100%;  /* Que los inputs ocupen todo el espacio disponible dentro del contenedor */
  max-width: 350px;  /* Limita el ancho de los inputs */
  padding: 12px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
}

button {
  width: 100%;  /* Que el botón ocupe todo el ancho del contenedor */
  max-width: 350px;  /* Limita el ancho del botón */
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
  transform: translateY(-3px);
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

.register p{
  text-align: center;
  color: white;
  font-size: 20px;

}


.register a {
  color: white; /* Color blanco para el enlace */
  text-decoration: none; /* Sin subrayado */
}

.register a:hover {
  text-decoration: underline; /* Subrayado al pasar el ratón */
}

label{
  font-size: 20px;
}
</style>
