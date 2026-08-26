# Carry On Round The World — Agent Instructions

- Hugo blog (Ananke v2 theme) deployed to Firebase Hosting.

## Quick commands

| What | Command |
|---|---|
| Dev server | `~/.local/bin/starthugod` -> `http://192.168.77.7:1313` (uses `--renderToMemory`, never writes `public/`)|
| Production build | `~/.local/bin/buildhugo` |
| Deploy to Firebase | `firebase deploy` -> `https://carryonrtw.com` |
| lighthouse commands | `lighthouse --help` |
| playwright-cli commands | `playwright-cli --help` |

- Requires **Hugo** (≥ 0.164.0) and **Firebase CLI**.
- Lighthouse is an open-source auditing tool for web page quality.
- playwright-cli is a browser automation framework.

## Architecture

- **Theme:** `github.com/gohugo-ananke/ananke/v2` vendored under `_vendor/`
- **Layouts:** `layouts/` overrides Ananke v2 theme. Custom `.html` files use old `partials.Include()` syntax.
- **Partials:** `layouts/partials/` (also `layouts/_partials/` is in use — same name, underscore prefix; both are honored by Hugo)
- **Shortcodes:** `layouts/_shortcodes/` — `cta`, `gslides` (Google Slides embed), `youtubepl` (YouTube playlist embed), `traveltime` (elapsed-time counter for homepage), `travelstats` (homepage stats table). **Important:** the active directory is `_shortcodes/` (with underscore), not `shortcodes/`. New shortcodes belong in `layouts/_shortcodes/`.
- **Custom CSS:** `assets/ananke/css/custom.css` (picked up by Ananke's asset pipeline); also referenced in `config/_default/hugo.toml` as `params.custom_css`: `custom.css`, `formatted_tables.css`, `next_prev_links.css`. The `formatted_tables.css` and `next_prev_links.css` entries are present as files in assets/ananke/css/.

## Content model

- Site has four standalone pages: home, search, contact and about defined in `content/`.
- Four content sections defined in `config/_default/hugo.toml`:

| Section | Path | Purpose |
|---|---|---|
| travels | `content/travels/` | Travel blog posts (62 posts) |
| articles | `content/articles/` | Travel philosophy, gear, banking (14 posts) |
| packs | `content/packs/` | Backpack evolution documentation (6 posts) |
| van-life | `content/van-life/` | Ford Transit van build (9 posts) |
| static pages | `content/` root | `_index.md`, `about.md`, `contact.md`, `search.md` |

- Pagination: 9 posts per page, path = `page`
- Taxonomies: `tags`, `categories`
- Next/prev navigation: `next-gallery-prev-navbar.html` partial (respects `params.album` per post)
- Images: Hosted in `static/images/` or on Google Photos (googleusercontent URLs) except for each pages banner: featured_image.

## Key config files

- `config/_default/hugo.toml` — baseURL, menu, mainSections, custom CSS, sitemap, analytics
- `config/_default/params.toml` — Ananke theme config, social networks (Bluesky, Mastodon, YouTube, GitHub), share networks
- Giscus comments — widget config in `config/_default/hugo.toml` under `[params.giscus]`, rendered via `layouts/_partials/giscus.html` (repo: `RoninTech/CarryOnRoundTheWorld`). `giscus.json` is Giscus server-side config only (allowed origins + default comment order), served from this repo by giscus.app.
- `firebase.json` — deployment target (`public/`)

## Search & comments

- **Search:** Pagefind, pre-built index in `static/_pagefind/` (gitignored). Regenerate with `buildhugo` or `npx pagefind --source public` after building.
- **Comments:** Giscus, wired to GitHub Discussions via `layouts/_partials/giscus.html` (config in `[params.giscus]`)

## Git-ignored build artifacts

- `public/` — Hugo output
- `static/_pagefind/` — Pagefind index
- `.firebase/`, `logs/`

## Content scripts

- `content/lpcount.py` — validates image dimensions in `.md` files against expected widths (210, 315, 370, 1000)
- `scrape_photos.py` — scrapes Google Photos URLs (caches to `.scrape_cache.json`)
- `scripts/fix_image_heights.py` — adds `height` attrs to body Google Photos `<img>` tags (aspect ratios from `crap/output.txt`; unknowns fetched and cached in `scripts/.img_dim_cache.json`). Run `python3 scripts/fix_image_heights.py --dry-run` to preview, then apply without flags. Idempotent; re-run after adding new posts with Google Photos images so they don't ship without `height`.

## Gotchas

- **`public/` is generated at build time, not committed and gitignored** — it exists for local dev but is never deployed from git. Firebase deploys from the checked-out `public/` directory.
- **Giscus origins:** `carryonrtw.com` and `192.168.77.7:1313` are in `giscus.json`. Local dev requires the latter origin.
- **Images:** External Google Photos URLs — Except for featured_image banners which live in `static/images/featured` directory.
- **--FIXED-- (2026-08-23) Deploy risk: the dev server no longer rewrites `public/`.** `starthugod` now runs `hugo server --renderToMemory`, which serves everything from memory and never writes `public/`, and runs `buildhugo` on exit. `public/` therefore always holds the last production build, and `firebase deploy` is safe at any time. Verified: `public/` mtime unchanged while the dev server ran; stopping the server fired the trailing `buildhugo`. (History: before 2026-08-23, `hugo server` rewrote `public/` with `baseURL 192.168.77.7:1313` baked into canonicals/`og:url`/hero URLs — see the 2026-08-22 audit and git history.)
