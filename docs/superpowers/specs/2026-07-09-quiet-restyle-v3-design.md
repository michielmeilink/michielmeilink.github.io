# Quiet restyle v3 — michielmeilink.com (à la joannanguyen.com)

**Datum:** 9 juli 2026 · **Status:** goedgekeurd door Michiel ("ja ga bouwen") · vervangt de stijl van v2 (dark/OFF+BRAND)

## Aanleiding

v2 (bijna-zwart, grote typografie, kleine kapitalen) was het ook niet. Michiel wil de site zo dicht mogelijk bij https://www.joannanguyen.com brengen, met als enige eigen accent: zijn logo duidelijk in beeld.

## Referentie-analyse (uit HTML/CSS van joannanguyen.com)

Vast linker-zijpaneel; naam groot bovenaan; platte projectlijst als enige navigatie met klein sectielabel ("selects"); achtergrond antraciet `#272727`; witte tekst, secundair grijs; één rustig schreefloos font (Proxima Nova), klein en zonder kapitalen-opmaak; homepage = thumbnail-mozaïek zonder bijschriften; projectpagina's met minimale credits; monochroom (geen kleuraccent).

## Ontwerp

### Tokens
- `--bg: #272727`, `--ink: #fff`, `--ink-soft: #9a9a9a`, `--line: #3a3a3a`
- `--font-display` wijst ook naar Inter (Sora-bestanden blijven staan maar worden niet meer gebruikt)
- Verloop-accent (`--grad`) verdwijnt uit alle hovers/actief-states; monochroom. Kleur komt van het logo.

### Zijbalk
- Logo groot: 150px breed (was 54px) — vervangt haar grote naam; geen tagline/naamtekst
- Kopjes All work/Animation/Video: klein (13px), gewoon gewicht, geen kapitalen; actief = onderstreept
- Clientnamen: 13px grijs → wit op hover/actief
- About + socials onderaan: grijs → wit op hover (geen blauw)

### Homepage
- Bijschriften uit beeld: strak mozaïek met 6px tussenruimte, geen afgeronde hoeken
- Clientnaam verschijnt subtiel op hover als overlay onderin de tegel (donker verloopje, kleine witte tekst); markup van de captions blijft staan
- Zoom-op-hover en gefaseerde inschuif-animatie vervallen (austere)

### Case-pagina's & About
- Titel klein en rustig: 20px, gewicht 500, body-font
- Meta-labels zonder kapitalen, 12px grijs; waarden wit
- Prev/next klein (13px), hover onderstreept
- Geen afgeronde hoeken op video's/hero

### Ongewijzigd
URL's, HTML-structuur (op logo-maat na), menu-fetch, filter-JS, embeds, OG-tags, mobiele hamburger-mechaniek.

## Verificatie
Grep-checks op tokens en verdwenen gradient-hovers; lokale servercheck home/case/about; push + livecheck.
