<template>
    <div v-if="gameOver" class="my-2 text-white text-center">
        <p v-if="hasWon">You got it!</p>
        <p v-else-if="gameOver">Oh no! The answer was <b>{{ gameDetails.title }}</b></p>

        <p>The answer was <a class="underline" :href="gameUrl">{{ gameDetails.title }}</a></p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { gameOver, hasWon, store } from '../store';

export default defineComponent({
  name: 'CompletionMessage',

  computed: {
    gameDetails() {
      return store.gameDetails;
    },

    gameUrl(): string {
      return `https://store.steampowered.com/app/${this.gameDetails.steamId}`;
    },

    gameOver() {
      return gameOver();
    },

    hasWon() {
      return hasWon();
    },
  },
});
</script>
