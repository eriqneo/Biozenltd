import type { StockStatus } from './types';

const kes = new Intl.NumberFormat('en-KE', { style: 'currency', currency: 'KES', maximumFractionDigits: 0 });

/** One consistent price format everywhere, e.g. "KES 128,000". */
export const formatKES = (amount: number) => kes.format(amount).replace(/ /g, ' ');

export const stockLabel: Record<StockStatus, string> = {
  in_stock: 'In stock',
  low_stock: 'Low stock',
  out_of_stock: 'Out of stock',
  on_order: 'Available on order',
};

export const stockTone: Record<StockStatus, string> = {
  in_stock: 'bg-emerald-50 text-emerald-700 ring-emerald-600/20',
  low_stock: 'bg-amber-50 text-amber-800 ring-amber-600/20',
  out_of_stock: 'bg-slate-100 text-slate-600 ring-slate-500/20',
  on_order: 'bg-sky-50 text-sky-700 ring-sky-600/20',
};
