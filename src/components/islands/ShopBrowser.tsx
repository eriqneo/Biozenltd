import { useEffect, useMemo, useState } from 'react';
import { formatKES, stockLabel, stockTone } from '../../lib/format';
import type { ShopItem as Lite } from '../../lib/shop-index';

interface Props {
  /** First page of products, server-rendered so the page works before JS. */
  initial: Lite[];
  total: number;
  /** URL of the full product index (fetched after the page loads). */
  indexUrl: string;
  categories: { id: string; name: string }[];
  brands: { id: string; name: string }[];
}

type Sort = 'featured' | 'newest' | 'price-asc' | 'price-desc' | 'name';
const PAGE = 24;

const PRICE_BANDS = [
  { id: '', label: 'Any price' },
  { id: '0-10000', label: 'Under KES 10,000' },
  { id: '10000-50000', label: 'KES 10,000 – 50,000' },
  { id: '50000-150000', label: 'KES 50,000 – 150,000' },
  { id: '150000-', label: 'Over KES 150,000' },
  { id: 'quote', label: 'Price on quote' },
];

/**
 * Client-side search/filter for the sample catalogue. Once PocketHost is
 * connected and the catalogue grows, move this filtering into a PocketBase
 * query (filter + sort + pagination) on a server-rendered /shop page.
 */
export default function ShopBrowser({ initial, total, indexUrl, categories, brands }: Props) {
  const [products, setProducts] = useState<Lite[]>(initial);
  const [loading, setLoading] = useState(initial.length < total);
  const [visible, setVisible] = useState(PAGE);
  const [q, setQ] = useState('');
  const [cat, setCat] = useState('');
  const [brand, setBrand] = useState('');
  const [band, setBand] = useState('');
  const [inStock, setInStock] = useState(false);
  const [sort, setSort] = useState<Sort>('featured');

  useEffect(() => {
    const p = new URLSearchParams(window.location.search);
    setQ(p.get('q') ?? '');
    setCat(p.get('category') ?? '');
    if (initial.length < total) {
      fetch(indexUrl)
        .then((r) => (r.ok ? r.json() : Promise.reject(r.status)))
        .then((all: Lite[]) => setProducts(all))
        .catch(() => { /* keep the first page if the index can't load */ })
        .finally(() => setLoading(false));
    }
  }, [indexUrl, initial.length, total]);

  useEffect(() => setVisible(PAGE), [q, cat, brand, band, inStock, sort]);

  const results = useMemo(() => {
    const terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    let list = products.filter((p) => {
      if (cat && p.root !== cat) return false;
      if (brand && p.brand !== brand) return false;
      if (inStock && !(p.stock === 'in_stock' || p.stock === 'low_stock')) return false;
      if (band === 'quote' && !p.quote_only) return false;
      if (band && band !== 'quote') {
        if (p.quote_only) return false;
        const [lo, hi] = band.split('-').map((v) => (v ? Number(v) : undefined));
        if (lo !== undefined && p.price < lo) return false;
        if (hi !== undefined && p.price >= hi) return false;
      }
      if (terms.length) {
        const hay = `${p.name} ${p.summary}`.toLowerCase();
        if (!terms.every((t) => hay.includes(t))) return false;
      }
      return true;
    });
    const price = (p: Lite) => (p.quote_only ? Number.POSITIVE_INFINITY : p.price);
    list = [...list].sort((a, b) => {
      switch (sort) {
        case 'newest': return b.created.localeCompare(a.created);
        case 'price-asc': return price(a) - price(b);
        case 'price-desc': return (b.quote_only ? -1 : b.price) - (a.quote_only ? -1 : a.price);
        case 'name': return a.name.localeCompare(b.name);
        default: return Number(b.featured) - Number(a.featured) || b.created.localeCompare(a.created);
      }
    });
    return list;
  }, [products, q, cat, brand, band, inStock, sort]);

  const reset = () => {
    setQ(''); setCat(''); setBrand(''); setBand(''); setInStock(false);
  };

  return (
    <div className="grid lg:grid-cols-[260px_1fr] gap-6 items-start">
      <aside className="card p-4 space-y-4 lg:sticky lg:top-36">
        <label className="field">
          <span>Search</span>
          <input type="search" className="input" value={q} onChange={(e) => setQ(e.target.value)} placeholder="e.g. oxygen concentrator" />
        </label>
        <label className="field">
          <span>Category</span>
          <select className="input" value={cat} onChange={(e) => setCat(e.target.value)}>
            <option value="">All categories</option>
            {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
          </select>
        </label>
        <label className="field">
          <span>Brand</span>
          <select className="input" value={brand} onChange={(e) => setBrand(e.target.value)}>
            <option value="">All brands</option>
            {brands.map((b) => <option key={b.id} value={b.id}>{b.name}</option>)}
          </select>
        </label>
        <label className="field">
          <span>Price</span>
          <select className="input" value={band} onChange={(e) => setBand(e.target.value)}>
            {PRICE_BANDS.map((b) => <option key={b.id} value={b.id}>{b.label}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-2 text-sm font-medium text-ink-700">
          <input type="checkbox" checked={inStock} onChange={(e) => setInStock(e.target.checked)} className="size-4 accent-brand-600" />
          In stock only
        </label>
        <button type="button" onClick={reset} className="text-sm text-brand-700 hover:underline">Clear filters</button>
      </aside>

      <section aria-live="polite">
        <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
          <p className="text-sm text-ink-600">
            {loading ? `Loading ${total} products…` : `${results.length} ${results.length === 1 ? 'product' : 'products'}`}
          </p>
          <label className="flex items-center gap-2 text-sm">
            <span className="text-ink-600">Sort by</span>
            <select className="input w-auto" value={sort} onChange={(e) => setSort(e.target.value as Sort)}>
              <option value="featured">Featured</option>
              <option value="newest">Newest</option>
              <option value="price-asc">Price: low to high</option>
              <option value="price-desc">Price: high to low</option>
              <option value="name">Name A–Z</option>
            </select>
          </label>
        </div>

        {results.length === 0 ? (
          <div className="card p-8 text-center space-y-3">
            <p className="font-medium">No products match those filters.</p>
            <p className="text-sm text-ink-600">Tell us what you need and we'll source it.</p>
            <a href="/clinics/quote" className="btn-primary">Request a quote</a>
          </div>
        ) : (
          <ul className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {results.slice(0, visible).map((p) => {
              const onSale = !p.quote_only && p.compare_at_price && p.compare_at_price > p.price;
              return (
                <li key={p.id} className="card group overflow-hidden hover:shadow-md transition">
                  <a href={`/product/${p.slug}`} className="flex h-full flex-col">
                    <div className="relative aspect-[4/3] grid place-items-center bg-gradient-to-br from-brand-50 to-ink-100 text-brand-600/60">
                      {p.image ? (
                        <img src={p.image} alt={p.name} loading="lazy" className="size-full object-contain bg-white" />
                      ) : (
                        <svg viewBox="0 0 48 48" className="w-1/4 max-w-16" fill="none" stroke="currentColor" strokeWidth="2.2" aria-hidden="true">
                          <rect x="6" y="6" width="36" height="36" rx="10" /><path d="M24 15v18M15 24h18" strokeLinecap="round" />
                        </svg>
                      )}
                      {onSale && <span className="absolute left-3 top-3 rounded-full bg-red-600 px-2 py-0.5 text-xs font-semibold text-white">Offer</span>}
                    </div>
                    <div className="flex flex-1 flex-col gap-2 p-4">
                      <h3 className="font-medium leading-snug group-hover:text-brand-700 line-clamp-2">{p.name}</h3>
                      <p className="text-sm text-ink-600 line-clamp-2">{p.summary}</p>
                      <div className="mt-auto flex flex-wrap items-end justify-between gap-2 pt-2">
                        {p.quote_only ? (
                          <span className="font-semibold text-brand-800">Price on quote</span>
                        ) : (
                          <span className="flex items-baseline gap-2">
                            <span className="font-semibold tabular-nums">{formatKES(p.price)}</span>
                            {onSale && <s className="text-xs text-ink-500 tabular-nums">{formatKES(p.compare_at_price!)}</s>}
                          </span>
                        )}
                        <span className={`rounded-full px-2 py-0.5 text-[11px] font-medium ring-1 ring-inset ${stockTone[p.stock]}`}>{stockLabel[p.stock]}</span>
                      </div>
                    </div>
                  </a>
                </li>
              );
            })}
          </ul>
        )}
        {results.length > visible && (
          <div className="mt-6 text-center">
            <button type="button" className="btn-secondary" onClick={() => setVisible((v) => v + PAGE)}>
              Show more ({results.length - visible} left)
            </button>
          </div>
        )}
      </section>
    </div>
  );
}
