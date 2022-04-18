<template>
  <div v-if="gameOver" class="flex w-full">
    <ShareButton/>
  </div>

  <div v-else class="flex w-full">
    <div class="w-4/5 relative">
        <div id="autocomplete-items-list" v-if="visible" class="absolute top-auto z-50 w-full mb-2 overflow-y-auto text-lg bg-white rounded bottom-full max-h-36">
            <div
                v-for="(item, index) in filteredItems" :key="item.index" class="overflow-x-clip"
                :class="{ 'bg-gray-200': currentSelectionIndex == index }"
                @mousedown.prevent @click="select(item)" @mouseenter="currentSelectionIndex = index"
            >
                <span class="pl-2">{{ item }}</span>
            </div>
        </div>
        <input
            id="typeahead-select" type="text" class="outline-none rounded h-full w-full p-2" placeholder="Guess the game" :value="input" autocomplete="off"
            @input="onInput" @focus="onFocus" @blur="onBlur" @keydown.down.prevent="onArrowDown" @keydown.up.prevent="onArrowUp" @keydown.enter.tab.prevent="selectCurrent"
        >
    </div>
    <button class="w-1/5 bg-green-500 hover:bg-green-700 ml-2 rounded text-white" @click="guess">Guess</button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import ShareButton from './ShareButton.vue';
import { makeGuess, gameOver } from '../store';

export default defineComponent({
  name: 'GuessTypeahead',
  components: { ShareButton },

  async mounted() {
    const response = await axios.get('/assets/game_titles.json');
    this.items = response.data as string[];
  },

  data() {
    return {
      items: [] as string[],
      input: '',
      currentSelectionIndex: 0,
      isFocused: false,
    };
  },

  methods: {
    select(item: string) {
      this.input = item;
    },

    onInput(e: any) {
      this.input = e.target.value;
      if (this.visible && this.currentSelectionIndex >= this.filteredItems.length) {
        this.currentSelectionIndex = (this.filteredItems.length || 1) - 1;
      }
    },

    onFocus() {
      this.isFocused = true;
    },

    onBlur() {
      this.isFocused = false;
    },

    onArrowDown() {
      if (this.visible && this.currentSelectionIndex < this.filteredItems.length - 1) {
        this.currentSelectionIndex += 1;
      }
      this.scrollSelection();
    },

    onArrowUp() {
      if (this.visible && this.currentSelectionIndex > 0) {
        this.currentSelectionIndex -= 1;
      }
      this.scrollSelection();
    },

    selectCurrent() {
      if (this.filteredItems.length === 1 || this.input === this.filteredItems[this.currentSelectionIndex]) {
        this.guess();
      } else if (this.currentSelectionIndex >= 0 && this.currentSelectionIndex < this.filteredItems.length) {
        this.input = this.filteredItems[this.currentSelectionIndex];
      }
    },

    scrollSelection() {
      setTimeout(() => {
        const list = document.getElementById('autocomplete-items-list');
        if (!list) return;

        const active = document.querySelector('#autocomplete-items-list .bg-gray-200');
        if (!active) return;
        if (active instanceof HTMLElement) {
          list.scrollTop = active.offsetTop;
        }
      }, 0);
    },

    guess() {
      if (!this.input || this.input.length < 1) return;
      if (gameOver()) return;
      if (!this.items.includes(this.input)) return;

      makeGuess(this.input);
      this.input = '';
    },
  },

  computed: {
    gameOver() {
      return gameOver();
    },

    visible(): boolean {
      return this.isFocused && this.input.length > 0 && this.filteredItems.length >= 1;
    },

    filteredItems(): string[] {
      return this.items.filter((item) => item.toLowerCase().includes(this.input.toLowerCase()));
    },
  },
});
</script>
