# Ontwerp: redesign michielmeilink.com

**Datum:** 9 juli 2026
**Status:** goedgekeurd concept, wacht op review geschreven spec

## Doel

Het portfolio van Michiel Meilink (motion designer / video editor) aantrekkelijker en
professioneler maken. Grote clientnamen (FrieslandCampina, Durex, Arriva, Doritos, …)
moeten direct zichtbaar zijn, het werk moet ingedeeld zijn in logische categorieën, en
de site moet creatief ogen zonder chaotisch te worden.

**Inspiratie:** maaikenienhuis.com (zijbalk met categorieën), g2k.nl (speels grid met
bijschriften), lovework.studio (tags/meta per project), buck.co (typografie),
robwienk.com (werk groot in beeld), ores-collective.com (editorial meta-labels).
Gekozen richting: **licht & creatief**.

## Constraints

- Puur statisch: HTML + CSS + een klein beetje vanilla JS. Geen build-stap, geen framework.
- Hosting blijft gratis via GitHub Pages met custom domein (CNAME: michielmeilink.com).
- Video's blijven op YouTube (embeds), thumbnails/afbeeldingen in de repo.
- Fonts self-hosted in de repo (geen betaalde licenties, geen trage externe calls).
- Onderhoudbaar door Michiel zelf: nieuwe case toevoegen moet simpel blijven.

## Structuur & navigatie

- **Desktop:** vaste zijbalk links met:
  1. MM-logo (link naar home)
  2. Categorieën: **Animatie**, **Video** — en **AI** zodra daar werk voor is
     (categorie met 0 projecten wordt niet getoond)
  3. Per categorie de projecten op clientnaam, altijd zichtbaar (zoals bij Maaike
     Nienhuis); de zijbalk scrollt mee als de lijst langer is dan het scherm
  4. Onderaan: About, e-mailadres, social-iconen (LinkedIn e.d.)
- Klik op categorienaam → grid filtert (URL-hash, bv. `/#animatie`, deelbaar).
- Klik op clientnaam → direct naar de case-pagina.
- **Mobiel (< ~800px):** zijbalk wordt topbalk met logo + menuknop; menu overlay met
  dezelfde inhoud. Grid 1–2 kolommen.
- De zijbalk staat in **één gedeeld bestand** (`menu.html`) dat elke pagina met een
  klein JS-fetchje inlaadt. `<noscript>`-fallback met basislinks (Work / About).

## Look & feel

- **Kleuren:** gebroken wit als achtergrond (geen hard #fff), donkergrijze tekst.
  Accent: het blauw→cyaan verloop uit het MM-logo (#0072FF → cyaan), spaarzaam gebruikt:
  actieve categorie, hover-states, kleine details.
- **Typografie:** één karaktervol display-font voor koppen + één strak leesbaar font
  voor lopende tekst. Self-hosted (woff2). Bij de bouw worden 2–3 concrete
  fontcombinaties ter keuze voorgelegd.
- **Beweging:** subtiel — zachte fade-in van grid-tegels, vloeiende hover-transities.
  `prefers-reduced-motion` wordt gerespecteerd. Geen zware scroll-libraries.

## Werk-grid (homepage)

- 3 kolommen op desktop (nu 4), 2 op tablet, 1 op mobiel.
- Onder elke tegel een bijschrift: **clientnaam + type werk** (bv. "Durex — 2D animatie").
- Hover: subtiele zoom op de thumbnail + bijschrift kleurt in het logo-verloop.
- Volgorde handmatig bepaald (beste werk bovenaan); categoriefilter eroverheen.
- Tegels krijgen `data-category`-attributen; filter is een paar regels JS (show/hide).

## Case-pagina's (compact sjabloon)

Eén vast sjabloon voor alle 20 cases:

1. Grote titel
2. Meta-labels in een nette rij: **Client / Agency / Rol / Type**
3. Korte omschrijving (bestaande teksten blijven, evt. licht geredigeerd)
4. Video('s) groot in beeld (bestaande YouTube-embeds, bestaande wrappers voor
   16:9 / vierkant / portret blijven werken)
5. Onderaan: **vorige / volgende project**-navigatie

## Concept-indeling categorieën (door Michiel te corrigeren)

| Categorie | Projecten |
|---|---|
| **Animatie** | Arriva Spitsmuis, Arriva Dienstregeling, Arriva Opstapper, Capetracks, Combi Outboards, Daelmans, Doritos, Durex, Ezeetabs, JAN Pannenkoek, Livium, Quaker Cruesli |
| **Video** | Arturo, Showreel Brand Builders, Ecoline (Talens), FrieslandCampina, Raak Puur, Summer Rain, Vegter, Verkade |
| **AI** | nog geen projecten — categorie verschijnt zodra het eerste AI-project erin staat |

Twijfelgevallen (stopmotion Raak/Verkade zit tussen animatie en video in) worden bij
review door Michiel definitief ingedeeld. Een project mag in meerdere categorieën.

## Techniek & opruimwerk (meegenomen in de bouw)

- `<meta name="description">` en Open Graph-tags (titel, omschrijving, thumbnail) op
  alle pagina's → nette previews op WhatsApp/LinkedIn.
- Thumbnails comprimeren (nu 3,1 MB totaal) en `loading="lazy"` op grid-afbeeldingen.
- Unieke `<title>` per case-pagina (ontbreekt nu op case-pagina's).
- `lang="en"` op `<html>` (huidige teksten zijn Engels; blijft Engels).
- `.DS_Store`-bestanden uit de repo, `.gitignore` dekt ze al.
- Ongebruikte bestanden opruimen (`grid.html`, lege `files/`-map) na check.
- Lokale map is gekoppeld aan de GitHub-repo; publiceren = `git push`.

## Wat bewust NIET verandert

- Hosting, domein, YouTube als videobron.
- De hoeveelheid tekst per case (compact; geen procesverhalen).
- Geen CMS, geen build-tooling, geen analytics (kan later altijd nog).

## Succescriteria

1. Bezoeker ziet binnen één scherm: wie Michiel is (logo/tagline), welke grote namen
   hij bediende (zijbalk + bijschriften), en zijn beste werk (grid).
2. Filteren op categorie werkt zonder herladen en is deelbaar via URL.
3. Site werkt goed op mobiel (menu, grid, video's).
4. Alle bestaande case-URL's blijven werken (geen gebroken links van buitenaf).
5. Homepage laadt merkbaar sneller (gecomprimeerde thumbnails + lazy loading).
6. Nieuwe case toevoegen = case-map + thumbnail + één regel in het gedeelde menu.

## Testen

- Handmatig: desktop (Chrome/Safari), mobiel formaat (responsive mode), filter,
  menu-overlay, alle case-links, prev/next-ketting, noscript-fallback.
- Check dat GitHub Pages de site correct serveert na push (CNAME intact).
