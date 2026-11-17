// Prerendered JSON of every product card, fetched by the shop page's filters.
// Served from Cloudflare's cache like any static file.
import type { APIRoute } from 'astro';
import { getShopIndex } from '../lib/shop-index';

export const GET: APIRoute = async () =>
  new Response(JSON.stringify(await getShopIndex()), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
