<script setup>
    import { ref } from 'vue'
    import { computed } from 'vue'
    import {onMounted } from 'vue'

    import { listGames, deleteGame } from '@/services/juegos'


    const busqueda = ref('')
    const juegos = ref([])              // ← ahora viene del backend
    const abierto = ref(null)
    const mostrarBotones = ref(false)
    const tituloPortal = ref('portalJuegos')
    const mostrarCategorias = ref(false)
    const juegosOriginal = ref([...juegos.value])



    const juegosFiltrados = computed(() => {
        const q = busqueda.value.toLowerCase()
        if (!q) return juegos.value

        return juegos.value.filter(j =>
          j.nombre.toLowerCase().includes(q)
        )
      })



// POPOVER DESCRIPCION
      function toggleDescripcion(id) {
      abierto.value = (abierto.value === id) ? null : id
    }


// FUNCIONES PARA ORDENAR
    function ordenAlfabetico() {
        juegos.value.sort((a, b) => a.nombre.localeCompare(b.nombre))
      }

      function ordenAlfabeticoInverso() {
        juegos.value.sort((a, b) => b.nombre.localeCompare(a.nombre))
      }
      function ordenPopularidad() {

        juegos.value.sort((a, b) => b.popularidad - a.popularidad)

      }

      function ordenOriginal() {

        juegos.value.sort((a, b) => a.id - b.id)
      }


      function mostrarOrden() {
        mostrarBotones.value = !mostrarBotones.value

      }


//FUNCION PARA FILTRAR CATEGORÍAS
    function categoriaSeleccionada(categoria) {
      if (categoria === 'Todas') {
        juegos.value = [...juegosOriginal.value]
        return
      }
      juegos.value = juegosOriginal.value.filter(juego => juego.categoria === categoria)
    }

    function mostrarCategoria() {
      mostrarCategorias.value = !mostrarCategorias.value
    }


// KEYWORDS PARA BARRA DE PALABRAS CLAVE
    //Con este diccionario evitaremos que se cuenten conectores que aparecen en todas las descripciones siempre
    const STOPWORDS_ES = new Set([
      'a','acá','ahí','al','algo','algunas','algunos','allá','allí','ante','antes','aquel','aquella','aquellas','aquellos','aqui','aquí',
      'asi','así','aun','aunque','cada','casi','como','con','contra','cual','cuales','cualquier','cualesquiera','cuan','cuando','cuanto',
      'de','debe','deben','deber','del','desde','donde','dos','el','ella','ellas','ellos','en','entonces','entre','era','erais','eran',
      'eres','es','esa','esas','ese','eso','esos','esta','estaba','estaban','estado','estamos','estar','estas','este','esto','estos',
      'etc','fue','fueron','ha','haber','habrá','había','hace','hacen','hacer','hacia','han','hasta','hay','incluso','la','las','le','les',
      'lo','los','mas','más','me','mi','mis','mismo','mucha','muchas','mucho','muchos','muy','nada','ni','no','nos','nosotros','nuestra',
      'nuestras','nuestro','nuestros','o','otra','otras','otro','otros','para','pero','poco','por','porque','que','qué','quien','quienes',
      'se','segun','según','ser','si','sí','sin','sobre','solo','sólo','son','su','sus','tal','tambien','también','tan','tanto','te','tener',
      'ti','tiene','tienen','todo','todos','tu','tus','un','una','uno','unos','usted','ustedes','ya','y'
    ])

    //Utilizamos un porcentaje de juesgos en los q aparece la palabra, porque si utilizamos que aparezca en todos los juegos apenas obtenemos palabras
        //0.6 = 60% ; 1 = 100%
        const PORCENTAJE = 0.6
        const keywords = computed(() => {
        const visibles = juegosFiltrados.value
        if (!visibles.length) return []

        // frecuencia por palabra
        const docFreq = new Map()
        visibles.forEach(j => {
          const setPalabras = new Set(dividir_texto(j.descripcion || ''))
          setPalabras.forEach(w => {
            docFreq.set(w, (docFreq.get(w) || 0) + 1)
          })
        })

        const minDocs = Math.max(1, Math.ceil(visibles.length*PORCENTAJE))
        const candidatos = [...docFreq.entries()]
          .filter(([,count]) => count >= minDocs)
          // ordena por frecuencia desc y luego alfabético
          .sort((a,b) => b[1]-a[1] || a[0].localeCompare(b[0]))
          .map(([w]) => w)

        return candidatos
      })



    function normalizar(texto) {
      return texto
        .toLowerCase()
        .normalize('NFD').replace(/[\u0300-\u036f]/g,'')   // quita tildes
        .replace(/[^a-z0-9ñáéíóúü\s]/gi,' ')              // signos → espacio
        .replace(/\s+/g,' ')                               // colapsa espacios
        .trim()}

    function dividir_texto(texto) {
      const words = normalizar(texto).split(' ')           // Divide el texto en palabras
      return words.filter(w =>
        w.length > 2 && !STOPWORDS_ES.has(w)             // Quita palabras cortas y stopwords
      )
    }

// CRUD: añadir / editar / borrar

    async function cargar(q = '') {
      const data = await listGames(q)   // ← pide al backend
      juegos.value = data
      juegosOriginal.value = [...data]  // refresca copia base
    }
  // al abrir la vista, carga
    onMounted(() => cargar())

// =====================

    async function borrarJuego(id) {
      if (!confirm('¿Eliminar este juego?')) return
      await deleteGame(id)
      await cargar(busqueda.value)
    }


</script>




<template>

<section>
<main>
    <h1 :class="tituloPortal">PORTAL DE JUEGOS</h1>
  </main>

  <div class = "buscador" >

    <label for="busqueda">Buscar juego:</label>
    <input v-model="busqueda"/>

  </div>

  <div class="ordenar">
    <button @click="mostrarOrden">ORDENAR POR</button>
      <div class="ordenar_botones" v-if="mostrarBotones">
        <button @click="ordenAlfabetico">A → Z</button>
        <button @click="ordenAlfabeticoInverso">Z → A</button>
        <button @click="ordenPopularidad">Popularidad</button>
        <button @click="ordenOriginal">Orden Original</button>
      </div>
  </div>

  <div class="categorias">
      <button @click="mostrarCategoria">CATEGORÍAS</button>
      <div class="categoria_botones" v-if="mostrarCategorias">
        <button @click="categoriaSeleccionada('Acción')">Acción</button>
        <button @click="categoriaSeleccionada('Aventura')">Aventura</button>
        <button @click="categoriaSeleccionada('Deportes')">Deportes</button>
        <button @click="categoriaSeleccionada('Estrategia')">Estrategia</button>
        <button @click="categoriaSeleccionada('Todas')">Todas</button>
      </div>
  </div>

  <div class = "añadir_juego">
      <RouterLink :to="{ name: 'game-new' }" v-slot="{ navigate }">
        <button class="btn-add" @click="navigate">+ AÑADIR JUEGO</button>
    </RouterLink>
  </div>

  <h2 id="Titulo_juegos">LISTA DE JUEGOS</h2>
  <div class= "juegos">
    <ul>
      <li v-for="juego in juegosFiltrados" :key="juego.id">

          <div class="card">
            <h1 class = "titulo">{{ juego.nombre }}</h1>
                    <template v-if="juego.nombre === 'TicTacToe'">
                      <img :src="juego.foto" :alt="`Portada de ${juego.nombre}`" />

                      <div class="btn-row">
                        <RouterLink class="btn-desc" :to="{ name: 'tictactoe' }">JUGAR</RouterLink>
                        <button class="btn-desc" @click.stop="toggleDescripcion(juego.id)" :aria-expanded="abierto === juego.id">SABER MÁS</button>
                      </div>

                      <div v-if="abierto === juego.id" class="popover" role="dialog" :aria-label="`Descripción de ${juego.nombre}`">
                        <button class="close" @click.stop="abierto = null" aria-label="Cerrar">×</button>
                        <p>{{ juego.descripcion }}</p>
                        <h3>POPULARIDAD (0–5): {{ juego.popularidad }}</h3>
                      </div>
                    </template>


                 <template v-else>
                    <a :href="juego.link" target="_blank" class="cover-link">
                      <img :src="juego.foto" :alt="`Portada de ${juego.nombre}`" />
                    </a>

                    <button class="btn-desc" @click.stop="toggleDescripcion(juego.id)" :aria-expanded="abierto === juego.id">SABER MÁS</button>

                    <div v-if="abierto === juego.id" class="popover" role="dialog" :aria-label="`Descripción de ${juego.nombre}`">
                      <button class="close" @click.stop="abierto = null" aria-label="Cerrar">×</button>
                      <p>{{ juego.descripcion }}</p>
                      <h3>POPULARIDAD (0–5): {{ juego.popularidad }}</h3>
                      <a :href="juego.trailer" target="_blank"><button class="trailer">TRAILER</button></a>
                    </div>

                            <!-- CRUD -->
                    <div class="crud-row">
                      <RouterLink class="btn-edit" :to="{ name: 'game-edit', params: { id: juego.id } }">Editar</RouterLink>
                      <button class="danger" @click="borrarJuego(juego.id)">Eliminar</button>
                    </div>

                </template>





          </div>
      </li>
    </ul>

    <footer class="keywords-footer" v-if="keywords.length">
        <h3>Keywords</h3>
        <ul class="keywords">
          <li v-for="k in keywords" :key="k">#{{ k }}</li>
        </ul>
    </footer>


  </div>





</section>
</template>

