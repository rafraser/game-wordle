<template>
    <div class="w-4/5 relative">
        <div v-if="visible" class="absolute top-auto z-50 w-full mb-2 overflow-y-auto text-lg bg-white rounded bottom-full max-h-36">
            <div
                v-for="(item, index) in filteredItems" :key="item.index" class="autocomplete-list-item"
                :class="{ 'bg-gray-200': currentSelectionIndex == index }"
                @mousedown.prevent @click="select(item)" @mouseenter="currentSelectionIndex = index"
            >
                <span class="pl-2">{{ item }}</span>
            </div>
        </div>
        <input
            id="typeahead-select" type="text" class="outline-none rounded h-full w-full p-2" placeholder="Guess the game" v-model="input" autocomplete="off"
            @input="onInput" @focus="onFocus" @blur="onBlur" @keydown.down.prevent="onArrowDown" @keydown.up.prevent="onArrowUp" @keydown.enter.tab.prevent="selectCurrent"
        >
    </div>
    <button class="w-1/5 bg-green-500 hover:bg-green-700 ml-2 rounded text-white" @click="guess">Guess</button>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { makeGuess, gameOver } from '../store';

export default defineComponent({
  name: 'GuessTypeahead',

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

    onInput() {
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
      if (this.visible && this.filteredItems.length - 1) {
        this.currentSelectionIndex += 1;
      }
    },

    onArrowUp() {
      if (this.visible && this.currentSelectionIndex > 0) {
        this.currentSelectionIndex -= 1;
      }
    },

    selectCurrent() {
      if (this.currentSelectionIndex >= 0 && this.currentSelectionIndex < this.filteredItems.length) {
        this.input = this.filteredItems[this.currentSelectionIndex];
      } else if (!this.visible) {
        this.guess();
      }
    },

    guess() {
      if (this.visible) return;
      if (!this.input || this.input.length < 1) return;
      if (gameOver()) return;
      if (!this.items.includes(this.input)) return;

      makeGuess(this.input);
      this.input = '';
    },
  },

  computed: {
    visible(): boolean {
      return this.isFocused && this.input.length > 0 && this.filteredItems.length > 1;
    },

    filteredItems(): string[] {
      return this.items.filter((item) => item.includes(this.input));
    },
  },
});
</script>
