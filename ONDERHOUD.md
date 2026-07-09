# Onderhoud michielmeilink.com

## Nieuwe case toevoegen (makkelijkste manier)

1. Exporteer een **vierkante thumbnail** (800×800, jpg, < 150 kB) en zet die in `thumbs/` — bestandsnaam = de slug die je in stap 2 kiest (bv. `thumbs/nieuweklant.jpg`). Exporteer ook per video een **mp4** (1080p of 720p, H.264, mik op 10–25 MB) — die zet je na stap 2 in de nieuwe casemap.
2. Open Terminal in deze map en run:

   ```
   python3 scripts/nieuwe-case.py
   ```

   Beantwoord de vragen (slug, clientnaam, type, categorie, beschrijving, video's + vorm per video). Per video geef je een **mp4-bestandsnaam** op (bv. `nieuweklant.mp4` — krijgt de eigen schone speler; zet het bestand daarna in de casemap) of een **YouTube-ID** (fallback met YouTube-embed). Het script maakt de casepagina aan en werkt automatisch bij: het grid op de homepage, het menu, de namen-ticker en de pijltjes-navigatie van de buurcases.

3. Controleer lokaal:

   ```
   python3 -m http.server 8000
   ```

   → open http://localhost:8000/ en klik de nieuwe case aan. Stop de server met Ctrl+C.

4. Zet live:

   ```
   git add -A
   git commit -m "feat: add case <naam>"
   git push
   ```

   Na ± 1 minuut staat het op michielmeilink.com.

## Handig om te weten

- **Alle video's zijn self-hosted**: de mp4's staan gewoon in de casemappen en worden door GitHub Pages geserveerd. De speler (play/geluid/voortgang/fullscreen, in huisstijl) zit in `css/main.css` + `js/site.js`; de markup kun je uit elke casepagina kopiëren. Vormen: standaard = liggend, `player-square` = vierkant, `player-portrait` = staand.
- **YouTube-ID** = het stukje na `watch?v=` in de video-URL (bv. `h-6NtHbFLJY`) — alleen nog nodig als fallback voor een case zonder mp4.
- **Case verwijderen**: map onder `cases/` weghalen, de tegel uit `index.html`, de regel uit `menu.html`, de naam uit de ticker (2×) en de pijltjes van de twee buurcases naar elkaar laten wijzen. (Of vraag Claude.)
- **Stijl wijzigen**: alle opmaak staat in `css/main.css`. Verhoog na élke CSS-wijziging het versienummer `?v=NN` in alle HTML-bestanden (staat in elke `<link rel="stylesheet">`), anders zien terugkerende bezoekers 10 minuten de oude stijl. Dit gaat in één keer met:

  ```
  grep -rl 'main.css?v=44' --include='*.html' . | xargs sed -i '' 's|main.css?v=44|main.css?v=45|'
  ```

  (pas de nummers aan naar het huidige en het volgende nummer)
- **Categorie AI**: zit al in de filter-code (`js/site.js`) maar staat bewust nog niet in het menu; toevoegen zodra er een eerste AI-project is.
