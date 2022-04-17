<template>
    <div class="h-full w-full bg-gray-800">
        <div class="h-full max-w-xl mx-auto flex flex-col px-10 bg-gray-900">
            <Header/>

            <div v-if="ready" id="game">
              <GameDetailsDisplay></GameDetailsDisplay>
              <PreviousGuesses></PreviousGuesses>
              <GuessInput></GuessInput>
              <CompletionMessage></CompletionMessage>
            </div>

            <Footer/>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import GameDetailsDisplay from './components/GameDetailsDisplay.vue';
import PreviousGuesses from './components/PreviousGuesses.vue';
import CompletionMessage from './components/CompletionMessage.vue';
import GuessInput from './components/GuessInput.vue';
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';

import { store, loadLocalStorage, saveToLocalStorage } from './store';
import { getGameToday, getGameDetails } from './games';

export default defineComponent({
  name: 'App',
  components: {
    GameDetailsDisplay,
    PreviousGuesses,
    GuessInput,
    CompletionMessage,
    Header,
    Footer,
  },

  async mounted() {
    const today = getGameToday();
    store.today = today;

    const state = loadLocalStorage();
    if (state && today === state.today) {
      store.guesses = state.guesses;
    } else {
      saveToLocalStorage();
    }

    // Fetch game details for today
    const details = await getGameDetails(today);
    store.gameDetails = details;
  },

  computed: {
    ready() {
      return store.gameDetails.title !== '';
    },
  },
});
</script>
