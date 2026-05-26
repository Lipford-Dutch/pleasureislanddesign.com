import test from "node:test";
import assert from "node:assert/strict";
import {
  MAX_ITEM_QUANTITY,
  addCartItem,
  coerceQuantity,
  getCartTotals,
  normalizeCartItems,
  removeCartItem,
  updateCartItem
} from "../src/cart.mjs";
import { products } from "../src/catalog.mjs";

test("coerceQuantity rejects unsafe quantities and clamps large quantities", () => {
  assert.equal(coerceQuantity(0), null);
  assert.equal(coerceQuantity(-2), null);
  assert.equal(coerceQuantity(Number.NaN), null);
  assert.equal(coerceQuantity("3.8"), 3);
  assert.equal(coerceQuantity(999), MAX_ITEM_QUANTITY);
});

test("normalizeCartItems removes invalid, unavailable, and malformed items", () => {
  const normalized = normalizeCartItems([
    { productId: "pid-coastal-cap", variantId: "navy", quantity: 2 },
    { productId: "pid-coastal-cap", variantId: "navy", quantity: 3 },
    { productId: "pid-fan-deck", quantity: 1 },
    { productId: "missing", quantity: 1 },
    { productId: "pid-finish-shirt", variantId: "bad-size", quantity: 1 },
    { productId: "pid-ceramic-mug", quantity: -10 }
  ]);

  assert.deepEqual(normalized, [
    { productId: "pid-coastal-cap", variantId: "navy", quantity: 5 }
  ]);
});

test("cart helpers add, update, remove, and total with catalog prices", () => {
  let cart = [];
  cart = addCartItem(cart, { productId: "pid-ceramic-mug", quantity: 1 }, products);
  cart = addCartItem(cart, { productId: "pid-ceramic-mug", quantity: 2 }, products);
  cart = updateCartItem(cart, "pid-ceramic-mug", "", 4, products);

  assert.deepEqual(cart, [{ productId: "pid-ceramic-mug", variantId: "", quantity: 4 }]);
  assert.deepEqual(getCartTotals(cart, products), { quantity: 4, subtotalCents: 8800 });

  cart = removeCartItem(cart, "pid-ceramic-mug", "", products);
  assert.deepEqual(cart, []);
});
