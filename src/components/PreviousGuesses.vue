<template>
    <div v-for="guess in guesses" :key="guess.index" class="bg-gray-700 rounded h-8 w-full mb-2 text-white align-middle px-2">{{ guessEmote(guess)}} {{ guess }}</div>
    <div v-for="index in emptyGuessCount" :key="index" class="bg-gray-700 rounded h-8 w-full mb-2 text-white align-middle px-2"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { hasWon, store } from '../store';

export default defineComponent({
  name: 'Guesses',

  methods: {
    guessEmote(guess: string) {
      return guess === store.gameDetails.title ? '✔️' : '❌';
    },
  },

  computed: {
    guesses() {
      return store.guesses;
    },

    guessEmoji() {
      let string = '🟧'.repeat(hasWon() ? store.guesses.length - 1 : 6);
      string += '🟩'.repeat(hasWon() ? 1 : 0);
      string += '⬛'.repeat(6 - store.guesses.length);
      return string;
    },

    emptyGuessCount() {
      return 6 - store.guesses.length;
    },

    gameDetails() {
      return store.gameDetails;
    },
  },
});
</script>
