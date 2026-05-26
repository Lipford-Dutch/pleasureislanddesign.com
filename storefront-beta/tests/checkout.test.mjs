import test from "node:test";
import assert from "node:assert/strict";
import {
  DeveloperConfigError,
  buildCheckoutParams,
  createCheckoutSession,
  getRequiredStripeSecret,
  validateCheckoutItems
} from "../src/checkout.mjs";

test("validateCheckoutItems rejects empty carts and unavailable products", () => {
  assert.equal(validateCheckoutItems([]).ok, false);

  const result = validateCheckoutItems([{ productId: "pid-fan-deck", quantity: 1 }]);
  assert.equal(result.ok, false);
  assert.match(result.message || result.errors[0], /empty|unavailable/i);
});

test("validateCheckoutItems creates trusted Stripe line items from catalog data", () => {
  const result = validateCheckoutItems([
    { productId: "pid-coastal-cap", variantId: "navy", quantity: 2, priceCents: 1 }
  ]);

  assert.equal(result.ok, true);
  assert.deepEqual(result.lineItems, [
    {
      price: "price_replace_coastal_craft_cap",
      quantity: 2,
      productId: "pid-coastal-cap",
      variantId: "navy"
    }
  ]);
});

test("getRequiredStripeSecret fails clearly without server secret keys", () => {
  assert.throws(() => getRequiredStripeSecret({}), DeveloperConfigError);
  assert.throws(() => getRequiredStripeSecret({ STRIPE_SECRET_KEY: "pk_test_bad" }), DeveloperConfigError);
  assert.equal(getRequiredStripeSecret({ STRIPE_SECRET_KEY: "sk_test_ok" }), "sk_test_ok");
});

test("buildCheckoutParams sends Stripe Checkout line items without client prices", () => {
  const params = buildCheckoutParams({
    lineItems: [{ price: "price_test", quantity: 3 }],
    origin: "http://localhost:3000",
    env: { PUBLIC_SITE_URL: "https://example.com" }
  });

  assert.equal(params.get("mode"), "payment");
  assert.equal(params.get("success_url"), "https://example.com/store?checkout=success");
  assert.equal(params.get("line_items[0][price]"), "price_test");
  assert.equal(params.get("line_items[0][quantity]"), "3");
  assert.equal(params.has("line_items[0][price_data][unit_amount]"), false);
});

test("createCheckoutSession handles Stripe API success and safe failure", async () => {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    return {
      ok: true,
      status: 200,
      async json() {
        return { url: "https://checkout.stripe.test/session" };
      }
    };
  };

  const result = await createCheckoutSession({
    items: [{ productId: "pid-ceramic-mug", quantity: 1 }],
    origin: "http://localhost:3000",
    env: { STRIPE_SECRET_KEY: "sk_test_123" },
    fetchImpl
  });

  assert.equal(result.ok, true);
  assert.equal(result.url, "https://checkout.stripe.test/session");
  assert.equal(calls[0].url, "https://api.stripe.com/v1/checkout/sessions");
  assert.equal(calls[0].init.headers.Authorization, "Bearer sk_test_123");

  const failed = await createCheckoutSession({
    items: [{ productId: "pid-ceramic-mug", quantity: 1 }],
    origin: "http://localhost:3000",
    env: { STRIPE_SECRET_KEY: "sk_test_123" },
    fetchImpl: async () => ({
      ok: false,
      status: 500,
      async json() {
        return { error: { message: "secret stripe detail" } };
      }
    })
  });

  assert.equal(failed.ok, false);
  assert.equal(failed.error, "checkout_unavailable");
  assert.doesNotMatch(failed.message, /secret stripe detail/i);
});
