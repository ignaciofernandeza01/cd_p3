<script setup>
import { ref } from 'vue'
import './style.css'
const busqueda = ref('')

const juegos = ref([
  { id: 1, nombre: 'EA FC26' , foto: "/public/fc26.jpg" , link : "https://www.ea.com/es-es/games/fifa/fc-26" },
  { id: 2, nombre: 'NBA 2K26',foto: "/public/2k26.jpg" , link : "https://nba.2k.com/es-ES/2k26/"  },
  { id: 3, nombre: 'Clash Royale', foto: "/public/clash.jpg" , link : "https://clashroyale.com/es/"  },
  { id: 4, nombre: 'Call of Duty Modern Warfare VI', foto: "/public/cod.jpg" , link : "https://www.callofduty.com/es/"  },
  { id: 5, nombre: 'Fortnite', foto: "/public/fortnite.jpg" , link : "https://www.epicgames.com/fortnite/es-ES/home"  },
  { id: 6, nombre: 'Minecraft', foto: "/public/minecraft.jpg" , link : "https://www.minecraft.net/es-es"  },
  { id: 7, nombre: 'F1 2025', foto: "/public/f1.jpg" , link : "https://www.ea.com/es/games/f1/f1-25"  },
  { id: 8, nombre: 'MotoGP 2025', foto: "/public/motogp.jpg" , link : "https://milestone.it/es/games/motogp-25/"  },
  { id: 9, nombre: 'GTA V' , foto: "/public/gta.jpg" , link : "https://www.rockstargames.com/es/games/gta-v" },
  { id: 10, nombre: 'Plants vs Zombies',foto: "/public/plants_vs_zombies.jpg" , link : "https://www.ea.com/es-es/games/plants-vs-zombies"  },
  { id: 11, nombre: 'FAR CRY 6', foto: "/public/farcry.jpg" , link : "https://www.ubisoft.com/es-es/game/far-cry/far-cry-6"  },
  { id: 12, nombre: 'eFOOTBALL 2026', foto: "/public/efootball.jpg" , link : "https://www.konami.com/efootball/es/"  },
  { id: 13, nombre: 'Tom Clancys Rainbow Six: Siege', foto: "/public/rainbow.jpg" , link : "https://www.ubisoft.com/es-es/game/rainbow-six/siege"  },
  { id: 14, nombre: 'Score! Hero 2', foto: "/public/score_hero.jpg" , link : "https://score-hero.softonic.com/android"  },
  { id: 15, nombre: 'Subway Surfers', foto: "/public/subway-surfers.jpg" , link : "https://subwaysurfersonline.io/"  },
  { id: 16, nombre: 'Gang Beasts', foto: "/public/gang_beasts.jpg" , link : "https://gangbeasts.game/"  },
  { id: 17, nombre: 'Parchis STAR', foto: "/public/parchis.jpg" , link : "https://parchisi-star-online.softonic.com/android"  },
  { id: 18, nombre: 'Fall Guys', foto: "/public/fall.jpg" , link : "https://www.fallguys.com/es-ES"  },

])
</script>


<template>
  
  <main>
    <h1 style="text-align: center;">Portal de juegos</h1>
  </main>

  <div class = "buscador" >
    <div class = "busq">
      <label for="busqueda" style="margin-right: 10px;">Buscar:</label>
      <input v-model="busqueda"/>
    </div>

    <!-- Mostramos lo que escribe el usuario -->
    <p style="margin-top: 10px">
      Estás buscando: <strong>{{ busqueda }}</strong>
    </p>

  </div>
  <h2 id="Titulo_juegos">Lista de juegos</h2>
  <div class= "juegos">
    <ul>
      <li v-for="juego in juegos" :key="juego.id">
        <div class = "card" href= "{{ juego.link }}">
          
          <h1 class = "titulo">{{ juego.nombre }}</h1>
          <img :src="juego.foto" alt="foto del juego"/>
        </div>
        

      </li>
    </ul>
  </div>

</template>
