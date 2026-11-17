import { useState } from 'react';
import { addItem } from '../../lib/store';

interface Props {
  productId: string;
  slug: string;
  name: string;
  price: number;
  quoteOnly: boolean;
  orderable: boolean;
  whatsappHref: string;
}

/**
 * One clear primary action per product: "Add to cart" for retail items,
 * "Add to quote" for quote-only items. The other path stays available but
 * visually secondary — fixing the inspiration site's five competing buttons.
 */
export default function BuyBox({ productId, slug, name, price, quoteOnly, orderable, whatsappHref }: Props) {
  const [qty, setQty] = useState(1);
  const [added, setAdded] = useState<'cart' | 'quote' | null>(null);

  const add = (key: 'cart' | 'quote') => {
    if (key === 'cart') addItem('cart', { productId, slug, name, price, qty });
    else addItem('quote', { productId, slug, name, qty });
    setAdded(key);
  };

  const primary = quoteOnly || !orderable ? 'quote' : 'cart';

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-3">
        <label htmlFor="qty" className="text-sm text-ink-600">Quantity</label>
        <div className="flex items-center rounded-lg ring-1 ring-ink-200">
          <button type="button" className="px-3 py-2 text-lg leading-none" onClick={() => setQty((q) => Math.max(1, q - 1))} aria-label="Decrease quantity">−</button>
          <input
            id="qty"
            type="number"
            min={1}
            value={qty}
            onChange={(e) => setQty(Math.max(1, Number(e.target.value) || 1))}
            className="w-14 text-center bg-transparent py-2 [appearance:textfield]"
          />
          <button type="button" className="px-3 py-2 text-lg leading-none" onClick={() => setQty((q) => q + 1)} aria-label="Increase quantity">+</button>
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-2">
        {primary === 'cart' ? (
          <>
            <button type="button" onClick={() => add('cart')} className="btn-primary flex-1">Add to cart</button>
            <button type="button" onClick={() => add('quote')} className="btn-secondary flex-1">Add to quote</button>
          </>
        ) : (
          <button type="button" onClick={() => add('quote')} className="btn-primary flex-1">Add to quote list</button>
        )}
      </div>

      <a href={whatsappHref} target="_blank" rel="noopener" className="inline-flex items-center gap-2 text-sm font-medium text-brand-700 hover:underline">
        Ask about this item on WhatsApp →
      </a>

      <p aria-live="polite" className="text-sm min-h-5">
        {added === 'cart' && (
          <span className="text-emerald-700">Added to cart. <a href="/cart" className="underline font-medium">View cart</a></span>
        )}
        {added === 'quote' && (
          <span className="text-emerald-700">Added to your quote list. <a href="/clinics/quote" className="underline font-medium">View quote list</a></span>
        )}
      </p>
    </div>
  );
}
