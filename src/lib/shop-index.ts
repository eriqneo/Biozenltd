import { getAllProducts, rootCategoryId } from './catalog';
import type { Product } from './types';

/** The fields a shop card and the filters need — kept small for the browser. */
export type ShopItem = Pick<Product, 'id' | 'slug' | 'name' | 'summary' | 'price' | 'compare_at_price' | 'quote_only' | 'stock' | 'brand' | 'created' | 'featured'> & {
  root: string;
  image?: string;
};

export async function getShopIndex(): Promise<ShopItem[]> {
  const products = await getAllProducts();
  return products.map((p) => ({
    id: p.id,
    slug: p.slug,
    name: p.name,
    summary: p.summary,
    price: p.price,
    compare_at_price: p.compare_at_price,
    quote_only: p.quote_only,
    stock: p.stock,
    brand: p.brand,
    created: p.created,
    featured: p.featured,
    root: rootCategoryId(p.category),
    image: p.images[0],
  }));
}
