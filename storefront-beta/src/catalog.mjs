export const BRAND = {
  name: "Pleasure Island Design",
  description: "Refined coastal cabinetry, finishing craft, and practical goods for polished home projects.",
  voice: "polished, local, precise, and coastal",
  supportEmail: "support@pleasureislanddesign.com",
  returnPolicyUrl: "/store#returns",
  shippingNotes: "Ships from North Carolina. Local pickup can be coordinated after checkout.",
  colors: {
    navy: "#092f4f",
    deepNavy: "#071d31",
    gold: "#b78a45",
    paleGold: "#e8d0a3",
    cream: "#fbf7ec",
    paper: "#fffaf0",
    sea: "#4f9ead"
  }
};

export const CURRENCY = "usd";
export const STOREFRONT_ROUTE = "/store";
export const MAX_UNIQUE_PRODUCTS = 12;

export const products = [
  {
    id: "pid-coastal-cap",
    slug: "coastal-craft-cap",
    name: "Coastal Craft Cap",
    description: "A structured navy cap with champagne stitching for job walks, beach errands, and sunny install days.",
    priceCents: 2800,
    currency: CURRENCY,
    image: "/assets/products/coastal-craft-cap.svg",
    category: "Wearables",
    available: true,
    stripePriceId: "price_replace_coastal_craft_cap",
    variants: [
      { id: "navy", name: "Deep navy", available: true },
      { id: "sand", name: "Sand", available: true }
    ]
  },
  {
    id: "pid-finish-shirt",
    slug: "flawless-finish-shirt",
    name: "Flawless Finish Shirt",
    description: "Soft cotton-blend shop shirt with the Pleasure Island Design mark and a clean coastal cabinet graphic.",
    priceCents: 3600,
    currency: CURRENCY,
    image: "/assets/products/flawless-finish-shirt.svg",
    category: "Wearables",
    available: true,
    stripePriceId: "price_replace_flawless_finish_shirt",
    variants: [
      { id: "s", name: "Small", available: true },
      { id: "m", name: "Medium", available: true },
      { id: "l", name: "Large", available: true },
      { id: "xl", name: "XL", available: true }
    ]
  },
  {
    id: "pid-shop-apron",
    slug: "cabinetry-shop-apron",
    name: "Cabinetry Shop Apron",
    description: "Heavy canvas apron for prep work, hardware sorting, gardening, or weekend projects.",
    priceCents: 4200,
    currency: CURRENCY,
    image: "/assets/products/cabinetry-shop-apron.svg",
    category: "Shop Goods",
    available: true,
    stripePriceId: "price_replace_cabinetry_shop_apron",
    variants: []
  },
  {
    id: "pid-ceramic-mug",
    slug: "morning-coast-mug",
    name: "Morning Coast Mug",
    description: "A substantial ceramic mug with a navy glazed base and a small wave mark.",
    priceCents: 2200,
    currency: CURRENCY,
    image: "/assets/products/morning-coast-mug.svg",
    category: "Home",
    available: true,
    stripePriceId: "price_replace_morning_coast_mug",
    variants: []
  },
  {
    id: "pid-care-kit",
    slug: "cabinet-care-kit",
    name: "Cabinet Care Kit",
    description: "A tidy kit for gentle cabinet touch-ups: microfiber cloth, care card, and hardware-safe cleaning notes.",
    priceCents: 3400,
    currency: CURRENCY,
    image: "/assets/products/cabinet-care-kit.svg",
    category: "Home",
    available: true,
    stripePriceId: "price_replace_cabinet_care_kit",
    variants: []
  },
  {
    id: "pid-sticker-pack",
    slug: "coastal-sticker-pack",
    name: "Coastal Sticker Pack",
    description: "Weather-resistant stickers with wave, shell, spray finish, and cabinet door motifs.",
    priceCents: 1200,
    currency: CURRENCY,
    image: "/assets/products/coastal-sticker-pack.svg",
    category: "Small Goods",
    available: true,
    stripePriceId: "price_replace_coastal_sticker_pack",
    variants: []
  },
  {
    id: "pid-fan-deck",
    slug: "coastal-color-fan-deck",
    name: "Coastal Color Fan Deck",
    description: "A compact fan deck inspired by cabinet-safe coastal tones, meant for early project dreaming.",
    priceCents: 1800,
    currency: CURRENCY,
    image: "/assets/products/coastal-color-fan-deck.svg",
    category: "Design Tools",
    available: false,
    stripePriceId: "price_replace_coastal_color_fan_deck",
    variants: []
  },
  {
    id: "pid-canvas-tote",
    slug: "project-day-canvas-tote",
    name: "Project Day Canvas Tote",
    description: "A sturdy cream canvas tote sized for finish samples, notebooks, and hardware selections.",
    priceCents: 2600,
    currency: CURRENCY,
    image: "/assets/products/project-day-canvas-tote.svg",
    category: "Bags",
    available: true,
    stripePriceId: "price_replace_project_day_canvas_tote",
    variants: []
  }
];

export function assertCatalogShape(catalog = products) {
  if (!Array.isArray(catalog)) {
    throw new Error("Product catalog must be an array.");
  }

  if (catalog.length > MAX_UNIQUE_PRODUCTS) {
    throw new Error(`Product catalog is limited to ${MAX_UNIQUE_PRODUCTS} products.`);
  }

  const ids = new Set();
  const slugs = new Set();

  for (const product of catalog) {
    if (!product || typeof product !== "object") {
      throw new Error("Every product must be an object.");
    }

    for (const field of ["id", "slug", "name", "description", "category", "currency"]) {
      if (typeof product[field] !== "string" || product[field].trim() === "") {
        throw new Error(`Product ${product.id || "(unknown)"} is missing ${field}.`);
      }
    }

    if (ids.has(product.id)) {
      throw new Error(`Duplicate product id: ${product.id}`);
    }

    if (slugs.has(product.slug)) {
      throw new Error(`Duplicate product slug: ${product.slug}`);
    }

    if (!Number.isInteger(product.priceCents) || product.priceCents < 0) {
      throw new Error(`Product ${product.id} has an invalid price.`);
    }

    if (product.currency !== CURRENCY) {
      throw new Error(`Product ${product.id} must use ${CURRENCY}.`);
    }

    if (typeof product.available !== "boolean") {
      throw new Error(`Product ${product.id} must include available.`);
    }

    if (!Array.isArray(product.variants)) {
      throw new Error(`Product ${product.id} variants must be an array.`);
    }

    ids.add(product.id);
    slugs.add(product.slug);
  }
}

export function getPublicProducts(catalog = products) {
  assertCatalogShape(catalog);

  return catalog.map(({ stripePriceId, variants, ...product }) => ({
    ...product,
    variants: variants.map(({ stripePriceId: _stripePriceId, ...variant }) => variant)
  }));
}

export function getProductById(productId, catalog = products) {
  return catalog.find((product) => product.id === productId) || null;
}

export function getProductBySlug(slug, catalog = products) {
  return catalog.find((product) => product.slug === slug) || null;
}

export function getVariant(product, variantId) {
  if (!product || !variantId) {
    return null;
  }

  return product.variants.find((variant) => variant.id === variantId) || null;
}

export function formatPrice(priceCents, currency = CURRENCY) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: currency.toUpperCase()
  }).format(priceCents / 100);
}
