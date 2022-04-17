<template>
    <button class="w-full bg-green-500 hover:bg-green-700 rounded text-white h-10" @click="share">{{ shareText }}</button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { getGameNumber } from '../games';
import { hasWon, store } from '../store';

export default defineComponent({
  name: 'ShareButton',

  data() {
    return { shareText: 'Share!' };
  },

  methods: {
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
  },
});
</script>
