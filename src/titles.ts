export const titles = [] as string[];

export function getMatchingTitles(query: string) {
  return titles.filter((title) => title.includes(query));
}
