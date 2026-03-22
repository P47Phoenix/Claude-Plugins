# Frontend Performance

Cross-framework reference for bundle optimization, lazy loading, image optimization, Core Web Vitals, render optimization, resource loading, service workers, CDN strategies, measurement, and anti-patterns.

---

## Bundle Optimization

### Code Splitting Strategies

- **Route-based splitting**: each route loads its own JavaScript chunk; reduces initial bundle size
- **Component-based splitting**: heavy components (rich text editors, charts, maps) loaded on demand
- **Vendor splitting**: separate third-party libraries into their own chunk; they change less frequently and cache longer
- **Manual chunks**: configure the bundler to group related modules (e.g., all chart libraries in one chunk)

### Dynamic Imports

```js
const Chart = lazy(() => import('./Chart'));         // React
const Chart = defineAsyncComponent(() => import('./Chart.vue')); // Vue
```

- Each dynamic import creates a new chunk boundary
- Name chunks for debugging: `import(/* webpackChunkName: "chart" */ './Chart')`

### Tree Shaking

- Only works with ES module syntax (`import`/`export`), not CommonJS (`require`)
- Mark packages as side-effect-free in `package.json` (`"sideEffects": false`) to enable aggressive tree shaking
- Avoid importing entire libraries: `import { debounce } from 'lodash-es'` not `import _ from 'lodash'`
- Verify tree shaking with bundle analysis tools (webpack-bundle-analyzer, rollup-plugin-visualizer, source-map-explorer)

### Dead Code Elimination

- Bundlers remove code that is never imported or referenced
- Use `process.env.NODE_ENV` / `import.meta.env.MODE` checks to strip debug code in production
- Remove unused exports; tools like `ts-prune` or `knip` find dead exports

### Bundle Analysis

- Regularly analyze bundle composition; identify unexpectedly large dependencies
- Set performance budgets: fail the build if a chunk exceeds a size threshold
- Track bundle size over time in CI to catch regressions

---

## Lazy Loading

### Images

- **Native lazy loading**: `<img loading="lazy">` -- browser-native, no JavaScript required
- **Intersection Observer**: more control over threshold, root margin, and loading behavior
- Load images when they are within a configurable distance from the viewport (e.g., 200px margin)
- Always set explicit `width` and `height` attributes to prevent layout shift when images load

### Components

- React: `React.lazy()` + `<Suspense fallback={<Skeleton />}>`
- Vue: `defineAsyncComponent` with loading and error component options
- Svelte: `{#await import('./Component.svelte')}`
- Show a meaningful loading state (skeleton screen, spinner) during chunk download

### Route Prefetching

- Prefetch route chunks on link hover or viewport intersection for near-instant navigation
- Next.js: `<Link>` prefetches automatically; disable with `prefetch={false}` for low-priority routes
- Frameworks: `router.prefetch('/path')` for programmatic prefetching
- Balance prefetching aggressiveness with bandwidth: do not prefetch every route on page load

---

## Image Optimization

### Modern Formats

| Format | Best for | Browser support |
|---|---|---|
| WebP | Photos, illustrations | All modern browsers |
| AVIF | Photos (better compression than WebP) | Broad support (2023+) |
| SVG | Icons, logos, simple illustrations | Universal |
| PNG | Screenshots, images requiring transparency | Universal |

Use `<picture>` with multiple `<source>` elements to serve the best format the browser supports.

### Responsive Images

```html
<img
  srcset="image-400.webp 400w, image-800.webp 800w, image-1200.webp 1200w"
  sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 33vw"
  src="image-800.webp"
  alt="Description"
  width="800" height="600"
  loading="lazy"
/>
```

- Serve appropriately sized images; do not send a 4000px image to a 400px container
- Use `srcset` with width descriptors (`w`) and `sizes` to let the browser choose the best source
- CDN image transformation: generate sizes and formats on-the-fly via URL parameters

### Placeholder Strategies

- **LQIP** (Low Quality Image Placeholder): a tiny blurred version of the image shown during load
- **Blur hash**: a compact string representation that decodes to a blurred placeholder; no network request
- **Dominant color**: a solid background matching the image's primary color
- **Skeleton**: a grey box matching the image dimensions
- Always transition smoothly from placeholder to loaded image (fade-in)

---

## Core Web Vitals

### LCP (Largest Contentful Paint)

The time until the largest visible content element (image, heading, text block) finishes rendering.

**Target**: under 2.5 seconds.

**Common causes of poor LCP**:
- Render-blocking CSS or JS delaying first paint
- Slow server response time (high TTFB)
- Large unoptimized hero images
- Web fonts blocking text rendering

**Optimization strategies**:
- Preload the LCP image: `<link rel="preload" as="image" href="hero.webp">`
- Inline critical CSS; defer non-critical CSS
- Use `fetchpriority="high"` on the LCP image element
- Optimize server response time; use a CDN
- Avoid lazy loading the LCP element

### INP (Interaction to Next Paint)

The latency of the slowest interaction during the page's lifecycle, measured from input to the next frame rendered.

**Target**: under 200 milliseconds.

**Common causes of poor INP**:
- Long JavaScript tasks blocking the main thread
- Expensive re-renders triggered by interaction
- Synchronous layout or style recalculation during event handlers
- Large DOM size slowing down rendering after state changes

**Optimization strategies**:
- Break long tasks into smaller chunks using `scheduler.yield()` or `setTimeout`
- Debounce or throttle high-frequency event handlers (scroll, resize, input)
- Use `startTransition` (React) or equivalent to mark non-urgent updates as low priority
- Virtualize long lists to reduce DOM size and rendering cost
- Avoid synchronous DOM measurement in event handlers

### CLS (Cumulative Layout Shift)

The sum of unexpected layout shifts that occur during the page's lifetime.

**Target**: under 0.1.

**Common causes of CLS**:
- Images without explicit dimensions
- Dynamically injected content above the viewport (ads, banners, cookie notices)
- Web fonts causing text reflow (FOIT/FOUT)
- Late-loading components pushing content down

**Prevention strategies**:
- Always set `width` and `height` on images and videos (or use `aspect-ratio` CSS)
- Reserve space for ads, embeds, and dynamic content with fixed-size containers
- Use `font-display: swap` with size-adjusted fallback fonts to minimize text reflow
- Use CSS `contain` to isolate layout changes within a container
- Insert new content below the viewport or with user-initiated action, not above visible content

---

## Render Optimization

### Virtualization / Windowing

Render only the visible items in a long list; recycle DOM nodes as the user scrolls.

- Libraries: TanStack Virtual, react-window, react-virtuoso, vue-virtual-scroller
- Reduces DOM node count from thousands to dozens
- Essential for lists over ~100 items with complex row rendering
- Provide an accurate item size estimate (fixed or measured) for smooth scrolling

### Memoization

Prevent unnecessary re-computation or re-rendering of components and values.

| Framework | Component memoization | Value memoization |
|---|---|---|
| React | `React.memo(Component)` | `useMemo`, `useCallback` |
| Vue | Automatic (reactivity system) | `computed` |
| Svelte | Automatic (compile-time) | `$:` reactive declarations |
| Solid | Automatic (signals) | `createMemo` |

- Do not wrap every component in `memo`; measure first, optimize the components that actually re-render expensively
- Ensure dependencies are stable references (avoid creating new objects/arrays in render)

### Key Prop Usage

- Always use a stable, unique key when rendering lists (database ID, not array index)
- Index-based keys cause incorrect reconciliation when items are reordered, inserted, or deleted
- Keys help the framework identify which items changed and minimize DOM mutations

---

## Resource Loading

### Resource Hints

| Hint | What it does | When to use |
|---|---|---|
| `preload` | Fetch immediately with high priority | Resources needed for the current page (fonts, hero image, critical CSS) |
| `prefetch` | Fetch at low priority for future navigation | Resources likely needed for the next page |
| `preconnect` | Establish connection (DNS + TCP + TLS) early | Third-party origins you will fetch from (CDN, API, analytics) |
| `dns-prefetch` | Resolve DNS only | Third-party origins where full preconnect is excessive |

### Script Loading

| Attribute | Behavior |
|---|---|
| No attribute | Blocks HTML parsing; executes immediately |
| `async` | Downloads in parallel; executes as soon as downloaded (order not guaranteed) |
| `defer` | Downloads in parallel; executes after HTML is parsed (order preserved) |
| `type="module"` | Deferred by default; supports `import`/`export` |

- Use `defer` for scripts that need DOM access and must execute in order
- Use `async` for independent scripts (analytics, ads) where execution order does not matter
- Place critical inline scripts in `<head>`; move non-critical scripts to end of `<body>` or use `defer`

---

## Service Workers

### Caching Strategies

| Strategy | Behavior | Best for |
|---|---|---|
| Cache-first | Serve from cache; fall back to network | Static assets (CSS, JS, images, fonts) |
| Network-first | Try network; fall back to cache | API responses, dynamic content |
| Stale-while-revalidate | Serve from cache immediately; update cache from network in the background | Content that can tolerate brief staleness (blog posts, product listings) |
| Cache-only | Only serve from cache | Offline-first apps with pre-cached content |
| Network-only | Only serve from network | Requests that must always be fresh (authentication, real-time data) |

### Offline Support

- Pre-cache critical assets during the `install` event (app shell model)
- Show an offline fallback page when the network is unavailable and the requested page is not cached
- Queue failed mutations (POST, PUT, DELETE) with Background Sync; replay when connectivity returns

### Lifecycle

- `install`: pre-cache assets; call `skipWaiting()` to activate immediately
- `activate`: clean up old caches; call `clients.claim()` to take control of open pages
- `fetch`: intercept network requests; apply caching strategy
- Update strategy: version the cache name; delete old caches during activation

---

## CDN Strategies

### Static Asset Caching

- Serve static assets (JS, CSS, images, fonts) from a CDN for lower latency
- Use content-hash filenames (`main.a1b2c3.js`) for cache busting; set long `Cache-Control: max-age` (1 year)
- HTML files should not be cached long-term (short max-age or `no-cache` with ETag)
- Configure `immutable` directive for hashed assets: `Cache-Control: public, max-age=31536000, immutable`

### Edge Caching

- Cache dynamic responses at the CDN edge for frequently accessed, infrequently changing content
- Use `Vary` headers correctly to avoid serving wrong cached content (e.g., `Vary: Accept-Encoding`)
- Implement cache purging for content updates; stale content after a deploy is a common issue

---

## Performance Measurement

### Tools

| Tool | Type | What it measures |
|---|---|---|
| Lighthouse | Lab | Simulated performance scores and recommendations |
| PageSpeed Insights | Lab + Field | Lighthouse scores plus real-user data from CrUX |
| Performance API | Code | Programmatic timing measurements in production |
| Web Vitals library | Code | Measure CWV in production (`onLCP`, `onINP`, `onCLS`) |
| Chrome DevTools Performance panel | Lab | Flame charts, main thread activity, rendering timeline |

### Real User Monitoring (RUM)

- Measure performance on real users' devices and networks, not just lab conditions
- Track Core Web Vitals (LCP, INP, CLS) plus custom metrics (time to interactive feature, API latency)
- Segment data by device type, connection speed, geography, and browser
- Set up alerts for performance regressions

### Performance Budgets

- Define maximum sizes for JavaScript bundles, CSS, images, and total page weight
- Enforce budgets in CI: fail the build if a budget is exceeded
- Track budgets over time; budgets should get tighter as the team optimizes, not looser

---

## Common Performance Anti-Patterns

### Layout Thrashing

Reading layout properties and then writing styles in a loop forces the browser to recalculate layout on every iteration.

```js
// Bad: read then write in a loop
items.forEach(el => {
  const height = el.offsetHeight; // read (forces layout)
  el.style.height = height + 10 + 'px'; // write (invalidates layout)
});

// Good: batch reads, then batch writes
const heights = items.map(el => el.offsetHeight);
items.forEach((el, i) => { el.style.height = heights[i] + 10 + 'px'; });
```

### Forced Synchronous Layout

Accessing layout properties (`offsetWidth`, `clientHeight`, `getBoundingClientRect()`) after modifying styles forces the browser to calculate layout synchronously. Batch reads before writes.

### Unoptimized Event Handlers

- Attaching expensive logic to `scroll`, `resize`, `mousemove`, or `input` without throttling or debouncing
- Use passive event listeners for scroll and touch events: `{ passive: true }`
- Debounce input handlers; throttle scroll handlers; use Intersection Observer instead of scroll position checks

### Memory Leaks from Subscriptions

- Event listeners, intervals, WebSocket connections, and observable subscriptions that are never cleaned up
- Always remove listeners and unsubscribe in component cleanup / unmount lifecycle
- Use WeakRef or WeakMap for caches that should not prevent garbage collection
- Monitor memory usage in DevTools; look for detached DOM nodes and growing heap over time
