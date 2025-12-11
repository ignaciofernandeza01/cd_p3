<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'

const board   = ref(Array(9).fill(null))
const current = ref('X')
const winner  = ref(null)

const lines = [
  [0,1,2],[3,4,5],[6,7,8],
  [0,3,6],[1,4,7],[2,5,8],
  [0,4,8],[2,4,6]
]

const isDraw = computed(() => board.value.every(Boolean) && !winner.value)
const status = computed(() =>
  winner.value ? `¡GANADOOOOR ${winner.value}!` : (isDraw.value ? 'EMPATE 🤝' : `TURNO DE ${current.value}`)
)

function checkWinner(p) {
  return lines.some(([a,b,c]) => board.value[a]===p && board.value[b]===p && board.value[c]===p)
}
function play(i) {
  if (winner.value || isDraw.value || board.value[i]) return
  board.value[i] = current.value
  if (checkWinner(current.value)) { winner.value = current.value; return }
  current.value = current.value === 'X' ? 'O' : 'X'
}
function resetGame() {
  board.value = Array(9).fill(null)
  current.value = 'X'
  winner.value = null
}
</script>

<template>
  <section class="ttt">
    <header class="topbar">
      <h2>TIC TAC TOE</h2>
      <div class="botones_tictac">
        <RouterLink class="back" :to="{ name: 'games' }">← Volver</RouterLink>
        <button class="reset" @click="resetGame">Reiniciar</button>
      </div>

    </header>

    <h2 class="estado">{{ status }}</h2>


    <div class="board">
      <div class="grid-ttt">
        <button v-for="(cell, i) in board" :key="i" class="cell" @click="play(i)">{{ cell }}</button>
      </div>
    </div>
  </section>
</template>




