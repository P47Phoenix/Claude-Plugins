# Frontend Styling Systems

Cross-framework reference for CSS architecture, theming, responsive design, dark mode, custom properties, performance, and anti-patterns.

---

## CSS Architecture Approaches

### BEM (Block__Element--Modifier)

A naming convention that makes CSS class relationships explicit and avoids specificity conflicts.

```
.card {}              /* Block */
.card__title {}       /* Element */
.card__title--large {}/* Modifier */
```

- Blocks are standalone components; elements belong to a block; modifiers change appearance or behavior
- Flat specificity: every selector is a single class, so overrides are predictable
- Scales well in large codebases with many contributors; class names are self-documenting
- Verbose class names are the tradeoff; mitigate with preprocessor nesting or utilities for common properties
- When to use: multi-team projects, CMS-driven sites, projects without a component framework's scoping

### CSS Modules

Scoped styles where class names are locally scoped by default and transformed to unique identifiers at build time.

- Import styles as an object: `import styles from './Card.module.css'` then `className={styles.title}`
- Composition: `composes: base from './shared.module.css'` to reuse rules without duplication
- Global styles via `:global(.className)` escape hatch; use sparingly
- Requires a build tool (webpack, Vite, etc.) that supports CSS Modules
- Works with any framework; no runtime cost; output is standard CSS
- Combine with CSS custom properties for theming across module boundaries

### CSS-in-JS

Write styles in JavaScript/TypeScript, generating scoped class names at build time or runtime.

- **Runtime** (styled-components, Emotion): styles computed and injected at render time
  - Pros: dynamic styles based on props, full JS expressiveness, automatic vendor prefixing
  - Cons: runtime overhead, larger bundle, SSR requires extra setup to avoid flash of unstyled content
- **Zero-runtime** (vanilla-extract, Linaria, Panda CSS): styles extracted at build time to static CSS
  - Pros: no runtime cost, type-safe style definitions, works well with SSR
  - Cons: limited dynamic styling (use CSS custom properties for runtime values)
- Pattern: define a `styled` wrapper or `css` function; co-locate styles with components
- SSR considerations: extract critical CSS on the server; hydrate style sheets on the client

### Utility-First / Tailwind CSS

Compose UI from small, single-purpose utility classes applied directly in markup.

```html
<div class="flex items-center gap-4 p-4 rounded-lg bg-white shadow-md">
```

- Rapid development; design consistency enforced by a constrained set of utilities
- Custom utilities: extend the config for project-specific values (colors, spacing, fonts)
- `@apply`: extract repeated utility combinations into a CSS class; use judiciously to avoid recreating BEM
- Purging: production builds remove unused utilities; ensure all dynamic class names are detectable
- Design system alignment: configure `tailwind.config` to match design tokens (colors, typography scale, spacing scale)
- Tradeoff: markup becomes verbose; extract components to manage complexity

---

## Theming Implementation

### CSS Custom Properties for Theming

Define a set of design tokens as CSS custom properties on a root element, then reference them throughout styles.

```css
:root {
  --color-primary: #2563eb;
  --color-surface: #ffffff;
  --spacing-md: 1rem;
  --font-size-body: 1rem;
  --radius-md: 0.5rem;
}
```

### Theme Tokens

Organize tokens in layers:
1. **Primitive tokens**: raw values (`--blue-500: #3b82f6`)
2. **Semantic tokens**: purpose-based aliases (`--color-primary: var(--blue-500)`)
3. **Component tokens**: scoped to a component (`--button-bg: var(--color-primary)`)

Semantic tokens are the primary interface for theming; changing primitive values propagates through the system.

### Theme Switching

- Swap a class or attribute on `<html>` or `<body>` (e.g., `data-theme="dark"`)
- Redefine CSS custom properties under the new selector
- Persist user preference in `localStorage`; apply before first render to avoid flash
- Use `prefers-color-scheme` media query as the default; allow manual override

### System Preference Detection

```js
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
prefersDark.addEventListener('change', (e) => applyTheme(e.matches ? 'dark' : 'light'));
```

---

## Responsive Strategies

### Media Queries

- Define a breakpoint system: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px)
- **Mobile-first** (recommended): base styles for small screens; `min-width` queries add complexity upward
- **Desktop-first**: base styles for large screens; `max-width` queries simplify downward
- Keep breakpoints consistent across the project; define them as CSS custom properties or preprocessor variables
- Avoid device-specific breakpoints; design for content, not for specific devices

### Container Queries

Component-level responsiveness based on the container's size rather than the viewport.

```css
.card-container { container-type: inline-size; }

@container (min-width: 400px) {
  .card { display: flex; }
}
```

- Components adapt to their available space, not the viewport -- essential for reusable components
- Use `container-type: inline-size` on the parent element
- Browser support is broad (2023+); use a polyfill for older browsers if needed
- Name containers with `container-name` when nesting multiple container query contexts

### Fluid Typography and Spacing

Use `clamp()` to create smoothly scaling values between a minimum and maximum.

```css
font-size: clamp(1rem, 0.5rem + 1.5vw, 2rem);
padding: clamp(0.75rem, 2vw, 2rem);
```

- Eliminates the need for multiple breakpoints for font size and spacing
- Combine with a modular type scale for consistent hierarchy
- Viewport-relative units (`vw`, `vh`, `dvh`): use for full-screen layouts; avoid for body text (zoom issues)
- `dvh` (dynamic viewport height) accounts for mobile browser chrome; prefer over `vh` on mobile

---

## Dark Mode

### Implementation

- Define light and dark token sets; switch via `data-theme` attribute or class
- Use `color-scheme: light dark` on `:root` to inform the browser and style native elements (scrollbars, form controls)
- Test both themes: ensure sufficient contrast ratios (WCAG AA: 4.5:1 for body text, 3:1 for large text)

### Color Token Strategy

- Do not hard-code colors in components; always reference semantic tokens
- Dark mode is not just inverting colors: adjust saturation, brightness, and elevation shadows
- Elevated surfaces in dark mode should be lighter, not darker (material elevation model)

### Image Handling

- Provide dark-mode variants for logos, illustrations, and decorative images where needed
- Use `filter: brightness(0.8)` or `opacity` adjustments as a fallback for images without dark variants
- `<picture>` with `prefers-color-scheme` media: serve different image sources per theme

### User Preference Persistence

- Check `localStorage` for a saved preference on page load
- Fall back to `prefers-color-scheme` if no preference is saved
- Apply the theme class/attribute in a blocking `<script>` in `<head>` to prevent flash of wrong theme
- Provide a visible toggle in the UI; update `localStorage` on toggle

---

## CSS Custom Properties

### Naming Conventions

- Use a consistent prefix: `--color-`, `--spacing-`, `--font-`, `--radius-`, `--shadow-`
- Use kebab-case: `--color-primary-500`, `--spacing-lg`
- Document the token set; generate documentation from token definitions if possible

### Scoping

- Define global tokens on `:root`
- Scope component tokens on the component's root class: `.dialog { --dialog-padding: var(--spacing-lg); }`
- Scoped properties inherit to children; use this for contextual theming (e.g., a sidebar with different spacing)

### Fallback Values

```css
color: var(--color-accent, #3b82f6);
```

- Always provide a fallback for custom properties that might not be defined
- Fallbacks are a safety net, not a theming mechanism; ensure all tokens are defined in every theme

### Dynamic Values via JavaScript

```js
document.documentElement.style.setProperty('--header-height', `${measuredHeight}px`);
```

- Use for values that depend on runtime measurement (header height, scroll position)
- Avoid setting many properties per frame; batch updates to prevent layout thrashing

---

## CSS Performance

### Critical CSS

- Inline the CSS needed for above-the-fold content in the HTML `<head>`
- Load remaining CSS asynchronously with `media="print" onload="this.media='all'"`
- Tools: Critters (webpack/Vite plugin), Critical (Node.js), PurgeCSS for unused removal

### Purging Unused Styles

- Remove unused CSS rules in production builds (PurgeCSS, Tailwind's built-in purge)
- Ensure dynamic class names are safelisted so they are not accidentally purged
- Audit CSS coverage with browser DevTools Coverage panel

### Render-Blocking CSS

- Stylesheets in `<head>` without `media` or `async` loading block rendering
- Split CSS by route; load only what the current page needs
- Use `<link rel="preload" as="style">` for CSS needed soon but not immediately

### Layout Thrashing

- Avoid reading layout properties (offsetHeight, getBoundingClientRect) and then writing styles in the same frame
- Batch DOM reads before DOM writes
- Use `requestAnimationFrame` or CSS transitions/animations instead of JS-driven layout changes

---

## CSS Anti-Patterns

### Overly Specific Selectors

- `div.container > ul.list > li.item > a.link` is fragile; any HTML change breaks the style
- Prefer flat, single-class selectors: `.nav-link`
- Specificity wars lead to unmaintainable CSS

### !important Abuse

- `!important` is a last resort for overriding third-party styles, not a regular tool
- If you need `!important` frequently, the architecture has a specificity problem
- Fix the root cause: reduce selector specificity, reorder stylesheets, use a more specific class

### Magic Numbers

- Avoid unexplained numeric values: `margin-top: 37px`
- Use design tokens or document why a specific value is needed
- If a value compensates for another element's size, use a CSS custom property tied to that element

### Deeply Nested Selectors

- Preprocessor nesting beyond 3 levels creates overly specific output
- Flat selectors are easier to override, easier to search, and faster for the browser to match
- Nesting is fine for pseudo-classes and pseudo-elements, not for deeply mirroring DOM structure
