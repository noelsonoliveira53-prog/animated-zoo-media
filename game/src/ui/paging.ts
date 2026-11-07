// Pure paging helpers (no Phaser import, so they are unit-testable).

export function pageCount(total: number, perPage: number): number {
  return Math.max(1, Math.ceil(total / perPage));
}

/** Clamp a page index into range (wrapping is the caller's choice). */
export function clampPage(page: number, total: number, perPage: number): number {
  return Math.max(0, Math.min(pageCount(total, perPage) - 1, Math.floor(page)));
}

export function pageItems<T>(items: T[], page: number, perPage: number): T[] {
  const p = clampPage(page, items.length, perPage);
  return items.slice(p * perPage, p * perPage + perPage);
}
