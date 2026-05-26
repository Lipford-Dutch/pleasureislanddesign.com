# Pleasure Island Design Swag Store

A small, branded storefront for up to 12 swag products. The app uses a local product catalog, a localStorage-backed cart with validation, and server-side Stripe Checkout session creation. It does not collect payment details directly.

## Run Locally

```bash
node server.mjs
```

Open `http://localhost:3000/store`.

## Configure Checkout

Copy `.env.example` into your deployment environment and set:

- `STRIPE_SECRET_KEY`: server-only Stripe secret key.
- `PUBLIC_SITE_URL`: public origin for success/cancel fallbacks.
- `STRIPE_SUCCESS_URL` and `STRIPE_CANCEL_URL`: optional explicit redirects.

Real Stripe Price IDs must be added in `src/catalog.mjs` before live checkout. The checkout endpoint only accepts product IDs, variant IDs, and quantities, then maps them to server-side `stripePriceId` values.

## Edit Products

Edit `src/catalog.mjs`. Keep the catalog to 12 or fewer products. Product images live in `public/assets/products`. If an image is missing or fails to load, the storefront shows a branded fallback and stays usable.

## Useful Checks

```bash
node --test tests/*.test.mjs
node --check server.mjs
node --check public/app.mjs
```
