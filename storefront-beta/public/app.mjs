const CART_STORAGE_KEY = "pid-swag-cart-v1";
const MAX_ITEM_QUANTITY = 12;
const MAX_TOTAL_ITEMS = 48;

const state = {
  products: [],
  brand: null,
  cart: [],
  selectedSlug: "",
  cartOpen: false,
  checkoutLoading: false
};

const els = {
  products: document.querySelector("[data-products]"),
  detail: document.querySelector("[data-detail]"),
  status: document.querySelector("[data-status]"),
  cartCount: document.querySelector("[data-cart-count]"),
  drawer: document.querySelector("[data-cart-drawer]"),
  backdrop: document.querySelector("[data-cart-backdrop]"),
  cartItems: document.querySelector("[data-cart-items]"),
  cartSubtotal: document.querySelector("[data-cart-subtotal]"),
  cartMessage: document.querySelector("[data-cart-message]"),
  checkout: document.querySelector("[data-checkout]"),
  shippingNotes: document.querySelector("[data-shipping-notes]"),
  supportLink: document.querySelector("[data-support-link]")
};

const formatter = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD"
});

function formatPrice(priceCents) {
  return formatter.format(priceCents / 100);
}

function coerceQuantity(value) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    return null;
  }

  const quantity = Math.floor(number);
  return quantity >= 1 ? Math.min(quantity, MAX_ITEM_QUANTITY) : null;
}

function getProduct(productId) {
  return state.products.find((product) => product.id === productId) || null;
}

function getProductBySlug(slug) {
  return state.products.find((product) => product.slug === slug) || null;
}

function getVariant(product, variantId) {
  if (!product || !variantId) {
    return null;
  }

  return product.variants.find((variant) => variant.id === variantId) || null;
}

function getCartKey(productId, variantId = "") {
  return `${productId}::${variantId || ""}`;
}

function normalizeCart(rawItems) {
  if (!Array.isArray(rawItems)) {
    return [];
  }

  const grouped = new Map();
  let runningTotal = 0;

  for (const rawItem of rawItems) {
    if (!rawItem || typeof rawItem !== "object") {
      continue;
    }

    const productId = typeof rawItem.productId === "string" ? rawItem.productId : "";
    const variantId = typeof rawItem.variantId === "string" ? rawItem.variantId : "";
    const product = getProduct(productId);
    const quantity = coerceQuantity(rawItem.quantity);

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
    const allowed = Math.min(quantity, MAX_TOTAL_ITEMS - runningTotal);
    const existing = grouped.get(key);

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

function getCartTotals() {
  return state.cart.reduce(
    (totals, item) => {
      const product = getProduct(item.productId);
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

function saveCart() {
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify({ items: state.cart }));
  } catch {
    showStatus("Cart changes are saved for this visit, but your browser blocked persistence.", "warn");
  }
}

function loadCart() {
  try {
    const payload = JSON.parse(localStorage.getItem(CART_STORAGE_KEY) || "{}");
    state.cart = normalizeCart(payload.items);
  } catch {
    state.cart = [];
    localStorage.removeItem(CART_STORAGE_KEY);
  }
}

function showStatus(message, tone = "info") {
  els.status.textContent = message;
  els.status.dataset.tone = tone;
  els.status.hidden = false;
}

function clearStatus() {
  els.status.hidden = true;
  els.status.textContent = "";
}

function showCartMessage(message) {
  els.cartMessage.textContent = message;
  els.cartMessage.hidden = false;
}

function clearCartMessage() {
  els.cartMessage.textContent = "";
  els.cartMessage.hidden = true;
}

function imageMarkup(product) {
  const fallback = `<div class="image-fallback" aria-hidden="true"><span>PID</span></div>`;
  if (!product.image) {
    return fallback;
  }

  return `
    <img src="${product.image}" alt="" loading="lazy" onerror="this.replaceWith(this.nextElementSibling)">
    ${fallback}
  `;
}

function getSelectedVariantId(product, sourceElement = document) {
  const scope = sourceElement.closest?.(".product-card, .detail-panel") || document;
  const select = scope.querySelector?.(`[data-variant-for="${product.id}"]`);
  if (product.variants.length === 0) {
    return "";
  }

  return select?.value || product.variants.find((variant) => variant.available !== false)?.id || "";
}

function renderProducts() {
  if (!state.products.length) {
    els.products.innerHTML = `
      <div class="empty-state">
        <h3>No products yet</h3>
        <p>The swag catalog is empty. Add products in the catalog file to publish the store.</p>
      </div>
    `;
    return;
  }

  els.products.innerHTML = state.products.map((product) => `
    <article class="product-card ${product.available ? "" : "is-unavailable"}">
      <a class="product-image" href="/store/${product.slug}" data-product-link="${product.slug}" aria-label="View ${product.name}">
        ${imageMarkup(product)}
        ${product.available ? "" : '<span class="sold-out">Sold out</span>'}
      </a>
      <div class="product-body">
        <p class="category">${product.category}</p>
        <h3><a href="/store/${product.slug}" data-product-link="${product.slug}">${product.name}</a></h3>
        <p>${product.description}</p>
        <div class="product-row">
          <strong>${formatPrice(product.priceCents)}</strong>
          ${variantControl(product)}
        </div>
        <button class="button add-button" type="button" data-add-product="${product.id}" ${product.available ? "" : "disabled"}>
          ${product.available ? "Add to cart" : "Unavailable"}
        </button>
      </div>
    </article>
  `).join("");
}

function variantControl(product) {
  if (product.variants.length === 0) {
    return "";
  }

  return `
    <label class="variant-label">
      <span>Option</span>
      <select data-variant-for="${product.id}" ${product.available ? "" : "disabled"}>
        ${product.variants.map((variant) => `
          <option value="${variant.id}" ${variant.available === false ? "disabled" : ""}>${variant.name}</option>
        `).join("")}
      </select>
    </label>
  `;
}

function renderDetail() {
  const product = getProductBySlug(state.selectedSlug) || state.products[0];

  if (!product) {
    els.detail.innerHTML = `
      <p class="overline">Product detail</p>
      <h2>No product selected</h2>
      <p>Choose an item to view its details.</p>
    `;
    return;
  }

  state.selectedSlug = product.slug;
  const variant = product.variants.length > 0 ? variantControl(product) : "";
  els.detail.innerHTML = `
    <div class="detail-image">${imageMarkup(product)}</div>
    <p class="overline">${product.category}</p>
    <h2>${product.name}</h2>
    <p>${product.description}</p>
    <dl class="detail-list">
      <div><dt>Price</dt><dd>${formatPrice(product.priceCents)}</dd></div>
      <div><dt>Status</dt><dd>${product.available ? "Available" : "Sold out"}</dd></div>
      <div><dt>Checkout</dt><dd>Stripe-hosted payment handoff</dd></div>
    </dl>
    ${variant}
    <button class="button primary" type="button" data-add-product="${product.id}" ${product.available ? "" : "disabled"}>
      ${product.available ? "Add to cart" : "Unavailable"}
    </button>
  `;
}

function renderCart() {
  const totals = getCartTotals();
  els.cartCount.textContent = String(totals.quantity);
  els.cartSubtotal.textContent = formatPrice(totals.subtotalCents);
  els.checkout.disabled = totals.quantity === 0 || state.checkoutLoading;
  els.checkout.textContent = state.checkoutLoading ? "Preparing checkout..." : "Continue to checkout";

  if (state.cart.length === 0) {
    els.cartItems.innerHTML = `
      <div class="empty-state compact">
        <h3>Your cart is empty</h3>
        <p>Add a favorite piece of Pleasure Island Design swag to get started.</p>
      </div>
    `;
    return;
  }

  els.cartItems.innerHTML = state.cart.map((item) => {
    const product = getProduct(item.productId);
    const variant = getVariant(product, item.variantId);
    return `
      <article class="cart-item">
        <div class="cart-thumb">${imageMarkup(product)}</div>
        <div>
          <h3>${product.name}</h3>
          <p>${variant ? variant.name : product.category}</p>
          <strong>${formatPrice(product.priceCents)}</strong>
          <div class="quantity-row">
            <button type="button" class="icon-button" data-decrease="${getCartKey(item.productId, item.variantId)}" aria-label="Decrease ${product.name} quantity">-</button>
            <label>
              <span class="sr-only">Quantity for ${product.name}</span>
              <input type="number" min="1" max="${MAX_ITEM_QUANTITY}" value="${item.quantity}" data-quantity="${getCartKey(item.productId, item.variantId)}">
            </label>
            <button type="button" class="icon-button" data-increase="${getCartKey(item.productId, item.variantId)}" aria-label="Increase ${product.name} quantity">+</button>
          </div>
          <button type="button" class="text-button" data-remove="${getCartKey(item.productId, item.variantId)}">Remove</button>
        </div>
      </article>
    `;
  }).join("");
}

function renderAll() {
  renderProducts();
  renderDetail();
  renderCart();
}

function addToCart(productId, sourceElement) {
  const product = getProduct(productId);
  if (!product || !product.available) {
    showStatus("That product is no longer available.", "warn");
    return;
  }

  const variantId = getSelectedVariantId(product, sourceElement);
  state.cart = normalizeCart([...state.cart, { productId, variantId, quantity: 1 }]);
  saveCart();
  renderCart();
  openCart();
  clearCartMessage();
}

function updateItemFromKey(key, quantity) {
  const [productId, variantId] = key.split("::");
  const cleanQuantity = coerceQuantity(quantity);
  if (!cleanQuantity) {
    state.cart = state.cart.filter((item) => getCartKey(item.productId, item.variantId) !== key);
  } else {
    state.cart = state.cart.map((item) => (
      item.productId === productId && (item.variantId || "") === (variantId || "")
        ? { ...item, quantity: cleanQuantity }
        : item
    ));
  }
  state.cart = normalizeCart(state.cart);
  saveCart();
  renderCart();
}

function openCart() {
  state.cartOpen = true;
  els.drawer.hidden = false;
  els.backdrop.hidden = false;
  document.body.classList.add("has-drawer");
  requestAnimationFrame(() => els.drawer.querySelector("[data-close-cart]")?.focus());
}

function closeCart() {
  state.cartOpen = false;
  els.drawer.hidden = true;
  els.backdrop.hidden = true;
  document.body.classList.remove("has-drawer");
  clearCartMessage();
}

async function checkout() {
  clearCartMessage();
  clearStatus();

  if (state.cart.length === 0) {
    showCartMessage("Your cart is empty.");
    return;
  }

  state.checkoutLoading = true;
  renderCart();

  try {
    const response = await fetch("/api/checkout", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ items: state.cart })
    });
    const payload = await response.json().catch(() => null);

    if (!response.ok || !payload?.url) {
      showCartMessage(payload?.message || "Checkout could not be started. Please try again.");
      return;
    }

    window.location.assign(payload.url);
  } catch {
    showCartMessage("Network trouble kept checkout from starting. Please try again.");
  } finally {
    state.checkoutLoading = false;
    renderCart();
  }
}

function selectProduct(slug, push = true) {
  const product = getProductBySlug(slug);
  if (!product) {
    showStatus("We could not find that product. Showing the current catalog instead.", "warn");
    state.selectedSlug = state.products[0]?.slug || "";
    history.replaceState({}, "", "/store");
  } else {
    state.selectedSlug = slug;
    clearStatus();
    if (push) {
      history.pushState({}, "", `/store/${slug}`);
    }
  }
  renderDetail();
}

function wireEvents() {
  document.addEventListener("click", (event) => {
    const productLink = event.target.closest("[data-product-link]");
    const addButton = event.target.closest("[data-add-product]");
    const openButton = event.target.closest("[data-open-cart]");
    const closeButton = event.target.closest("[data-close-cart]");
    const removeButton = event.target.closest("[data-remove]");
    const increaseButton = event.target.closest("[data-increase]");
    const decreaseButton = event.target.closest("[data-decrease]");

    if (productLink) {
      event.preventDefault();
      selectProduct(productLink.dataset.productLink);
      document.querySelector("[data-detail]")?.scrollIntoView({ behavior: "smooth", block: "start" });
      return;
    }

    if (addButton) {
      addToCart(addButton.dataset.addProduct, addButton);
      return;
    }

    if (openButton) {
      openCart();
      return;
    }

    if (closeButton || event.target === els.backdrop) {
      closeCart();
      return;
    }

    if (removeButton) {
      updateItemFromKey(removeButton.dataset.remove, 0);
      return;
    }

    if (increaseButton) {
      const item = state.cart.find((cartItem) => getCartKey(cartItem.productId, cartItem.variantId) === increaseButton.dataset.increase);
      updateItemFromKey(increaseButton.dataset.increase, (item?.quantity || 0) + 1);
      return;
    }

    if (decreaseButton) {
      const item = state.cart.find((cartItem) => getCartKey(cartItem.productId, cartItem.variantId) === decreaseButton.dataset.decrease);
      updateItemFromKey(decreaseButton.dataset.decrease, (item?.quantity || 1) - 1);
    }
  });

  document.addEventListener("change", (event) => {
    if (event.target.matches("[data-quantity]")) {
      updateItemFromKey(event.target.dataset.quantity, event.target.value);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && state.cartOpen) {
      closeCart();
    }
  });

  els.checkout.addEventListener("click", checkout);
  window.addEventListener("popstate", () => {
    const slug = window.location.pathname.replace(/^\/store\/?/, "");
    if (slug) {
      selectProduct(slug, false);
    }
  });
}

async function init() {
  wireEvents();

  const query = new URLSearchParams(window.location.search);
  if (query.get("checkout") === "success") {
    localStorage.removeItem(CART_STORAGE_KEY);
    showStatus("Thanks. Stripe confirmed the checkout handoff, and your cart has been cleared.", "success");
  } else if (query.get("checkout") === "cancelled") {
    showStatus("Checkout was cancelled. Your cart is still here when you are ready.", "warn");
  }

  try {
    const response = await fetch("/api/catalog", { headers: { Accept: "application/json" } });
    if (!response.ok) {
      throw new Error("Catalog unavailable.");
    }
    const payload = await response.json();
    state.products = Array.isArray(payload.products) ? payload.products : [];
    state.brand = payload.brand || null;
    if (state.brand?.shippingNotes) {
      els.shippingNotes.textContent = state.brand.shippingNotes;
    }
    if (state.brand?.supportEmail) {
      els.supportLink.href = `mailto:${state.brand.supportEmail}`;
    }
    loadCart();
    const slug = window.location.pathname.replace(/^\/store\/?/, "");
    state.selectedSlug = slug || state.products[0]?.slug || "";
    renderAll();
    if (slug && !getProductBySlug(slug)) {
      selectProduct(slug, false);
    }
  } catch {
    els.products.innerHTML = `
      <div class="empty-state">
        <h3>Catalog unavailable</h3>
        <p>The shop could not load products. Refresh the page or try again shortly.</p>
      </div>
    `;
    els.detail.innerHTML = `
      <p class="overline">Error</p>
      <h2>Product details are unavailable.</h2>
      <p>The storefront recovered safely, but product data could not be loaded.</p>
    `;
    showStatus("Product data could not be loaded.", "warn");
    renderCart();
  }
}

init();
