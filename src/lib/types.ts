// Shapes mirror the planned PocketBase collections, so swapping sample data
// for PocketHost later only changes src/lib/catalog.ts.

export interface Category {
  id: string;
  slug: string;
  name: string;
  description: string;
  /** Empty for top-level categories. */
  parent: string;
  icon: string;
  sort: number;
}

export interface Brand {
  id: string;
  slug: string;
  name: string;
}

export type StockStatus = 'in_stock' | 'low_stock' | 'out_of_stock' | 'on_order';

export interface Product {
  id: string;
  slug: string;
  name: string;
  summary: string;
  description: string;
  /** Category record id (a subcategory where one exists). */
  category: string;
  brand: string;
  sku: string;
  /** Retail price in KES. Ignored when quote_only is true. */
  price: number;
  /** Optional price before discount, for offers. */
  compare_at_price?: number;
  /** High-value or configurable items: no cart, quote only. */
  quote_only: boolean;
  stock: StockStatus;
  warranty_months: number;
  installation_available: boolean;
  specs: Record<string, string>;
  in_the_box: string[];
  images: string[];
  manuals: string[];
  featured: boolean;
  created: string;
}

export type CustomerType = 'retail' | 'clinic';

export interface QuoteItem {
  productId: string;
  slug: string;
  name: string;
  qty: number;
}

export interface CartItem {
  productId: string;
  slug: string;
  name: string;
  price: number;
  qty: number;
}
