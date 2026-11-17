// Single entry point for catalogue data. Pages never import sample data or the
// PocketBase SDK directly, so connecting PocketHost later means changing only
// this file. Keep every function async for that reason.
import { brands, categories, products as rawProducts } from './data/sample';
import { site } from './site';
import type { Brand, Category, Product } from './types';

// High-value items are quote-only everywhere (cards, product page, filters),
// not just on the product page.
const products: Product[] = rawProducts.map((p) =>
  p.quote_only || p.price >= site.quoteThreshold ? { ...p, quote_only: true } : p,
);

export type SortKey = 'featured' | 'newest' | 'price-asc' | 'price-desc' | 'name';

const bySort = (a: Category, b: Category) => a.sort - b.sort || a.name.localeCompare(b.name);

export async function getTopCategories(): Promise<Category[]> {
  return categories.filter((c) => !c.parent).sort(bySort);
}

export async function getCategoryBySlug(slug: string): Promise<Category | undefined> {
  return categories.find((c) => !c.parent && c.slug === slug);
}

export async function getSubcategory(parentSlug: string, slug: string): Promise<Category | undefined> {
  return categories.find((c) => c.parent === parentSlug && c.slug === slug);
}

export async function getSubcategories(parentId: string): Promise<Category[]> {
  return categories.filter((c) => c.parent === parentId).sort(bySort);
}

export async function getCategoryById(id: string): Promise<Category | undefined> {
  return categories.find((c) => c.id === id);
}

export async function getBrands(): Promise<Brand[]> {
  return [...brands].sort((a, b) => a.name.localeCompare(b.name));
}

export async function getBrand(id: string): Promise<Brand | undefined> {
  return brands.find((b) => b.id === id);
}

/** Top-level category id for any category id. */
export function rootCategoryId(categoryId: string): string {
  return categories.find((c) => c.id === categoryId)?.parent || categoryId;
}

export async function getProducts(opts: { category?: string; featured?: boolean; limit?: number } = {}): Promise<Product[]> {
  let list = products;
  if (opts.category) {
    const cat = opts.category;
    list = list.filter((p) => p.category === cat || rootCategoryId(p.category) === cat);
  }
  if (opts.featured) list = list.filter((p) => p.featured);
  list = [...list].sort((a, b) => b.created.localeCompare(a.created));
  return opts.limit ? list.slice(0, opts.limit) : list;
}

export async function getOffers(): Promise<Product[]> {
  return products.filter((p) => p.compare_at_price && p.compare_at_price > p.price);
}

export async function getProductBySlug(slug: string): Promise<Product | undefined> {
  return products.find((p) => p.slug === slug);
}

export async function getRelated(product: Product, limit = 4): Promise<Product[]> {
  const root = rootCategoryId(product.category);
  return products
    .filter((p) => p.id !== product.id && rootCategoryId(p.category) === root)
    .slice(0, limit);
}

export async function getAllProducts(): Promise<Product[]> {
  return products;
}
