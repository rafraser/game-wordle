<template>
    <div v-if="gameOver" class="my-2 text-white text-center">
        <p v-if="hasWon">You got it!</p>
        <p v-else-if="gameOver">Oh no! The answer was <b>{{ gameDetails.title }}</b></p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { gameOver, hasWon } from '../store';

export default defineComponent({
  name: 'CompletionMessage',

  computed: {
    gameOver() {
      return gameOver();
    },

    hasWon() {
      return hasWon();
    },
  },
});
</script>
