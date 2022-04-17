<template>
    <div class="h-full w-full bg-gray-800">
        <div class="h-full max-w-xl mx-auto flex flex-col px-10 bg-gray-900">
            <h1 class="text-center text-gray-200">Gamele</h1>

            <Gallery v-if="ready"></Gallery>
            <Guesses v-if="ready"></Guesses>

            <footer class="mt-auto py-2 text-gray-200 text-center">
                made with ❤️ by <a class="underline" href="https://robertafraser.com">Robert A Fraser</a>
            </footer>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import Gallery from './components/Gallery.vue';
import Guesses from './components/Guesses.vue';
import { store, loadLocalStorage, saveToLocalStorage } from './store';
import { getGameToday, getGameDetails } from './games';

export default defineComponent({
  name: 'App',
  components: {
    Gallery,
    Guesses,
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
