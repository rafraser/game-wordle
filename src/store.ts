import { reactive } from 'vue';

export const store = reactive({
  guesses: [] as string[],
  today: '',
  gameDetails: {
    tags: [],
    description: '',
    title: '',
  },
});

export function hasWon() {
  if (store.guesses.length === 0) return false;
  return store.guesses[store.guesses.length - 1] === store.gameDetails.title;
}

export function guesses() {
  return store.guesses.length;
}

export function gameOver() {
  return hasWon() || guesses() >= 6;
}

export function saveToLocalStorage() {
  localStorage.setItem('game-state', JSON.stringify({
    today: store.today,
    guesses: store.guesses,
  }));
}

export function loadLocalStorage() {
  const state = localStorage.getItem('game-state');
  return state ? JSON.parse(state) : null;
}

export function makeGuess(guess: string) {
  if (hasWon() || store.guesses.length === 6) return;
  store.guesses.push(guess);
  saveToLocalStorage();
}
