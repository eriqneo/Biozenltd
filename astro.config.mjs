// @ts-check
import { defineConfig } from 'astro/config';

import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';
import cloudflare from '@astrojs/cloudflare';

// https://astro.build/config
export default defineConfig({
  // TODO: set the real domain once it's connected in Cloudflare.
  site: 'https://www.example.com',
  integrations: [react()],

  // Pages build as /about.html (not /about/index.html) so Cloudflare serves
  // them at /about without a trailing-slash redirect on every click.
  build: { format: 'file' },
  trailingSlash: 'never',

  vite: {
    plugins: [tailwindcss()],
  },

  // Cloudflare Workers + static assets. Every page is currently prerendered;
  // pages that need live PocketBase data can opt into on-demand rendering
  // with `export const prerender = false`.
  adapter: cloudflare(),
});
