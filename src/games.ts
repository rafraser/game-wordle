import axios from 'axios';

const GAMES = [
  '4000',
];

// game 0 is April 18th, game 1 is April 19th
const EPOCH = new Date(2022, 3, 18).valueOf();

export function getGameNumber() {
  return Math.floor((Date.now() - EPOCH) / (24 * 60 * 60 * 1000));
}

export function getGameToday() {
  return GAMES[getGameNumber() % GAMES.length];
}

export async function getGameDetails(game: string) {
  const response = await axios.get(`/assets/${game}/info.json`);
  const { data } = response;

  return {
    tags: data.tags,
    description: data.description,
    title: data.title,
    releaseYear: data.release_year,
  } as any;
}
