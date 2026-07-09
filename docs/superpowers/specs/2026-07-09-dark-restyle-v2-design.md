# Dark restyle v2 — michielmeilink.com

**Datum:** 9 juli 2026 · **Status:** goedgekeurd door Michiel ("klopt ga bouwen")

## Aanleiding

Michiel is na de livegang van het redesign nog niet tevreden over de stijl. Referenties: https://www.itsoffbrand.com/our-work (donker, grote vette typografie, minimale bijschriften) en https://www.joannanguyen.com (kaal, werk voorop). Gewenst: een combinatie van beide.

## Besluiten (bevraagd en gekozen)

1. **Donker** — bijna-zwarte achtergrond zoals OFF+BRAND.
2. **Titels weg** — homepage-kop ("Michiel Meilink" + tagline-zin) én zijbalk-tagline vervallen; homepage opent direct met het grid.
3. **Zijbalk blijft zoals hij is** (structuur): logo, All work, Animation/Video + clientnamen, About, socials — alleen donker gerestyled.
4. **3 kolommen blijven** in het grid.
5. **Blauw→cyaan verloop blijft** als accent (actieve categorie, hovers).
6. **Aanpak:** donker + scherpere typografie (niet alleen kleuren omzetten).

## Ontwerp

### Kleurtokens (`css/main.css`)
- `--bg: #0e0f12` (bijna-zwart, iets warm)
- `--ink: #f2f1ed` (gebroken wit)
- `--ink-soft: #8a8d94` (secundair grijs)
- `--line: #26282e` (lijnen, tegel-placeholder)
- `--grad` ongewijzigd: `linear-gradient(100deg, #0072ff, #00c8ff)`

### Homepage
- `page-intro`-blok verwijderd uit `index.html` (en bijbehorende CSS).
- Bijschriften in kleine kapitalen met letterafstand: clientnaam links (wit), type rechts (grijs). Hover: zoom blijft, clientnaam krijgt het verloop.

### Zijbalk (`menu.html` + CSS)
- `menu-tagline` verwijderd (HTML + CSS).
- Categorietitels iets prominenter; clientnamen grijs → wit op hover en actief (hover-verloop op clientnamen vervalt; verloop blijft op categorietitels/All work actief).
- Mobiele topbalk + hamburger-overlay donker (hamburgerstreepjes worden licht via `var(--ink)`).

### Case-pagina's & About
- Casetitel groter/vetter: `clamp(32px, 5vw, 56px)`.
- Meta-rij en prev/next: labels kleine kapitalen grijs, waarden wit (structuur ongewijzigd).
- About: zelfde behandeling; hero blijft.

### Logo
`images/logo5.png` is blauw→cyaan lijnwerk op transparant — werkt op donker, geen nieuwe variant nodig.

### Ongewijzigd
HTML-structuur en URL's, menu-fetch-mechaniek, filter-JS, fonts (Space Grotesk + Inter), video-embeds, OG-tags.

## Verificatie
Grep-checks (geen page-intro/menu-tagline meer; tokens aanwezig), lokale server-check van home/case/about, daarna push en livecheck zoals bij v1.
