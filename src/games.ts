import axios from 'axios';

const GAMES = [
  'cc3b820d37ec',
  'ed33d36c645c',
  '6adb2652d421',
  '923131e63c60',
  'eea13fef13cc',
  '3dc03c3fdece',
  '0717d705040f',
  '09737b41b539',
  'e3ae671f0b21',
  '0a0c6272c6b8',
  'ad3e3c040bc5',
  '16641e2f0675',
  '0c6632d8f842',
  '3aac67cd7316',
  '04323f73ed5b',
  '9303895f7314',
  '44a338904571',
  'cc697de591be',
  '92b72c299ad3',
  '18ff43ad88cd',
  '9b15a40a88ee',
  '49e04ac3119a',
  'f2bdb0417e3b',
  'a750abdc866a',
  '4b6fe0a57c41',
  '246a9cf9e8ed',
  'c8bdb1484a6f',
  '4462aabba64b',
  'a5c1849f8f1c',
  '2a73c7e812b5',
  'd435722b1b8d',
  'bfc8373ba76c',
  '89ce6ff25f1b',
  '5c471255af29',
  '98ff1e5b226f',
  '56fbf33e32c1',
  'db962bd70ec6',
  'a4f6beacfdaa',
  '00e759b3b5e6',
  'c59febd4fd5a',
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
    steamId: data.steamid,
  } as any;
}
