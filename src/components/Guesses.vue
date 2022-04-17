<template>
    <div v-for="guess in guesses" :key="guess.index" class="bg-gray-700 rounded h-8 w-full mb-2 text-white align-middle px-2">{{ guessEmote(guess)}} {{ guess }}</div>
    <div v-for="index in emptyGuessCount" :key="index" class="bg-gray-700 rounded h-8 w-full mb-2 text-white align-middle px-2"></div>

    <div v-if="gameOver" class="flex w-full">
        <button class="w-full bg-green-500 hover:bg-green-700 rounded text-white h-10" @click="share">{{ shareText }}</button>
    </div>

    <div v-else class="flex w-full">
        <input type="text" class="w-4/5 outline-none rounded p-2 h-10" @keyup.enter="guess" v-model="guessInput" placeholder="Guess the game!">
        <button class="w-1/5 bg-green-500 hover:bg-green-700 ml-2 rounded text-white" @click="guess">Guess</button>
    </div>

    <div class="my-2 text-white text-center">
        <p v-if="hasWon">You got it!</p>
        <p v-else-if="gameOver">Oh no! The answer was <b>{{ gameDetails.title }}</b></p>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { getGameNumber } from '../games';
import {
  makeGuess, gameOver, hasWon, store,
} from '../store';

export default defineComponent({
  name: 'Guesses',

  data() {
    return { guessInput: '', shareText: 'Share!' };
  },

  methods: {
    guess() {
      if (this.guessInput.length < 1) return;
      if (gameOver()) return;

      makeGuess(this.guessInput);
      this.guessInput = '';
    },

    async share() {
      let result = `Gamele #${getGameNumber()} - ${hasWon() ? this.guesses.length : 'X'}/6\n`;
      result += `🎮 ${this.guessEmoji}\n\n`;
      result += 'https://gamele.robertafraser.com';

      await navigator.clipboard.writeText(result);
      this.shareText = 'Copied to clipboard.';
      setTimeout(this.clearShareText, 1000);
    },

    clearShareText() {
      this.shareText = 'Share!';
    },

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

    gameOver() {
      return gameOver();
    },

    hasWon() {
      return hasWon();
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
