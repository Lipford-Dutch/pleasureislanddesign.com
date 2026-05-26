import { createReadStream, existsSync, readFileSync } from "node:fs";
import { readFile, stat } from "node:fs/promises";
import { createServer } from "node:http";
import { extname, join, normalize, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { BRAND, STOREFRONT_ROUTE, getPublicProducts } from "./src/catalog.mjs";
import { DeveloperConfigError, createCheckoutSession } from "./src/checkout.mjs";

const __dirname = fileURLToPath(new URL(".", import.meta.url));
const publicDir = resolve(__dirname, "public");
loadDotEnv();
const port = Number(process.env.PORT || 3000);
const maxBodyBytes = 32_768;

const mimeTypes = new Map([
  [".html", "text/html; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".mjs", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".svg", "image/svg+xml"],
  [".png", "image/png"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".webp", "image/webp"],
  [".ico", "image/x-icon"]
]);

function loadDotEnv() {
  const envPath = resolve(__dirname, ".env");
  if (!existsSync(envPath)) {
    return;
  }

  try {
    const content = readFileSync(envPath, "utf8");
    for (const line of content.split(/\r?\n/)) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) {
        continue;
      }

      const [key, ...valueParts] = trimmed.split("=");
      if (!process.env[key]) {
        process.env[key] = valueParts.join("=").replace(/^["']|["']$/g, "");
      }
    }
  } catch {
    // Ignore unreadable local env files; deployment env vars still work.
  }
}

function sendJson(res, status, payload) {
  res.writeHead(status, {
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  res.end(JSON.stringify(payload));
}

function sendText(res, status, message) {
  res.writeHead(status, {
    "Content-Type": "text/plain; charset=utf-8",
    "X-Content-Type-Options": "nosniff"
  });
  res.end(message);
}

function isStoreRoute(pathname) {
  return pathname === STOREFRONT_ROUTE || pathname.startsWith(`${STOREFRONT_ROUTE}/`);
}

function getOrigin(req) {
  const forwardedProto = req.headers["x-forwarded-proto"];
  const proto = Array.isArray(forwardedProto) ? forwardedProto[0] : forwardedProto || "http";
  const host = req.headers["x-forwarded-host"] || req.headers.host;
  return host ? `${proto}://${Array.isArray(host) ? host[0] : host}` : undefined;
}

async function readJsonBody(req) {
  const chunks = [];
  let size = 0;

  for await (const chunk of req) {
    size += chunk.length;
    if (size > maxBodyBytes) {
      throw Object.assign(new Error("Request body is too large."), { statusCode: 413 });
    }
    chunks.push(chunk);
  }

  if (chunks.length === 0) {
    return {};
  }

  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf8"));
  } catch {
    throw Object.assign(new Error("Malformed JSON request body."), { statusCode: 400 });
  }
}

async function serveStatic(req, res, pathname) {
  const requestPath = pathname === "/" ? "/index.html" : pathname;
  const safePath = normalize(decodeURIComponent(requestPath)).replace(/^(\.\.[/\\])+/, "");
  const filePath = resolve(join(publicDir, safePath));

  if (!filePath.startsWith(publicDir)) {
    sendText(res, 403, "Forbidden");
    return;
  }

  try {
    const fileStat = await stat(filePath);
    if (!fileStat.isFile()) {
      sendText(res, 404, "Not found");
      return;
    }

    res.writeHead(200, {
      "Content-Type": mimeTypes.get(extname(filePath)) || "application/octet-stream",
      "Cache-Control": process.env.NODE_ENV === "production" && !filePath.endsWith("index.html")
        ? "public, max-age=3600"
        : "no-store",
      "X-Content-Type-Options": "nosniff"
    });
    createReadStream(filePath).pipe(res);
  } catch {
    sendText(res, 404, "Not found");
  }
}

async function serveIndex(res) {
  const html = await readFile(join(publicDir, "index.html"), "utf8");
  res.writeHead(200, {
    "Content-Type": "text/html; charset=utf-8",
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff"
  });
  res.end(html);
}

export function createStoreServer() {
  return createServer(async (req, res) => {
    try {
      const url = new URL(req.url || "/", "http://localhost");

      if (req.method === "GET" && url.pathname === "/") {
        res.writeHead(302, { Location: STOREFRONT_ROUTE });
        res.end();
        return;
      }

      if (req.method === "GET" && url.pathname === "/api/catalog") {
        sendJson(res, 200, {
          brand: BRAND,
          storefrontRoute: STOREFRONT_ROUTE,
          products: getPublicProducts()
        });
        return;
      }

      if (req.method === "POST" && url.pathname === "/api/checkout") {
        const body = await readJsonBody(req);
        const result = await createCheckoutSession({
          items: body.items,
          origin: getOrigin(req)
        });

        sendJson(res, result.status, result.ok ? { url: result.url } : {
          error: result.error,
          message: result.message
        });
        return;
      }

      if (req.method === "GET" && isStoreRoute(url.pathname)) {
        await serveIndex(res);
        return;
      }

      if (req.method === "GET" || req.method === "HEAD") {
        await serveStatic(req, res, url.pathname);
        return;
      }

      sendJson(res, 405, { error: "method_not_allowed", message: "Method not allowed." });
    } catch (error) {
      if (error instanceof DeveloperConfigError) {
        console.error(`[checkout config] ${error.message}`);
        sendJson(res, 500, {
          error: "checkout_not_configured",
          message: "Checkout is not configured yet."
        });
        return;
      }

      const status = error.statusCode || 500;
      if (status >= 500) {
        console.error("[storefront]", error);
      }

      sendJson(res, status, {
        error: status >= 500 ? "server_error" : "bad_request",
        message: status >= 500 ? "Something went wrong. Please try again." : error.message
      });
    }
  });
}

if (process.argv[1] && fileURLToPath(import.meta.url) === resolve(process.argv[1])) {
  const server = createStoreServer();
  server.listen(port, () => {
    console.log(`Pleasure Island Design store running at http://localhost:${port}${STOREFRONT_ROUTE}`);
  });
}
