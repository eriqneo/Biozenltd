import { useState } from 'react';
import { clearList, setQty, useList } from '../../lib/store';

interface Props {
  whatsapp: string;
}

type Status = 'idle' | 'sent';

/**
 * Quote builder: shop items + free-text items + optional file, then contact
 * details. Submission is local for now; it will create `quotes` and
 * `quote_items` records in PocketBase once PocketHost is connected.
 */
export default function QuoteBuilder({ whatsapp }: Props) {
  const quote = useList('quote');
  const [extra, setExtra] = useState<{ name: string; qty: number }[]>([]);
  const [extraName, setExtraName] = useState('');
  const [extraQty, setExtraQty] = useState(1);
  const [status, setStatus] = useState<Status>('idle');
  const [ref, setRef] = useState('');
  const [summary, setSummary] = useState('');
  const [hasFile, setHasFile] = useState(false);

  const addExtra = () => {
    if (!extraName.trim()) return;
    setExtra((e) => [...e, { name: extraName.trim(), qty: extraQty }]);
    setExtraName('');
    setExtraQty(1);
  };

  const onSubmit = (e: { preventDefault(): void; currentTarget: HTMLFormElement }) => {
    e.preventDefault();
    const data = new FormData(e.currentTarget);
    const reference = `BZQ-${Date.now().toString(36).toUpperCase().slice(-6)}`;
    const lines = [
      ...quote.map((i) => `• ${i.qty} × ${i.name}`),
      ...extra.map((i) => `• ${i.qty} × ${i.name} (not in shop)`),
      ...(hasFile ? ['• Equipment list attached to the web request'] : []),
    ];
    const text = [
      `Hello Biozen, quote request ${reference}`,
      `Name: ${data.get('name')}`,
      data.get('facility') ? `Facility: ${data.get('facility')}` : '',
      data.get('town') ? `Delivery to: ${data.get('town')}` : '',
      '',
      ...lines,
    ]
      .filter((l, i, arr) => l !== '' || arr[i - 1] !== '')
      .join('\n');
    // TODO(PocketHost): pb.collection('quotes').create({...}) then quote_items.
    setRef(reference);
    setSummary(text);
    setStatus('sent');
    clearList('quote');
  };

  if (status === 'sent') {
    return (
      <div className="card p-8 space-y-4">
        <p className="text-sm font-medium text-emerald-700">Request received</p>
        <h2 className="text-2xl font-semibold">Your reference is {ref}</h2>
        <p className="text-ink-600">
          We reply with a priced quotation within one working day. For a faster response, send the summary to us on WhatsApp.
        </p>
        <a className="btn-primary" target="_blank" rel="noopener" href={`https://wa.me/${whatsapp}?text=${encodeURIComponent(summary)}`}>
          Send summary on WhatsApp
        </a>
        <a href="/shop" className="block text-sm text-brand-700 hover:underline">Back to the shop</a>
      </div>
    );
  }

  const hasItems = quote.length > 0 || extra.length > 0 || hasFile;

  return (
    <form onSubmit={onSubmit} className="grid lg:grid-cols-2 gap-6 items-start">
      <section className="card p-5 space-y-4">
        <h2 className="text-lg font-semibold">1. Your items</h2>
        {quote.length === 0 && extra.length === 0 && (
          <p className="text-sm text-ink-600">
            No items yet. Use <strong>Add to quote</strong> on any product, add items below, or upload your list.
          </p>
        )}
        <ul className="divide-y divide-ink-100">
          {quote.map((item) => (
            <li key={item.productId} className="py-2 flex items-center gap-3">
              <a href={`/product/${item.slug}`} className="flex-1 hover:text-brand-700">{item.name}</a>
              <input
                type="number"
                min={0}
                value={item.qty}
                aria-label={`Quantity for ${item.name}`}
                onChange={(e) => setQty('quote', item.productId, Number(e.target.value))}
                className="input w-20"
              />
            </li>
          ))}
          {extra.map((item, idx) => (
            <li key={`x${idx}`} className="py-2 flex items-center gap-3">
              <span className="flex-1">{item.name} <span className="text-xs text-ink-500">(not in shop)</span></span>
              <span className="w-20 text-center tabular-nums">{item.qty}</span>
              <button type="button" className="text-sm text-ink-500 hover:text-red-700" onClick={() => setExtra((e) => e.filter((_, i) => i !== idx))}>Remove</button>
            </li>
          ))}
        </ul>

        <fieldset className="space-y-2">
          <legend className="text-sm font-medium">Can't find something? Describe it</legend>
          <div className="flex gap-2">
            <input
              className="input flex-1"
              placeholder="e.g. 3-function electric bed with mattress"
              value={extraName}
              onChange={(e) => setExtraName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  addExtra();
                }
              }}
            />
            <input className="input w-20" type="number" min={1} value={extraQty} onChange={(e) => setExtraQty(Math.max(1, Number(e.target.value) || 1))} aria-label="Quantity" />
            <button type="button" className="btn-secondary" onClick={addExtra}>Add</button>
          </div>
        </fieldset>

        <div className="space-y-1">
          <label htmlFor="list" className="text-sm font-medium">Or upload your list (PDF, Excel, Word or photo, max 10 MB)</label>
          <input id="list" name="list" type="file" accept=".pdf,.xls,.xlsx,.csv,.doc,.docx,image/*" className="block text-sm" onChange={(e) => setHasFile(!!e.target.files?.length)} />
          <p className="text-xs text-ink-500">Equipment lists only. Please don't include patient information.</p>
        </div>
      </section>

      <section className="card p-5 space-y-4">
        <h2 className="text-lg font-semibold">2. Your details</h2>
        <div className="grid sm:grid-cols-2 gap-3">
          <label className="field">
            <span>Full name *</span>
            <input name="name" required className="input" autoComplete="name" />
          </label>
          <label className="field">
            <span>Phone / WhatsApp *</span>
            <input name="phone" required type="tel" className="input" autoComplete="tel" placeholder="07XX XXX XXX" />
          </label>
          <label className="field">
            <span>Email *</span>
            <input name="email" required type="email" className="input" autoComplete="email" />
          </label>
          <label className="field">
            <span>Clinic / facility</span>
            <input name="facility" className="input" autoComplete="organization" />
          </label>
          <label className="field sm:col-span-2">
            <span>Delivery town</span>
            <input name="town" className="input" placeholder="e.g. Nakuru" />
          </label>
          <label className="field sm:col-span-2">
            <span>Anything else? (installation, delivery date, budget)</span>
            <textarea name="notes" rows={3} className="input" />
          </label>
        </div>
        <button type="submit" className="btn-primary w-full" disabled={!hasItems}>
          Request my quotation
        </button>
        {!hasItems && <p className="text-xs text-ink-500 text-center">Add at least one item or upload a list to continue.</p>}
        <p className="text-xs text-ink-500">No payment needed. We reply with a priced quotation within one working day.</p>
      </section>
    </form>
  );
}
