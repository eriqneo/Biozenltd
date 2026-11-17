# Biozen K Limited — website

Medical equipment shop for clinics and retail customers. Astro 7 + React islands + Tailwind v4, deployed on **Cloudflare Workers (static assets)**. The backend (PocketBase on PocketHost) will be connected later.

## Commands

| Command | What it does |
| --- | --- |
| `npm run dev` | Local dev server at http://localhost:4321 |
| `npm run check` | Type-check |
| `npm run build` | Production build into `dist/` |
| `npm run preview` | Build, then run it in Cloudflare's local runtime at http://localhost:8787 |
| `npm run deploy` | Build and deploy to Cloudflare |

Requires Node 22.23+.

## Deploying to Cloudflare

### Option A — from your computer
1. `npx wrangler login` (opens the browser to sign in to Cloudflare).
2. `npm run deploy`.
3. The site goes live at `https://biozen.<your-subdomain>.workers.dev`.

### Option B — automatic deploys from GitHub (recommended)
1. Push this folder to a GitHub repository.
2. Cloudflare dashboard → **Workers & Pages → Create → Import a repository**.
3. Build command: `npm run build` · Deploy command: `npx wrangler deploy`.
4. Every push to `main` deploys automatically; other branches get preview URLs.

### Option C — Cloudflare Pages (current setup: biozenltd.pages.dev)
Pages project settings → Build:
- Build command: `npm run build`
- **Build output directory: `dist/client`** (not `dist` — the Astro Cloudflare adapter puts the site in `dist/client`; with `dist` the homepage 404s)

Pages ignores `wrangler.jsonc` (it logs a harmless "not valid" notice) but honours `public/_headers` and the 404 page.

### Custom domain
Cloudflare dashboard → **Workers & Pages → biozen → Settings → Domains & Routes → Add custom domain**. Then replace `https://www.example.com` in:
- `astro.config.mjs` (`site`)
- `src/lib/site.ts` (`url`)
- `wrangler.jsonc` (`PUBLIC_SITE_URL`)

## How it's set up for Cloudflare

- **All pages are prerendered**, so Cloudflare serves plain files from its CDN (fast, and free-tier friendly). When live PocketBase data is needed on a page, add `export const prerender = false` to that page and it renders on demand in the Worker.
- **Clean URLs**: pages build as `about.html` and are served at `/about` (no trailing-slash redirects).
- **`public/_headers`**: long caching for hashed assets, short caching for images, `no-store` for cart/checkout/account, and security headers.
- **404**: unknown URLs show `src/pages/404.astro` with a real 404 status.

## Connecting PocketHost (later)

1. Copy `.env.example` to `.env` and set `PUBLIC_POCKETBASE_URL`.
2. Add the same variable in Cloudflare (Settings → Variables and Secrets, as a **build** variable, since pages are prerendered).
3. Rewrite `src/lib/catalog.ts` to read from PocketBase. It's the only file pages read catalogue data from; `src/lib/types.ts` mirrors the planned collections.
4. Any admin or API keys go in `wrangler secret put NAME`, never in `wrangler.jsonc`.

## Project map

- `src/lib/site.ts` — business details (name, phone, WhatsApp, nav)
- `src/lib/catalog.ts` — catalogue data access (swap to PocketBase here)
- `src/lib/data/sample.ts` — sample products (replace with real catalogue)
- `src/components/islands/` — interactive React parts (shop filters, buy box, cart, quote builder)
- `public/images/products/` — sample illustrations from `scripts/make-sample-images.py`
