// Tiny browser store for the cart and quote list. Lives in localStorage until
// PocketBase auth lands; then signed-in users' lists can sync to `carts`/`quotes`.
import { useSyncExternalStore } from 'react';
import type { CartItem, QuoteItem } from './types';

type Lists = { cart: CartItem[]; quote: QuoteItem[] };
type Key = keyof Lists;

const STORAGE: Record<Key, string> = { cart: 'bz-cart', quote: 'bz-quote' };
const EMPTY: Lists = { cart: [], quote: [] };
const listeners = new Set<() => void>();
let cache: Lists | null = null;

function read(): Lists {
  if (cache) return cache;
  const next: Lists = { cart: [], quote: [] };
  for (const key of Object.keys(STORAGE) as Key[]) {
    try {
      const raw = localStorage.getItem(STORAGE[key]);
      if (raw) (next[key] as unknown[]) = JSON.parse(raw);
    } catch {
      /* private mode or corrupt value: start empty */
    }
  }
  cache = next;
  return next;
}

function write<K extends Key>(key: K, items: Lists[K]) {
  cache = { ...read(), [key]: items };
  try {
    localStorage.setItem(STORAGE[key], JSON.stringify(items));
  } catch {
    /* storage unavailable: keep in memory for this page */
  }
  listeners.forEach((l) => l());
  // Lets the non-React header counter (Header.astro) update too.
  window.dispatchEvent(new Event('bz-store'));
}

if (typeof window !== 'undefined') {
  window.addEventListener('storage', () => {
    cache = null;
    listeners.forEach((l) => l());
  });
}

const subscribe = (l: () => void) => {
  listeners.add(l);
  return () => listeners.delete(l);
};

export function useList<K extends Key>(key: K): Lists[K] {
  return useSyncExternalStore(
    subscribe,
    () => read()[key],
    () => EMPTY[key],
  );
}

export function addItem<K extends Key>(key: K, item: Lists[K][number]) {
  const current = read()[key] as Lists[K][number][];
  const exists = current.some((i) => i.productId === item.productId);
  const items = exists
    ? current.map((i) => (i.productId === item.productId ? { ...i, qty: i.qty + item.qty } : i))
    : [...current, item];
  write(key, items as Lists[K]);
}

export function setQty<K extends Key>(key: K, productId: string, qty: number) {
  const items = (read()[key] as Lists[K][number][])
    .map((i) => (i.productId === productId ? { ...i, qty } : i))
    .filter((i) => i.qty > 0);
  write(key, items as Lists[K]);
}

export function clearList(key: Key) {
  write(key, []);
}
