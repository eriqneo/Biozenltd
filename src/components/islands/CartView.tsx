import { formatKES } from '../../lib/format';
import { setQty, useList } from '../../lib/store';

interface Props {
  freeDeliveryThreshold: number;
}

export default function CartView({ freeDeliveryThreshold }: Props) {
  const cart = useList('cart');
  const subtotal = cart.reduce((n, i) => n + i.price * i.qty, 0);
  const remaining = freeDeliveryThreshold - subtotal;

  if (!cart.length) {
    return (
      <div className="card p-8 text-center">
        <p className="text-lg font-medium">Your cart is empty.</p>
        <a href="/shop" className="btn-primary mt-4 inline-flex">Browse equipment</a>
      </div>
    );
  }

  return (
    <div className="grid lg:grid-cols-[1fr_320px] gap-6 items-start">
      <ul className="card divide-y divide-ink-100">
        {cart.map((item) => (
          <li key={item.productId} className="p-4 flex flex-wrap items-center gap-4">
            <a href={`/product/${item.slug}`} className="flex-1 min-w-48 font-medium hover:text-brand-700">{item.name}</a>
            <div className="flex items-center rounded-lg ring-1 ring-ink-200">
              <button type="button" className="px-3 py-1.5" onClick={() => setQty('cart', item.productId, item.qty - 1)} aria-label={`Decrease ${item.name}`}>−</button>
              <span className="w-8 text-center tabular-nums">{item.qty}</span>
              <button type="button" className="px-3 py-1.5" onClick={() => setQty('cart', item.productId, item.qty + 1)} aria-label={`Increase ${item.name}`}>+</button>
            </div>
            <span className="w-32 text-right tabular-nums font-semibold">{formatKES(item.price * item.qty)}</span>
            <button type="button" className="text-sm text-ink-500 hover:text-red-700" onClick={() => setQty('cart', item.productId, 0)}>Remove</button>
          </li>
        ))}
      </ul>

      <aside className="card p-5 space-y-3">
        <div className="flex justify-between text-lg font-semibold">
          <span>Subtotal</span>
          <span className="tabular-nums">{formatKES(subtotal)}</span>
        </div>
        <p className="text-sm text-ink-600">
          {remaining > 0
            ? `Add ${formatKES(remaining)} more for free Nairobi delivery.`
            : 'You qualify for free Nairobi delivery.'}
        </p>
        {/* Checkout is wired up once PocketBase orders + payments (M-PESA/DPO) are connected. */}
        <a href="/checkout" className="btn-primary w-full">Checkout</a>
        <a href="/clinics/quote" className="btn-secondary w-full">Need an invoice? Request a quote</a>
      </aside>
    </div>
  );
}
