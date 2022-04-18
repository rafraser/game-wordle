<template>
    <img class="w-full rounded-md my-2 aspect-video" alt="Video game screenshot" :src="url">

    <div class="flex justify-center my-2">
        <button
            v-for="index in imageCount" :key="index" :class="{ 'bg-green-700': selected === index, 'bg-green-500': selected !== index }"
            class="hover:bg-green-700 text-white font-bold p-2 mx-2 rounded aspect-square" @click="select(index)"
        >
            {{ index }}
        </button>
    </div>

    <div v-if="imageCount >= 3" class="text-center text-md my-2">
        <div v-for="tag in tags" :key="tag.index" class="h-full inline-block border-2 border-green-700 text-white p-2 mx-2 rounded">{{ tag }}</div>
    </div>
    <div v-else class="my-2"></div>

    <div v-if="imageCount >= 4" class="text-center text-white text-md my-2">
        <p>Released in {{ releaseYear }}</p>
    </div>
    <div v-else class="my-2"></div>

    <div v-if="imageCount >= 5" class="flex flex-col justify-start text-white text-center text-sm my-2">
        <p>{{ description }}</p>
    </div>
    <div v-else class="my-2"></div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { gameOver, store } from '../store';

export default defineComponent({
  name: 'Gallery',

  data() {
    return { selected: 1 };
  },

  methods: {
    select(number: number) {
      this.selected = number;
    },
  },

  watch: {
    imageCount() {
      if (gameOver()) return;
      this.selected = store.guesses.length + 1;
    },
  },

  computed: {
    url(): string {
      return `/assets/${store.today}/${this.selected}.jpg`;
    },

    imageCount(): number {
      if (gameOver()) return 6;
      return store.guesses.length + 1;
    },

    description() {
      return store.gameDetails.description;
    },

    releaseYear() {
      return store.gameDetails.releaseYear;
    },

    tags() {
      return store.gameDetails.tags;
    },
  },
});
</script>
