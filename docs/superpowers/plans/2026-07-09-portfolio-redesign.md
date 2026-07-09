# Portfolio Redesign michielmeilink.com — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Herbouw michielmeilink.com als licht & creatief portfolio met vaste zijbalk (categorieën + clientnamen), gefilterd werk-grid met bijschriften, en een vast compact case-sjabloon — puur statisch (HTML/CSS/vanilla JS) op GitHub Pages.

**Architecture:** Eén gedeeld `menu.html` (zijbalk, desktop) / topbalk-overlay (mobiel) dat elke pagina via een klein JS-fetchje inlaadt; één nieuw `css/main.css` met design-tokens (kleuren, logo-verloop, fonts als custom properties) dat de twee oude CSS-bestanden vervangt; hash-gebaseerd categoriefilter (`/#animation`) in `js/site.js`. Alle bestaande case-URL's blijven intact; alle paden worden root-relatief (`/css/main.css`) zodat elke paginadiepte hetzelfde werkt.

**Tech Stack:** HTML, CSS, vanilla JS (geen build-stap), self-hosted woff2-fonts, GitHub Pages + CNAME `michielmeilink.com`.

**Spec:** `docs/superpowers/specs/2026-07-09-portfolio-redesign-design.md`

## Global Constraints

- Puur statisch: HTML + CSS + een klein beetje vanilla JS. Geen build-stap, geen framework, geen CDN-dependencies (ook het Google-Fonts-`@import` in de oude `menu.css` verdwijnt).
- Alle bestaande case-URL's blijven werken: bestands- en mapnamen onder `cases/` wijzigen NIET.
- Video's blijven YouTube-embeds; bestaande wrapper-classes `video-responsive-wrapper` (16:9), `video-square-wrapper` (1:1), `video-portrait-wrapper` (9:16) blijven bestaan in de nieuwe CSS.
- Kleuren: achtergrond gebroken wit `#faf9f6` (géén hard #fff), tekst donkergrijs `#23252b`, accent-verloop `linear-gradient(100deg, #0072ff, #00c8ff)` — spaarzaam (actieve categorie, hover, kleine details).
- Categorieën heten Engels: **Animation**, **Video**, **AI** (hash `#animation`, `#video`, `#ai`). AI heeft nog 0 projecten en wordt dus nog NIET in het menu opgenomen (categorie met 0 projecten niet tonen).
- Contact onderaan zijbalk: GEEN e-mailadres. Wel: About-link + social-iconen naar `https://www.linkedin.com/in/michiel-meilink-009546b3/` en `https://www.instagram.com/michielmeilink/`.
- `lang="en"` op elke `<html>`; alle site-teksten blijven Engels; bestaande case-teksten blijven inhoudelijk ongewijzigd.
- `prefers-reduced-motion: reduce` schakelt animaties/overgangen uit.
- Elke pagina krijgt unieke `<title>`, `<meta name="description">` en Open Graph-tags (og:title, og:description, og:image met absolute URL `https://michielmeilink.com/...`, og:url, og:type).
- Testen: er is geen testframework; elke taak eindigt met expliciete verificatiecommando's (grep/curl) + browsercheck. Lokaal serveren met `python3 -m http.server 8000` vanuit de repo-root (nodig omdat `fetch()` niet op `file://` werkt).
- Committen per taak; NIET pushen tot de eindtaak (Task 10) — de live site blijft ongewijzigd tot alles af is.
- Repo-pad: `/Users/michiel/Documents/michielmeilink.github.io` (alle commando's gaan uit van deze cwd).

## Canonieke projectvolgorde (grid, zijbalk én prev/next-ketting)

Deze volgorde is heilig door het hele plan; prev/next wikkelt rond (project 20 → next = project 1).

| # | map onder `cases/` | Grid-label (client) | Type (bijschrift) | Categorie | Thumb in `thumbs/` |
|---|---|---|---|---|---|
| 1 | `durex` | Durex | 2D animation | animation | `durex_standjegezocht.jpg` |
| 2 | `frieslandcampina` | FrieslandCampina | Video production | video | `frieslandcampina.jpg` |
| 3 | `doritos` | Doritos | Social animation | animation | `doritos.jpg` |
| 4 | `quakercruesli` | Quaker Cruesli | TV commercial & social | animation | `quakercruesli.jpg` |
| 5 | `verkade` | Verkade | Stop-motion | video | `verkade.jpg` |
| 6 | `daelmans` | Daelmans | 2.5D product animation | animation | `daelmans.jpg` |
| 7 | `ecoline` | Talens Ecoline | Promo & social content | video | `ecoline.jpg` |
| 8 | `arriva` | Arriva Spitsmuis | 2D animation | animation | `arriva_spitsmuis.jpg` |
| 9 | `raakpuur` | Raak Puur | Stop-motion | video | `raakpuur.jpg` |
| 10 | `jan_pannenkoek` | JAN Pannenkoek | 2D animation | animation | `jan_pannenkoek.jpg` |
| 11 | `bb_showreel` | Brand Builders | Showreel | video | `bb_showreel.jpg` |
| 12 | `arrivaopstapper` | Arriva Opstapper | 2D animation | animation | `arriva_opstapper.jpg` |
| 13 | `capetracks` | Capetracks | Brand animation | animation | `capetracks.jpg` |
| 14 | `vegter` | Vegter | Campaign videos | video | `vegter.jpg` |
| 15 | `arrivadienstregeling` | Arriva Dienstregeling | 2D animation | animation | `arriva_dienstregeling.jpg` |
| 16 | `summerrain` | Summer Rain | Instruction videos | video | `summerrain.jpg` |
| 17 | `livium` | Livium | Logo animation | animation | `livium.jpg` |
| 18 | `arturo` | Arturo | Campaign visuals | video | `arturo.jpg` |
| 19 | `ezeetabs` | Ezeetabs | Social animation | animation | `ezeetabs.jpg` |
| 20 | `combi_outboards` | Combi Outboards | 2D animation | animation | `combi_outboards.jpg` |

HTML-bestand per case = `cases/<map>/<map>.html` (bv. `cases/durex/durex.html`).

---

### Task 1: Repo opschonen

**Files:**
- Delete (git rm): `.DS_Store`, `cases/.DS_Store`, alle `cases/*/.DS_Store`, `grid.html`, `cases/_case/case.php`, `cases/css/menu.css`, `cases/css/styles.css`, `images/DSC08251-min.jpg`, `images/logo3.png` (laatste twee alléén na de grep-check in stap 1)

**Interfaces:**
- Produces: schone repo zonder ongebruikte bestanden; latere taken hoeven nergens rekening te houden met `cases/css/` of `_case/`.

- [x] **Step 1: Controleer dat de te verwijderen bestanden nergens gerefereerd worden**

Run:
```bash
cd /Users/michiel/Documents/michielmeilink.github.io
grep -rn "grid.html\|_case\|cases/css\|DSC08251\|logo3" --include="*.html" .
```
Expected: geen output (exit code 1). Als een bestand wél gerefereerd wordt: dat bestand NIET verwijderen en de referentie noteren in het taakverslag.

- [x] **Step 2: Verwijder de bestanden uit git en van schijf**

```bash
cd /Users/michiel/Documents/michielmeilink.github.io
git rm -r --ignore-unmatch .DS_Store cases/.DS_Store grid.html cases/_case cases/css images/DSC08251-min.jpg images/logo3.png
find . -name ".DS_Store" -not -path "./.git/*" -delete
rmdir files 2>/dev/null || true
```
(`files/` is een lege, niet-getrackte map; `images/IMG_6923.jpg` blijft — die is de hero op about.html; `images/logo5.png` blijft — dat is het logo.)

- [x] **Step 3: Verifieer**

Run: `git status --short && git ls-files | grep -iE 'DS_Store|grid|_case|cases/css|DSC08251|logo3' || echo SCHOON`
Expected: alleen `D`-regels in status, daarna `SCHOON`.

- [x] **Step 4: Commit**

```bash
git commit -m "chore: remove unused files and .DS_Store from repo"
```

---

### Task 2: Afbeeldingen comprimeren

**Files:**
- Modify: alle 20 bestanden in `thumbs/`, plus `images/IMG_6923.jpg`

**Interfaces:**
- Produces: alle thumbs exact 800×800px, totaal `thumbs/` < 1,5 MB. Bestandsnamen wijzigen NIET (index.html verwijst er straks naar).

- [x] **Step 1: Resize de ene te grote thumb en hercomprimeer alles**

```bash
cd /Users/michiel/Documents/michielmeilink.github.io
sips -Z 800 thumbs/arriva_dienstregeling.jpg
for f in thumbs/*.jpg; do sips -s format jpeg -s formatOptions 70 "$f" --out "$f" >/dev/null; done
sips -Z 1600 images/IMG_6923.jpg
sips -s format jpeg -s formatOptions 70 images/IMG_6923.jpg --out images/IMG_6923.jpg >/dev/null
```

- [x] **Step 2: Verifieer maten en totaalgrootte**

Run: `sips -g pixelWidth thumbs/arriva_dienstregeling.jpg && du -sh thumbs images && find thumbs -size +150k`
Expected: pixelWidth 800; `thumbs` ≤ ~1,5M (was 3,1M); geen bestanden > 150 kB. Controleer visueel (Quick Look) dat 2–3 thumbs er nog goed uitzien; bij zichtbare artefacten `formatOptions 80` gebruiken en opnieuw draaien vanaf de git-versie (`git checkout thumbs/ && …`).

- [x] **Step 3: Commit**

```bash
git add thumbs images/IMG_6923.jpg
git commit -m "perf: compress thumbnails (800px, q70) and about hero image"
```

---

### Task 3: Fontkeuze (checkpoint met Michiel) + self-hosten

**Files:**
- Create: `fonts/` met 4 woff2-bestanden (display 500 + 700, body regular + 500)
- Create (tijdelijk, niet committen): `font-preview.html` in de repo-root

**Interfaces:**
- Produces: exacte bestandsnamen voor Task 4's `@font-face`:
  `fonts/display-500.woff2`, `fonts/display-700.woff2`, `fonts/body-400.woff2`, `fonts/body-500.woff2` — plus de gekozen font-family-namen voor de CSS-variabelen `--font-display` en `--font-body`.

- [x] **Step 1: Maak de preview-pagina met de drie kandidaat-combinaties**

Schrijf `font-preview.html` (laadt voor de preview éénmalig van Google Fonts CDN — dit bestand wordt niet gecommit en daarna verwijderd):

```html
<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<title>Fontproef — michielmeilink.com</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Sora:wght@600;700&family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
  body { margin:0; background:#faf9f6; color:#23252b; }
  section { padding:48px clamp(20px,6vw,90px); border-bottom:1px solid #e8e6e0; }
  .label { font:600 12px/-, sans-serif; font-family:sans-serif; letter-spacing:.14em; text-transform:uppercase; color:#6b6f76; }
  h1 { font-size:clamp(30px,5vw,52px); margin:.3em 0; letter-spacing:-.01em; }
  .meta { font-family:'Inter'; font-size:12px; letter-spacing:.12em; text-transform:uppercase; color:#6b6f76; }
  p { font-family:'Inter'; font-weight:400; font-size:15.5px; line-height:1.65; max-width:620px; }
  .accent { background:linear-gradient(100deg,#0072ff,#00c8ff); -webkit-background-clip:text; background-clip:text; color:transparent; }
  .a h1 { font-family:'Space Grotesk'; font-weight:700; }
  .b h1 { font-family:'Sora'; font-weight:700; }
  .c h1 { font-family:'Fraunces'; font-weight:600; }
</style>
</head>
<body>
<section class="a"><div class="label">1 — Space Grotesk + Inter (aanbevolen: technisch-speels, past bij motion design)</div>
  <h1>Durex — <span class="accent">2D animation</span></h1>
  <div class="meta">Client: Durex &nbsp; Agency: Brand Builders &nbsp; Role: Animation</div>
  <p>The Netherlands does not yet have a well-known stand that they are known for. For Durex, Brand Builders came up with a concept in which we search for the stand of the Dutch.</p></section>
<section class="b"><div class="label">2 — Sora + Inter (ronder, vriendelijker)</div>
  <h1>Durex — <span class="accent">2D animation</span></h1>
  <div class="meta">Client: Durex &nbsp; Agency: Brand Builders &nbsp; Role: Animation</div>
  <p>The Netherlands does not yet have a well-known stand that they are known for. For Durex, Brand Builders came up with a concept in which we search for the stand of the Dutch.</p></section>
<section class="c"><div class="label">3 — Fraunces + Inter (karaktervol serif, editorial)</div>
  <h1>Durex — <span class="accent">2D animation</span></h1>
  <div class="meta">Client: Durex &nbsp; Agency: Brand Builders &nbsp; Role: Animation</div>
  <p>The Netherlands does not yet have a well-known stand that they are known for. For Durex, Brand Builders came up with a concept in which we search for the stand of the Dutch.</p></section>
</body>
</html>
```

- [x] **Step 2: CHECKPOINT — laat Michiel kiezen**

Open `font-preview.html` in de browser (`open font-preview.html`) en vraag Michiel welke van de drie combinaties het wordt. **Wacht op antwoord; niet verder zonder keuze.** Kiest hij "kies jij" → combinatie 1 (Space Grotesk + Inter).

- [x] **Step 3: Download de gekozen fonts als woff2**

Voor combinatie 1 (pas de eerste URL aan bij keuze 2 → `sora?...&variants=600,700` of keuze 3 → `fraunces?...&variants=600,700`):

```bash
cd /Users/michiel/Documents/michielmeilink.github.io
mkdir -p fonts
curl -sL "https://gwfh.mranftl.com/api/fonts/space-grotesk?download=zip&subsets=latin&variants=500,700&formats=woff2" -o /tmp/display.zip
curl -sL "https://gwfh.mranftl.com/api/fonts/inter?download=zip&subsets=latin&variants=regular,500&formats=woff2" -o /tmp/body.zip
unzip -o /tmp/display.zip -d /tmp/display && unzip -o /tmp/body.zip -d /tmp/body
cp /tmp/display/*-500.woff2 fonts/display-500.woff2
cp /tmp/display/*-700.woff2 fonts/display-700.woff2
cp /tmp/body/*-regular.woff2 fonts/body-400.woff2
cp /tmp/body/*-500.woff2 fonts/body-500.woff2
rm font-preview.html
```
Fallback als gwfh.mranftl.com niet bereikbaar is: download de familie via https://fonts.google.com ("Get font" → download), pak de statische woff2/ttf-varianten en converteer ttf indien nodig NIET — gebruik dan de variable-font woff2 en noteer dat in het taakverslag.

- [x] **Step 4: Verifieer**

Run: `ls -la fonts/ && file fonts/*.woff2`
Expected: 4 bestanden, elk herkend als "Web Open Font Format (Version 2)", elk < 80 kB.

- [x] **Step 5: Commit**

```bash
git add fonts
git commit -m "feat: self-host chosen webfonts (display + body, woff2)"
```

---

### Task 4: Nieuwe stylesheet `css/main.css`

**Files:**
- Create: `css/main.css`
- (De oude `css/styles.css` en `css/menu.css` blijven voorlopig staan — pagina's verwijzen er nog naar; ze worden in Task 10 verwijderd.)

**Interfaces:**
- Consumes: `fonts/display-500.woff2`, `fonts/display-700.woff2`, `fonts/body-400.woff2`, `fonts/body-500.woff2` (Task 3). Als in Task 3 een andere familie dan Space Grotesk/Inter is gekozen: pas ALLEEN de `font-family`-namen in de `@font-face`-blokken en de twee custom properties aan.
- Produces: alle class-namen die Task 5–9 gebruiken: `.sidebar`, `.sidebar-inner`, `.mobile-bar`, `.menu-toggle`, `.menu-logo`, `.menu-tagline`, `.menu-nav`, `.menu-all`, `.menu-cat`, `.menu-cat-title`, `.menu-foot`, `.menu-social`, `.is-active`, `.content`, `.grid`, `.tile`, `.tile-media`, `.tile-caption`, `.tile-client`, `.tile-type`, `.case-article`, `.case-meta`, `.case-intro`, `.case`, `.case-nav`, `.case-nav-prev`, `.case-nav-next`, `.video-responsive-wrapper`, `.video-square-wrapper`, `.video-portrait-wrapper`, `.about-hero`, `.noscript-nav`, `body.menu-open`, `html.no-js`.

- [x] **Step 1: Schrijf `css/main.css` integraal**

```css
/* ===== Fonts (self-hosted) ===== */
@font-face { font-family: 'Space Grotesk'; src: url('/fonts/display-500.woff2') format('woff2'); font-weight: 500; font-display: swap; }
@font-face { font-family: 'Space Grotesk'; src: url('/fonts/display-700.woff2') format('woff2'); font-weight: 700; font-display: swap; }
@font-face { font-family: 'Inter'; src: url('/fonts/body-400.woff2') format('woff2'); font-weight: 400; font-display: swap; }
@font-face { font-family: 'Inter'; src: url('/fonts/body-500.woff2') format('woff2'); font-weight: 500; font-display: swap; }

/* ===== Tokens ===== */
:root {
  --bg: #faf9f6;
  --ink: #23252b;
  --ink-soft: #6b6f76;
  --line: #e8e6e0;
  --accent: #0072ff;
  --grad: linear-gradient(100deg, #0072ff, #00c8ff);
  --font-display: 'Space Grotesk', 'Helvetica Neue', Arial, sans-serif;
  --font-body: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --sidebar-w: 250px;
}

/* ===== Base ===== */
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  background: var(--bg);
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 15px;
  font-weight: 400;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}
img { max-width: 100%; }
a { color: inherit; text-decoration: none; }
h1, h2, h3 { font-family: var(--font-display); color: var(--ink); }

/* Verloop-tekst (actief/hover-accent) */
.grad-text, .tile:hover .tile-client, .tile:focus-visible .tile-client,
.menu-cat-title.is-active, .menu-all.is-active,
.case-nav a:hover, .menu-foot a:hover, .menu-cat li a:hover {
  background: var(--grad);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* ===== Layout: sidebar + content ===== */
.content {
  margin-left: var(--sidebar-w);
  padding: 44px clamp(20px, 4vw, 64px) 64px;
  min-height: 100vh;
}
.sidebar {
  position: fixed;
  top: 0; left: 0; bottom: 0;
  width: var(--sidebar-w);
  background: var(--bg);
  border-right: 1px solid var(--line);
  overflow-y: auto;
  z-index: 30;
}
.sidebar-inner {
  display: flex;
  flex-direction: column;
  gap: 34px;
  min-height: 100%;
  padding: 36px 30px 28px;
}
.menu-logo img { display: block; width: 54px; height: auto; }
.menu-tagline { margin: 12px 0 0; font-size: 12.5px; letter-spacing: .02em; color: var(--ink-soft); }
.menu-nav { display: flex; flex-direction: column; gap: 26px; }
.menu-all, .menu-cat-title {
  display: block;
  font-family: var(--font-display);
  font-weight: 500;
  font-size: 12.5px;
  letter-spacing: .13em;
  text-transform: uppercase;
  color: var(--ink);
}
.menu-cat-title { margin-bottom: 9px; }
.menu-cat ul { list-style: none; margin: 0; padding: 0; }
.menu-cat li a {
  display: block;
  padding: 3px 0;
  font-size: 13.5px;
  color: var(--ink-soft);
}
.menu-cat li a.is-active { color: var(--ink); font-weight: 500; }
.menu-foot {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding-top: 26px;
  border-top: 1px solid var(--line);
  font-size: 13.5px;
}
.menu-foot a.is-active { font-weight: 500; }
.menu-social { display: flex; gap: 14px; }
.menu-social a { display: inline-flex; color: var(--ink-soft); }
.menu-social a:hover { color: var(--accent); }
.menu-social svg { width: 18px; height: 18px; fill: currentColor; }

/* Mobiele balk (verborgen op desktop) */
.mobile-bar { display: none; }

/* ===== No-JS fallback ===== */
html.no-js .sidebar { display: none; }
html.no-js .content { margin-left: 0; }
.noscript-nav {
  display: flex;
  gap: 24px;
  padding: 18px clamp(20px, 4vw, 64px);
  border-bottom: 1px solid var(--line);
  font-family: var(--font-display);
  font-weight: 500;
}

/* ===== Werk-grid ===== */
.page-intro { max-width: 560px; margin: 0 0 34px; }
.page-intro h1 { font-size: clamp(24px, 3vw, 32px); font-weight: 700; letter-spacing: -.01em; margin: 0 0 6px; }
.page-intro p { margin: 0; color: var(--ink-soft); }
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 34px 26px;
  max-width: 1400px;
}
.tile { display: block; }
.tile[hidden] { display: none; }
.tile-media {
  display: block;
  overflow: hidden;
  border-radius: 10px;
  background: var(--line);
}
.tile-media img { display: block; width: 100%; height: auto; }
.tile-caption {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  gap: 12px;
  margin-top: 10px;
}
.tile-client { font-family: var(--font-display); font-weight: 500; font-size: 14.5px; }
.tile-type { font-size: 12.5px; color: var(--ink-soft); white-space: nowrap; }

/* ===== Case-pagina ===== */
.case-article { max-width: 980px; }
.case-article h1 {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 700;
  letter-spacing: -.015em;
  margin: 0 0 20px;
}
.case-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 36px;
  margin: 0 0 26px;
  padding: 16px 0;
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}
.case-meta > div { margin: 0; }
.case-meta dt {
  font-size: 11px;
  letter-spacing: .13em;
  text-transform: uppercase;
  color: var(--ink-soft);
  margin-bottom: 2px;
}
.case-meta dd { margin: 0; font-size: 14px; font-weight: 500; }
.case-intro { max-width: 640px; font-size: 15.5px; margin: 0 0 36px; }
div.case { width: 100%; max-width: 980px; margin: 0 0 26px; }
div.case img, div.case video { max-width: 100%; height: auto; }
.case-nav {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  margin-top: 48px;
  padding-top: 22px;
  border-top: 1px solid var(--line);
}
.case-nav a { font-family: var(--font-display); font-weight: 500; font-size: 15px; }
.case-nav a span {
  display: block;
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 11px;
  letter-spacing: .13em;
  text-transform: uppercase;
  color: var(--ink-soft);
  margin-bottom: 2px;
}
.case-nav-next { text-align: right; margin-left: auto; }

/* ===== Video-wrappers (bestaand gedrag behouden) ===== */
.video-responsive-wrapper { position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; border-radius: 10px; }
.video-square-wrapper { position: relative; width: 100%; padding-bottom: 100%; height: 0; overflow: hidden; border-radius: 10px; }
.video-portrait-wrapper { position: relative; width: 100%; padding-bottom: 177.77%; height: 0; overflow: hidden; border-radius: 10px; }
.video-responsive-wrapper iframe, .video-square-wrapper iframe, .video-portrait-wrapper iframe {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;
}

/* Meerdere vierkante/portret-video's naast elkaar (bestaand gedrag) */
.video-container-horizontal { display: flex; flex-wrap: wrap; gap: 20px; }
.video-container-horizontal .case { flex: 1 1 100%; margin: 0 0 6px; min-width: 0; }
@media (min-width: 768px) {
  .video-container-horizontal .case { flex: 1 1 45%; }
}

/* ===== About ===== */
.about-hero {
  border-radius: 12px;
  width: 100%;
  max-width: 980px;
  height: auto;
  display: block;
  margin-bottom: 34px;
}

/* ===== Beweging (alleen zonder reduced-motion) ===== */
@media (prefers-reduced-motion: no-preference) {
  .tile-media img { transition: transform .45s cubic-bezier(.22, .61, .36, 1); }
  .tile:hover .tile-media img, .tile:focus-visible .tile-media img { transform: scale(1.05); }
  .menu-cat li a, .menu-foot a, .menu-social a { transition: color .15s ease; }
  .grid .tile { opacity: 0; transform: translateY(12px); animation: tile-in .5s ease forwards; }
  .grid .tile:nth-child(1) { animation-delay: .04s; }
  .grid .tile:nth-child(2) { animation-delay: .09s; }
  .grid .tile:nth-child(3) { animation-delay: .14s; }
  .grid .tile:nth-child(4) { animation-delay: .19s; }
  .grid .tile:nth-child(5) { animation-delay: .24s; }
  .grid .tile:nth-child(6) { animation-delay: .29s; }
  .grid .tile:nth-child(n+7) { animation-delay: .34s; }
}
@keyframes tile-in { to { opacity: 1; transform: none; } }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition: none !important; animation: none !important; }
}

/* ===== Responsive ===== */
@media (max-width: 1100px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 800px) {
  .sidebar {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: auto;
    width: 100%;
    border-right: none;
    border-bottom: 1px solid var(--line);
    overflow: visible;
  }
  .mobile-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 60px;
    padding: 0 20px;
  }
  .mobile-bar img { display: block; width: 40px; height: auto; }
  .menu-toggle {
    width: 34px; height: 34px;
    border: 0; padding: 0;
    background: none;
    cursor: pointer;
    position: relative;
  }
  .menu-toggle::before, .menu-toggle::after {
    content: '';
    position: absolute;
    left: 4px; right: 4px;
    height: 2.5px;
    border-radius: 2px;
    background: var(--ink);
    transition: transform .25s ease, top .25s ease;
  }
  .menu-toggle::before { top: 12px; }
  .menu-toggle::after { top: 20px; }
  body.menu-open .menu-toggle::before { top: 16px; transform: rotate(45deg); }
  body.menu-open .menu-toggle::after { top: 16px; transform: rotate(-45deg); }
  .sidebar-inner { display: none; }
  body.menu-open .sidebar-inner {
    display: flex;
    position: fixed;
    top: 60px; left: 0; right: 0; bottom: 0;
    background: var(--bg);
    overflow-y: auto;
    z-index: 40;
  }
  body.menu-open { overflow: hidden; }
  .content { margin-left: 0; padding: 84px 20px 48px; }
  html.no-js .content { padding-top: 24px; }
  .case-nav a { font-size: 14px; }
}
@media (max-width: 640px) {
  .grid { grid-template-columns: 1fr; }
}
```

- [x] **Step 2: Verifieer dat de CSS parsebaar is en de fontpaden kloppen**

Run:
```bash
cd /Users/michiel/Documents/michielmeilink.github.io
grep -c "@font-face" css/main.css
grep -o "/fonts/[a-z0-9-]*\.woff2" css/main.css | sort -u | while read p; do test -f ".${p}" && echo "OK ${p}" || echo "ONTBREEKT ${p}"; done
```
Expected: `4`, daarna vier regels `OK /fonts/...`.

- [x] **Step 3: Commit**

```bash
git add css/main.css
git commit -m "feat: add main.css with design tokens, sidebar layout, grid and case template styles"
```

---

### Task 5: Gedeeld menu (`menu.html`) + `js/site.js`

**Files:**
- Create (overschrijft bestaand): `menu.html`
- Create: `js/site.js`

**Interfaces:**
- Consumes: class-namen uit `css/main.css` (Task 4); canonieke projectvolgorde (tabel bovenaan dit plan).
- Produces: elke pagina bevat straks dit vaste snippet (Task 6–9 gebruiken het letterlijk):
  ```html
  <aside id="site-menu" class="sidebar"></aside>
  <noscript><nav class="noscript-nav"><a href="/index.html">Work</a><a href="/about.html">About</a></nav></noscript>
  ```
  plus in `<head>`: `<script src="/js/site.js" defer></script>` en op `<html>`: `class="no-js"`.

- [x] **Step 1: Schrijf `menu.html` integraal (vervangt de oude inhoud volledig)**

```html
<div class="mobile-bar">
  <a href="/index.html" aria-label="Michiel Meilink — home"><img src="/images/logo5.png" alt="MM logo" width="40" height="34"></a>
  <button class="menu-toggle" type="button" aria-expanded="false" aria-label="Menu"></button>
</div>
<div class="sidebar-inner">
  <div>
    <a class="menu-logo" href="/index.html" aria-label="Michiel Meilink — home"><img src="/images/logo5.png" alt="MM logo" width="54" height="46"></a>
    <p class="menu-tagline">Motion design &amp; video editing</p>
  </div>
  <nav class="menu-nav" aria-label="Work">
    <a class="menu-all" href="/index.html">All work</a>
    <section class="menu-cat">
      <a class="menu-cat-title" href="/#animation">Animation</a>
      <ul>
        <li><a href="/cases/durex/durex.html">Durex</a></li>
        <li><a href="/cases/doritos/doritos.html">Doritos</a></li>
        <li><a href="/cases/quakercruesli/quakercruesli.html">Quaker Cruesli</a></li>
        <li><a href="/cases/daelmans/daelmans.html">Daelmans</a></li>
        <li><a href="/cases/arriva/arriva.html">Arriva Spitsmuis</a></li>
        <li><a href="/cases/jan_pannenkoek/jan_pannenkoek.html">JAN Pannenkoek</a></li>
        <li><a href="/cases/arrivaopstapper/arrivaopstapper.html">Arriva Opstapper</a></li>
        <li><a href="/cases/capetracks/capetracks.html">Capetracks</a></li>
        <li><a href="/cases/arrivadienstregeling/arrivadienstregeling.html">Arriva Dienstregeling</a></li>
        <li><a href="/cases/livium/livium.html">Livium</a></li>
        <li><a href="/cases/ezeetabs/ezeetabs.html">Ezeetabs</a></li>
        <li><a href="/cases/combi_outboards/combi_outboards.html">Combi Outboards</a></li>
      </ul>
    </section>
    <section class="menu-cat">
      <a class="menu-cat-title" href="/#video">Video</a>
      <ul>
        <li><a href="/cases/frieslandcampina/frieslandcampina.html">FrieslandCampina</a></li>
        <li><a href="/cases/verkade/verkade.html">Verkade</a></li>
        <li><a href="/cases/ecoline/ecoline.html">Talens Ecoline</a></li>
        <li><a href="/cases/raakpuur/raakpuur.html">Raak Puur</a></li>
        <li><a href="/cases/bb_showreel/bb_showreel.html">Brand Builders</a></li>
        <li><a href="/cases/vegter/vegter.html">Vegter</a></li>
        <li><a href="/cases/summerrain/summerrain.html">Summer Rain</a></li>
        <li><a href="/cases/arturo/arturo.html">Arturo</a></li>
      </ul>
    </section>
  </nav>
  <div class="menu-foot">
    <a href="/about.html">About</a>
    <div class="menu-social">
      <a href="https://www.linkedin.com/in/michiel-meilink-009546b3/" aria-label="LinkedIn" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.86 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/></svg></a>
      <a href="https://www.instagram.com/michielmeilink/" aria-label="Instagram" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 0 1-1.38-.9 3.7 3.7 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23-.06-1.27-.07-1.65-.07-4.85s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41 1.27-.06 1.65-.07 4.85-.07zM12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.9 5.9 0 0 0-2.13 1.38A5.9 5.9 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.8.72 1.47 1.38 2.13a5.9 5.9 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.9 5.9 0 0 0 2.13-1.38 5.9 5.9 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.9 5.9 0 0 0-1.38-2.13A5.9 5.9 0 0 0 19.86.63c-.76-.3-1.64-.5-2.91-.56C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm7.85-10.4a1.44 1.44 0 1 1-2.88 0 1.44 1.44 0 0 1 2.88 0z"/></svg></a>
    </div>
  </div>
</div>
```

- [x] **Step 2: Schrijf `js/site.js` integraal**

```js
document.documentElement.classList.replace('no-js', 'js');

(function () {
  'use strict';

  var CATEGORIES = ['animation', 'video', 'ai'];

  function currentCategory() {
    var hash = location.hash.slice(1);
    return CATEGORIES.indexOf(hash) !== -1 ? hash : '';
  }

  function applyFilter() {
    var cat = currentCategory();
    var tiles = document.querySelectorAll('.grid .tile');
    for (var i = 0; i < tiles.length; i++) {
      var cats = (tiles[i].getAttribute('data-category') || '').split(' ');
      tiles[i].hidden = cat !== '' && cats.indexOf(cat) === -1;
    }
    var titles = document.querySelectorAll('.menu-cat-title');
    for (var j = 0; j < titles.length; j++) {
      var isActive = cat !== '' && titles[j].getAttribute('href') === '/#' + cat;
      titles[j].classList.toggle('is-active', isActive);
    }
    var all = document.querySelector('.menu-all');
    if (all) {
      var onHome = location.pathname === '/' || /\/index\.html$/.test(location.pathname);
      all.classList.toggle('is-active', onHome && cat === '');
    }
  }

  function markActivePage(scope) {
    var links = scope.querySelectorAll('a[href^="/cases/"], a[href="/about.html"]');
    for (var i = 0; i < links.length; i++) {
      if (links[i].pathname === location.pathname) links[i].classList.add('is-active');
    }
  }

  function initToggle(scope) {
    var btn = scope.querySelector('.menu-toggle');
    if (!btn) return;
    btn.addEventListener('click', function () {
      var open = document.body.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    scope.addEventListener('click', function (e) {
      var link = e.target.closest && e.target.closest('a');
      if (link && document.body.classList.contains('menu-open')) {
        document.body.classList.remove('menu-open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  fetch('/menu.html')
    .then(function (r) { return r.text(); })
    .then(function (html) {
      var mount = document.getElementById('site-menu');
      if (!mount) return;
      mount.innerHTML = html;
      markActivePage(mount);
      initToggle(mount);
      applyFilter();
    });

  window.addEventListener('hashchange', applyFilter);
  applyFilter();
})();
```

- [x] **Step 3: Verifieer links in menu.html tegen de bestaande bestanden**

Run:
```bash
cd /Users/michiel/Documents/michielmeilink.github.io
grep -o 'href="/cases/[^"]*"' menu.html | sed 's/href="\(.*\)"/\1/' | while read p; do test -f ".${p}" && echo "OK ${p}" || echo "KAPOT ${p}"; done | sort | uniq -c
```
Expected: `20 OK`-regels (via uniq-telling: alleen OK, nul KAPOT).

- [x] **Step 4: Commit**

```bash
git add menu.html js/site.js
git commit -m "feat: shared sidebar menu with categories and hash-filter script"
```

---

### Task 6: Homepage `index.html` (grid + filter + meta)

**Files:**
- Rewrite: `index.html`

**Interfaces:**
- Consumes: snippet + `js/site.js` (Task 5), classes uit `css/main.css` (Task 4), canonieke volgorde-tabel.
- Produces: 20 `.tile`-elementen met `data-category`, in canonieke volgorde.

- [x] **Step 1: Schrijf `index.html` integraal**

Kop en shell exact zo; de 20 tegels volgen de canonieke tabel (hieronder staan alle 20 uitgeschreven):

```html
<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<title>Michiel Meilink — Motion design &amp; video editing</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Portfolio of Michiel Meilink, motion designer and video editor. Animation and video work for Durex, FrieslandCampina, Doritos, Quaker, Arriva and more.">
<meta property="og:title" content="Michiel Meilink — Motion design &amp; video editing">
<meta property="og:description" content="Animation and video work for Durex, FrieslandCampina, Doritos, Quaker, Arriva and more.">
<meta property="og:image" content="https://michielmeilink.com/thumbs/bb_showreel.jpg">
<meta property="og:url" content="https://michielmeilink.com/">
<meta property="og:type" content="website">
<link rel="icon" href="/favicon.ico">
<link rel="stylesheet" href="/css/main.css">
<script src="/js/site.js" defer></script>
</head>
<body>
<aside id="site-menu" class="sidebar"></aside>
<noscript><nav class="noscript-nav"><a href="/index.html">Work</a><a href="/about.html">About</a></nav></noscript>
<main class="content">
  <header class="page-intro">
    <h1>Michiel Meilink</h1>
    <p>Motion design &amp; video editing for brands like Durex, FrieslandCampina, Doritos and Arriva.</p>
  </header>
  <div class="grid">
    <a class="tile" data-category="animation" href="/cases/durex/durex.html">
      <span class="tile-media"><img src="/thumbs/durex_standjegezocht.jpg" alt="Durex — 2D animation" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Durex</span><span class="tile-type">2D animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/frieslandcampina/frieslandcampina.html">
      <span class="tile-media"><img src="/thumbs/frieslandcampina.jpg" alt="FrieslandCampina — Video production" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">FrieslandCampina</span><span class="tile-type">Video production</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/doritos/doritos.html">
      <span class="tile-media"><img src="/thumbs/doritos.jpg" alt="Doritos — Social animation" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Doritos</span><span class="tile-type">Social animation</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/quakercruesli/quakercruesli.html">
      <span class="tile-media"><img src="/thumbs/quakercruesli.jpg" alt="Quaker Cruesli — TV commercial and social animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Quaker Cruesli</span><span class="tile-type">TV commercial &amp; social</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/verkade/verkade.html">
      <span class="tile-media"><img src="/thumbs/verkade.jpg" alt="Verkade — Stop-motion" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Verkade</span><span class="tile-type">Stop-motion</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/daelmans/daelmans.html">
      <span class="tile-media"><img src="/thumbs/daelmans.jpg" alt="Daelmans — 2.5D product animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Daelmans</span><span class="tile-type">2.5D product animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/ecoline/ecoline.html">
      <span class="tile-media"><img src="/thumbs/ecoline.jpg" alt="Talens Ecoline — Promo and social content" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Talens Ecoline</span><span class="tile-type">Promo &amp; social content</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/arriva/arriva.html">
      <span class="tile-media"><img src="/thumbs/arriva_spitsmuis.jpg" alt="Arriva Spitsmuis — 2D animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Arriva Spitsmuis</span><span class="tile-type">2D animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/raakpuur/raakpuur.html">
      <span class="tile-media"><img src="/thumbs/raakpuur.jpg" alt="Raak Puur — Stop-motion" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Raak Puur</span><span class="tile-type">Stop-motion</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/jan_pannenkoek/jan_pannenkoek.html">
      <span class="tile-media"><img src="/thumbs/jan_pannenkoek.jpg" alt="JAN Pannenkoek — 2D animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">JAN Pannenkoek</span><span class="tile-type">2D animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/bb_showreel/bb_showreel.html">
      <span class="tile-media"><img src="/thumbs/bb_showreel.jpg" alt="Brand Builders — Showreel" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Brand Builders</span><span class="tile-type">Showreel</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/arrivaopstapper/arrivaopstapper.html">
      <span class="tile-media"><img src="/thumbs/arriva_opstapper.jpg" alt="Arriva Opstapper — 2D animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Arriva Opstapper</span><span class="tile-type">2D animation</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/capetracks/capetracks.html">
      <span class="tile-media"><img src="/thumbs/capetracks.jpg" alt="Capetracks — Brand animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Capetracks</span><span class="tile-type">Brand animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/vegter/vegter.html">
      <span class="tile-media"><img src="/thumbs/vegter.jpg" alt="Vegter — Campaign videos" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Vegter</span><span class="tile-type">Campaign videos</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/arrivadienstregeling/arrivadienstregeling.html">
      <span class="tile-media"><img src="/thumbs/arriva_dienstregeling.jpg" alt="Arriva Dienstregeling — 2D animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Arriva Dienstregeling</span><span class="tile-type">2D animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/summerrain/summerrain.html">
      <span class="tile-media"><img src="/thumbs/summerrain.jpg" alt="Summer Rain — Instruction videos" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Summer Rain</span><span class="tile-type">Instruction videos</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/livium/livium.html">
      <span class="tile-media"><img src="/thumbs/livium.jpg" alt="Livium — Logo animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Livium</span><span class="tile-type">Logo animation</span></span>
    </a>
    <a class="tile" data-category="video" href="/cases/arturo/arturo.html">
      <span class="tile-media"><img src="/thumbs/arturo.jpg" alt="Arturo — Campaign visuals" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Arturo</span><span class="tile-type">Campaign visuals</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/ezeetabs/ezeetabs.html">
      <span class="tile-media"><img src="/thumbs/ezeetabs.jpg" alt="Ezeetabs — Social animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Ezeetabs</span><span class="tile-type">Social animation</span></span>
    </a>
    <a class="tile" data-category="animation" href="/cases/combi_outboards/combi_outboards.html">
      <span class="tile-media"><img src="/thumbs/combi_outboards.jpg" alt="Combi Outboards — 2D animation" loading="lazy" width="800" height="800"></span>
      <span class="tile-caption"><span class="tile-client">Combi Outboards</span><span class="tile-type">2D animation</span></span>
    </a>
  </div>
</main>
</body>
</html>
```

Let op: de eerste 3 tegels hebben bewust GEEN `loading="lazy"` (boven de vouw), de rest wel.

- [x] **Step 2: Verifieer structuur**

Run:
```bash
cd /Users/michiel/Documents/michielmeilink.github.io
grep -c 'class="tile"' index.html
grep -c 'loading="lazy"' index.html
grep -o 'href="/cases/[^"]*"' index.html | sed 's/href="\(.*\)"/\1/' | while read p; do test -f ".${p}" || echo "KAPOT ${p}"; done
grep -o 'src="/thumbs/[^"]*"' index.html | sed 's/src="\(.*\)"/\1/' | while read p; do test -f ".${p}" || echo "KAPOT ${p}"; done
```
Expected: `20`, `17`, en geen KAPOT-regels.

- [x] **Step 3: Browsercheck filter**

Run: `cd /Users/michiel/Documents/michielmeilink.github.io && python3 -m http.server 8000` (achtergrond) en open `http://localhost:8000/`.
Check: zijbalk laadt; klik "Animation" → 12 tegels, hash wordt `#animation`; klik "Video" → 8 tegels; "All work" → 20; hard refresh op `http://localhost:8000/#video` toont direct alleen video-tegels. Stop de server daarna.

- [x] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: rebuild homepage as filterable work grid with captions and OG tags"
```

---

### Task 7: Case-sjabloon — referentiecase `durex`

**Files:**
- Rewrite: `cases/durex/durex.html`

**Interfaces:**
- Consumes: snippet uit Task 5, classes uit Task 4.
- Produces: het exacte sjabloon dat Task 8 op de overige 19 cases toepast.

- [x] **Step 1: Schrijf `cases/durex/durex.html` integraal**

```html
<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<title>Durex: 2D animation — Michiel Meilink</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="For Durex, Brand Builders came up with a concept in which we search for the stand of the Dutch. I animated all the videos.">
<meta property="og:title" content="Durex: 2D animation — Michiel Meilink">
<meta property="og:description" content="For Durex, Brand Builders came up with a concept in which we search for the stand of the Dutch. I animated all the videos.">
<meta property="og:image" content="https://michielmeilink.com/thumbs/durex_standjegezocht.jpg">
<meta property="og:url" content="https://michielmeilink.com/cases/durex/durex.html">
<meta property="og:type" content="article">
<link rel="icon" href="/favicon.ico">
<link rel="stylesheet" href="/css/main.css">
<script src="/js/site.js" defer></script>
</head>
<body>
<aside id="site-menu" class="sidebar"></aside>
<noscript><nav class="noscript-nav"><a href="/index.html">Work</a><a href="/about.html">About</a></nav></noscript>
<main class="content">
  <article class="case-article">
    <h1>Durex: 2D animation</h1>
    <dl class="case-meta">
      <div><dt>Client</dt><dd>Durex</dd></div>
      <div><dt>Agency</dt><dd>Brand Builders</dd></div>
      <div><dt>Role</dt><dd>Animation</dd></div>
      <div><dt>Type</dt><dd>2D animation</dd></div>
    </dl>
    <p class="case-intro">The Netherlands does not yet have a well-known stand that they are known for. For Durex, Brand Builders has come up with a concept in which we search for the stand of the Dutch. I was allowed to animate all the videos.</p>
    <div class="case">
      <div class="video-responsive-wrapper">
        <iframe src="https://www.youtube.com/embed/h-6NtHbFLJY" title="Durex — 2D animation" allowfullscreen loading="lazy"></iframe>
      </div>
    </div>
    <nav class="case-nav" aria-label="Projects">
      <a class="case-nav-prev" href="/cases/combi_outboards/combi_outboards.html"><span>Previous</span>Combi Outboards</a>
      <a class="case-nav-next" href="/cases/frieslandcampina/frieslandcampina.html"><span>Next</span>FrieslandCampina</a>
    </nav>
  </article>
</main>
</body>
</html>
```

- [x] **Step 2: Browsercheck**

Start `python3 -m http.server 8000`, open `http://localhost:8000/cases/durex/durex.html`.
Check: zijbalk laadt en "Durex" is gemarkeerd (is-active); meta-rij toont Client/Agency/Role/Type; video speelt; Previous → Combi Outboards, Next → FrieslandCampina werken. Mobiel formaat (responsive mode 390px): topbalk + hamburger werkt.

- [x] **Step 3: Commit**

```bash
git add cases/durex/durex.html
git commit -m "feat: new case template applied to durex (reference case)"
```

---

### Task 8: Sjabloon toepassen op de overige 19 cases

**Files:**
- Rewrite: de 19 overige `cases/<map>/<map>.html`

**Interfaces:**
- Consumes: het letterlijke sjabloon uit Task 7; per case de gegevens uit de tabel hieronder plus de canonieke volgorde (prev/next).

**Werkwijze per case:** neem het Task 7-sjabloon en vervang:
1. `<title>` → `<h1-tekst> — Michiel Meilink`; og:title idem zonder suffixwijziging.
2. `<h1>` → bestaande h1-tekst uit de tabel (kolom "h1 blijft") — deze blijven letterlijk zoals ze nu in de bestanden staan.
3. `meta description` en `og:description` → kolom "Description" hieronder (exacte string).
4. `og:image` → `https://michielmeilink.com/thumbs/<thumb>` (canonieke tabel); `og:url` → de eigen case-URL.
5. `case-meta` → Client/Agency/Role/Type uit de tabel; bij een "Extra"-waarde één extra `<div><dt>…</dt><dd>…</dd></div>` toevoegen; bij `combi_outboards` de Agency-regel WEGLATEN.
6. `case-intro` → de bestaande beschrijvende alinea('s) uit het huidige bestand, letterlijk overnemen (alleen witruimte normaliseren). Bij meerdere alinea's: meerdere `<p class="case-intro">`.
7. De bestaande `<div class="case">`-blokken met video-embeds → letterlijk overnemen uit het huidige bestand, inclusief hun wrapper-classes; elke `<iframe>` krijgt `title="<Grid-label> — <Type>"` en `loading="lazy"` (en behoudt `allowfullscreen`).
8. `case-nav` → prev/next volgens de canonieke volgorde (1↔20 wikkelt rond), met de Grid-labels als linktekst.

**Casegegevens (aanvulling op de canonieke tabel):**

| map | h1 blijft | Client | Agency | Role | Extra | Description (meta + og) |
|---|---|---|---|---|---|---|
| `frieslandcampina` | Friesland Campina | FrieslandCampina | Brand Builders | Edit & compositing | — | I created several videos for FrieslandCampina, both for internal use and for social media. |
| `doritos` | Doritos | Doritos | Brand Builders | Animation | — | PepsiCo launched a contest where users could send in their dip tip. I created the social media animations for the campaign. |
| `quakercruesli` | Quaker Cruesli | Quaker Cruesli | Brand Builders | Animation | — | A contest was devised for Quaker Cruesli, and I animated both the TV commercial and the social media content. |
| `verkade` | Verkade stopmotion | Verkade | Brand Builders | Stop-motion & edit | — | For Verkade, we created a stop-motion video to promote their new flavor and packaging. |
| `daelmans` | Daelmans: 2.5D product animation | Daelmans | Brand Builders | Animation | — | Daelmans, the stroopwafel producer, wanted an animation to announce their new packaging. I created the entire animation from start to finish. |
| `ecoline` | Talens - Ecoline Duotip | Talens / Ecoline | Brand Builders | Animation & compositing | Artwork: Third party | For the launch of Talens / Ecoline's new Duotip pen, I produced the promotional animations and social media content. |
| `arriva` | Arriva Spitsmuis | Arriva | Brand Builders | Animation | — | I created an animation video for a major passenger transport company to announce a new boarding point. |
| `raakpuur` | Raak: Puur | Raak | Brand Builders | Stop-motion & edit | Photography: Studio Wilkin's | Soft drink brand Raak launched three new flavors. I created the stop-motion video and edited a behind-the-scenes video. |
| `jan_pannenkoek` | JAN Pannenkoek | JAN Pannenkoek | Brand Builders | Animation | — | To bring JAN Pannenkoek into the spotlight, I created several animated videos. |
| `bb_showreel` | Showreel Brand Builders | Brand Builders | Brand Builders | Edit & motion design | Photography: Stock | I produced Brand Builders' showreel, combining video, 3D, shop floor material, and other expressions. |
| `arrivaopstapper` | Arriva Opstapper | Arriva | Brand Builders | Animation | — | An animation video announcing a new boarding point for public transport, made for Arriva. |
| `capetracks` | Capetracks | Capetracks | Brand Builders | Animation | — | Capetracks introduced a new visual identity. I created this short animation to bring their visual language to life. |
| `vegter` | Vegter's rolletjes | Vegter | Brand Builders | Video editing | — | Two extreme personalities opposite each other in conversation — I edited the campaign videos for Vegter's Rolletjes. |
| `arrivadienstregeling` | Arriva Dienstregeling | Arriva | Brand Builders | Animation | — | I created an animation video for Arriva to announce the new timetables. |
| `summerrain` | Summer Rain | Jarola | Brand Builders | Video editing | — | Summer Rain produces professional irrigation systems. I edited a series of videos explaining how to install their products. |
| `livium` | Livium | Livium | Brand Builders | Animation | — | For Livium a new visual identity was created. I made two logo animations as a proposal. |
| `arturo` | Arturo campaign visuals | Arturo flooring | Brand Builders | Motion design & edit | Photography: Stock | Arturo, a floor manufacturer, asked me to create various visuals for their social media channels. |
| `ezeetabs` | Ezeetabs | Ezeetabs | Brand Builders | Animation | — | Ezeetabs wanted to promote their product on social media, and I created the animations for the campaign. |
| `combi_outboards` | Combi Outboards | Combi Outboards | *(geen Agency-regel)* | Animation | — | Combi Outboards produces electric engines for the shipping industry. This animation was part of my graduation thesis. |

(Type per case staat in de canonieke tabel bovenaan het plan.)

- [x] **Step 1: Pas het sjabloon toe op alle 19 bestanden** (volgens de werkwijze en tabellen hierboven; embeds en beschrijvende teksten uit de huidige bestanden overnemen — eerst het huidige bestand lezen, dan herschrijven)

- [x] **Step 2: Verifieer over alle 20 cases**

Run:
```bash
cd /Users/michiel/Documents/michielmeilink.github.io
for f in cases/*/[a-z]*.html; do
  for pat in 'lang="en"' 'og:image' 'case-meta' 'case-nav' 'js/site.js' '<title>'; do
    grep -q "$pat" "$f" || echo "MIST $pat in $f"
  done
done
grep -o 'href="/cases/[^"]*"' cases/*/[a-z]*.html | sed 's/.*href="\(.*\)"/\1/' | sort -u | while read p; do test -f ".${p}" || echo "KAPOT ${p}"; done
grep -c 'youtube.com/embed' cases/*/[a-z]*.html
```
Expected: geen MIST/KAPOT-regels; het aantal embeds per case gelijk aan vóór de wijziging (totaal 39: arriva 1, arrivadienstregeling 1, arrivaopstapper 2, arturo 4, bb_showreel 1, capetracks 1, combi_outboards 1, daelmans 2, doritos 2, durex 1, ecoline 1, ezeetabs 3, frieslandcampina 3, jan_pannenkoek 1, livium 2, quakercruesli 4, raakpuur 2, summerrain 2, vegter 2, verkade 3).

- [x] **Step 3: Controleer de prev/next-ketting**

Run:
```bash
cd /Users/michiel/Documents/michielmeilink.github.io
for f in cases/*/[a-z]*.html; do echo "$f: prev=$(grep -o 'case-nav-prev" href="[^"]*' $f | cut -d'"' -f3) next=$(grep -o 'case-nav-next" href="[^"]*' $f | cut -d'"' -f3)"; done
```
Expected: elke case verwijst naar zijn buren in de canonieke volgorde; `durex` prev=combi_outboards; `combi_outboards` next=durex.

- [x] **Step 4: Steekproef in de browser**

Start server, open 3 cases (`arturo` — 4 vierkante video's, `arrivaopstapper` — portret + vierkant, `verkade` — mix) en klik de hele prev/next-ketting minimaal 5 stappen door.

- [x] **Step 5: Commit**

```bash
git add cases
git commit -m "feat: apply new case template with meta row, OG tags and prev/next to all cases"
```

---

### Task 9: About-pagina

**Files:**
- Rewrite: `about.html`

**Interfaces:**
- Consumes: snippet Task 5, classes Task 4, hero `images/IMG_6923.jpg` (gecomprimeerd in Task 2).

- [x] **Step 1: Schrijf `about.html` integraal**

```html
<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<title>About — Michiel Meilink</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Michiel Meilink is a motion designer and video editor working in advertising, with a background in computer science.">
<meta property="og:title" content="About — Michiel Meilink">
<meta property="og:description" content="Michiel Meilink is a motion designer and video editor working in advertising, with a background in computer science.">
<meta property="og:image" content="https://michielmeilink.com/images/IMG_6923.jpg">
<meta property="og:url" content="https://michielmeilink.com/about.html">
<meta property="og:type" content="profile">
<link rel="icon" href="/favicon.ico">
<link rel="stylesheet" href="/css/main.css">
<script src="/js/site.js" defer></script>
</head>
<body>
<aside id="site-menu" class="sidebar"></aside>
<noscript><nav class="noscript-nav"><a href="/index.html">Work</a><a href="/about.html">About</a></nav></noscript>
<main class="content">
  <article class="case-article">
    <h1>About me</h1>
    <img class="about-hero" src="/images/IMG_6923.jpg" alt="Michiel Meilink" width="1600" height="1067">
    <p class="case-intro">I began my journey in computer science but eventually found my way into advertising. My expertise is focused on motion graphics and videography. In my free time, I love traveling to different countries with my camera and drone, playing the guitar, engaging in sports, and enjoying outdoor activities.</p>
  </article>
</main>
</body>
</html>
```
Let op: controleer de werkelijke pixelmaten van `images/IMG_6923.jpg` na Task 2 (`sips -g pixelWidth -g pixelHeight images/IMG_6923.jpg`) en zet die in de `width`/`height`-attributen.

- [x] **Step 2: Browsercheck**

Server aan, open `http://localhost:8000/about.html`: zijbalk met "About" gemarkeerd, hero netjes afgerond, tekst leesbaar; mobiel formaat OK.

- [x] **Step 3: Commit**

```bash
git add about.html
git commit -m "feat: restyle about page in new layout with meta tags"
```

---

### Task 10: Oude CSS verwijderen, eindcontrole & livegang

**Files:**
- Delete: `css/styles.css`, `css/menu.css`

- [x] **Step 1: Controleer dat niets meer naar de oude CSS verwijst**

Run: `cd /Users/michiel/Documents/michielmeilink.github.io && grep -rn "styles.css\|menu.css" --include="*.html" .`
Expected: geen output. (Wel output → die pagina is gemist in Task 6–9; eerst fixen.)

- [x] **Step 2: Verwijder de oude bestanden**

```bash
git rm css/styles.css css/menu.css
```

- [x] **Step 3: Volledige lokale eindcontrole**

Start `python3 -m http.server 8000` en loop na:
1. Home: 20 tegels, fade-in, hover (zoom + verloop-bijschrift), filter Animation/Video, deelbare hash-URL.
2. Zijbalk: alle 20 clientlinks klikken door naar de juiste case; About werkt; social-iconen openen LinkedIn/Instagram.
3. Prev/next-ketting: volledige rondgang van 20 stappen begint en eindigt bij Durex.
4. Mobiel (responsive mode 390px): topbalk, hamburger-overlay, menu sluit na klik, grid 1 kolom.
5. `prefers-reduced-motion` emuleren (DevTools → Rendering): geen tile-animaties meer.
6. JS uit (DevTools → Settings → Disable JavaScript): noscript-navigatie zichtbaar, content full-width, geen lege zijbalkstrook.
7. `curl -s http://localhost:8000/menu.html | head -3` levert de mobile-bar HTML.

- [x] **Step 4: Commit en push naar GitHub Pages**

```bash
git commit -m "chore: remove superseded stylesheets"
git push origin main
```
(Branchnaam checken met `git branch --show-current`; als het `master` is, dat gebruiken.)

- [x] **Step 5: Livecheck**

Wacht ~2 min op de Pages-build en check:
```bash
curl -sI https://michielmeilink.com/ | head -5
curl -s https://michielmeilink.com/ | grep -c 'class="tile"'
curl -s https://michielmeilink.com/menu.html | grep -c 'menu-cat-title'
curl -sI https://michielmeilink.com/css/main.css | head -3
```
Expected: HTTP 200, `20`, `2`, HTTP 200. Daarna handmatige check van de live site op desktop + telefoon, en een WhatsApp/LinkedIn-preview-test van 1 case-URL (via https://www.opengraph.xyz of door de link in een chat te plakken).

- [x] **Step 6: Afronden**

Meld aan Michiel dat de site live staat, met de verificatie-uitkomsten. Nieuwe case toevoegen is voortaan: case-map kopiëren + thumbnail in `thumbs/` + één tegel in `index.html` + één regel in `menu.html` + prev/next van de buren bijwerken.
