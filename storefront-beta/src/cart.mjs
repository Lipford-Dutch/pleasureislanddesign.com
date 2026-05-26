import { getProductById, getVariant, products } from "./catalog.mjs";

export const CART_STORAGE_KEY = "pid-swag-cart-v1";
export const MAX_ITEM_QUANTITY = 12;
export const MAX_TOTAL_ITEMS = 48;

export function coerceQuantity(value) {
  const number = Number(value);

  if (!Number.isFinite(number)) {
    return null;
  }

  const quantity = Math.floor(number);

  if (quantity < 1) {
    return null;
  }

  return Math.min(quantity, MAX_ITEM_QUANTITY);
}

export function getCartKey(productId, variantId = "") {
  return `${productId}::${variantId || ""}`;
}

export function normalizeCartItems(rawItems, catalog = products) {
  if (!Array.isArray(rawItems)) {
    return [];
  }

  const grouped = new Map();
  let runningTotal = 0;

  for (const item of rawItems) {
    if (!item || typeof item !== "object") {
      continue;
    }

    const productId = typeof item.productId === "string" ? item.productId : "";
    const variantId = typeof item.variantId === "string" ? item.variantId : "";
    const product = getProductById(productId, catalog);
    const quantity = coerceQuantity(item.quantity);

    if (!product || !product.available || !quantity) {
      continue;
    }

    if (product.variants.length > 0) {
      const variant = getVariant(product, variantId);
      if (!variant || variant.available === false) {
        continue;
      }
    }

    if (runningTotal >= MAX_TOTAL_ITEMS) {
      break;
    }

    const key = getCartKey(productId, variantId);
    const existing = grouped.get(key);
    const allowed = Math.min(quantity, MAX_TOTAL_ITEMS - runningTotal);

    if (existing) {
      const nextQuantity = Math.min(existing.quantity + allowed, MAX_ITEM_QUANTITY);
      runningTotal += nextQuantity - existing.quantity;
      existing.quantity = nextQuantity;
    } else {
      grouped.set(key, { productId, variantId, quantity: allowed });
      runningTotal += allowed;
    }
  }

  return Array.from(grouped.values());
}

export function addCartItem(items, item, catalog = products) {
  return normalizeCartItems([...normalizeCartItems(items, catalog), item], catalog);
}

export function updateCartItem(items, productId, variantId, quantity, catalog = products) {
  const cleanQuantity = coerceQuantity(quantity);

  if (!cleanQuantity) {
    return removeCartItem(items, productId, variantId, catalog);
  }

  return normalizeCartItems(items, catalog).map((item) => {
    if (item.productId === productId && (item.variantId || "") === (variantId || "")) {
      return { ...item, quantity: cleanQuantity };
    }

    return item;
  });
}

export function removeCartItem(items, productId, variantId = "", catalog = products) {
  return normalizeCartItems(items, catalog).filter(
    (item) => !(item.productId === productId && (item.variantId || "") === (variantId || ""))
  );
}

export function getCartTotals(items, catalog = products) {
  const cleanItems = normalizeCartItems(items, catalog);

  return cleanItems.reduce(
    (totals, item) => {
      const product = getProductById(item.productId, catalog);
      if (!product) {
        return totals;
      }

      totals.quantity += item.quantity;
      totals.subtotalCents += product.priceCents * item.quantity;
      return totals;
    },
    { quantity: 0, subtotalCents: 0 }
  );
}
