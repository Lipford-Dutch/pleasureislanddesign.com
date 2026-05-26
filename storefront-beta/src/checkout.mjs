import { getProductById, getVariant, products } from "./catalog.mjs";
import { MAX_ITEM_QUANTITY, MAX_TOTAL_ITEMS, coerceQuantity, normalizeCartItems } from "./cart.mjs";

export class DeveloperConfigError extends Error {
  constructor(message) {
    super(message);
    this.name = "DeveloperConfigError";
  }
}

export function validateCheckoutItems(rawItems, catalog = products) {
  const cleanItems = normalizeCartItems(rawItems, catalog);
  const errors = [];

  if (cleanItems.length === 0) {
    errors.push("Your cart is empty or contains unavailable items.");
  }

  let totalQuantity = 0;
  const lineItems = [];

  for (const item of cleanItems) {
    const product = getProductById(item.productId, catalog);
    const variant = item.variantId ? getVariant(product, item.variantId) : null;
    const quantity = coerceQuantity(item.quantity);

    if (!product || !product.available) {
      errors.push("One or more cart items are no longer available.");
      continue;
    }

    if (product.variants.length > 0 && (!variant || variant.available === false)) {
      errors.push(`${product.name} needs a valid available option.`);
      continue;
    }

    if (!quantity || quantity > MAX_ITEM_QUANTITY) {
      errors.push(`${product.name} has an invalid quantity.`);
      continue;
    }

    const priceId = variant?.stripePriceId || product.stripePriceId;
    if (typeof priceId !== "string" || !priceId.startsWith("price_")) {
      errors.push(`${product.name} is missing a Stripe Price ID.`);
      continue;
    }

    totalQuantity += quantity;
    lineItems.push({
      price: priceId,
      quantity,
      productId: product.id,
      variantId: variant?.id || ""
    });
  }

  if (totalQuantity > MAX_TOTAL_ITEMS) {
    errors.push(`Checkout is limited to ${MAX_TOTAL_ITEMS} total items.`);
  }

  return {
    ok: errors.length === 0,
    errors,
    lineItems,
    cleanItems,
    totalQuantity
  };
}

export function getRequiredStripeSecret(env = process.env) {
  const secret = env.STRIPE_SECRET_KEY;

  if (typeof secret !== "string" || secret.trim() === "") {
    throw new DeveloperConfigError("STRIPE_SECRET_KEY is required for checkout.");
  }

  if (!secret.startsWith("sk_")) {
    throw new DeveloperConfigError("STRIPE_SECRET_KEY must be a server-side Stripe secret key.");
  }

  return secret;
}

export function getCheckoutUrls({ origin, env = process.env }) {
  const baseUrl = env.PUBLIC_SITE_URL || origin || "http://localhost:3000";
  const successUrl = env.STRIPE_SUCCESS_URL || `${baseUrl}/store?checkout=success`;
  const cancelUrl = env.STRIPE_CANCEL_URL || `${baseUrl}/store?checkout=cancelled`;

  return { successUrl, cancelUrl };
}

export function buildCheckoutParams({ lineItems, origin, env = process.env }) {
  const { successUrl, cancelUrl } = getCheckoutUrls({ origin, env });
  const params = new URLSearchParams();

  params.set("mode", "payment");
  params.set("success_url", successUrl);
  params.set("cancel_url", cancelUrl);
  params.set("allow_promotion_codes", "true");
  params.set("shipping_address_collection[allowed_countries][0]", "US");
  params.set("metadata[store]", "pleasure-island-design-swag");

  lineItems.forEach((item, index) => {
    params.set(`line_items[${index}][price]`, item.price);
    params.set(`line_items[${index}][quantity]`, String(item.quantity));
  });

  return params;
}

export async function createCheckoutSession({
  items,
  origin,
  env = process.env,
  fetchImpl = fetch,
  catalog = products
}) {
  const validation = validateCheckoutItems(items, catalog);

  if (!validation.ok) {
    return {
      ok: false,
      status: 400,
      error: "invalid_cart",
      message: validation.errors[0],
      details: validation.errors
    };
  }

  const secret = getRequiredStripeSecret(env);
  const body = buildCheckoutParams({ lineItems: validation.lineItems, origin, env });
  const response = await fetchImpl("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${secret}`,
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok || !payload?.url) {
    return {
      ok: false,
      status: response.status || 502,
      error: "checkout_unavailable",
      message: "Checkout is temporarily unavailable. Please try again."
    };
  }

  return {
    ok: true,
    status: 200,
    url: payload.url
  };
}
