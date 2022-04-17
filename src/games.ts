import axios from 'axios';

const GAMES = [
  '10',
];

const EPOCH = new Date(2022).valueOf();

export function getGameNumber() {
  return Math.floor((Date.now() - EPOCH) / (24 * 60 * 60 * 1000));
}

export function getGameToday() {
  return GAMES[getGameNumber() % GAMES.length];
}

export async function getGameDetails(game: string) {
  const response = await axios.get(`/assets/${game}/info.json`);
  return response.data as any;
}
