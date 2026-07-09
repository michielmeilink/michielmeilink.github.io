# Onderhoud michielmeilink.com

## Nieuwe case toevoegen (makkelijkste manier)

1. Exporteer een **vierkante thumbnail** (800×800, jpg, < 150 kB) en zet die in `thumbs/` — bestandsnaam = de slug die je in stap 2 kiest (bv. `thumbs/nieuweklant.jpg`).
2. Open Terminal in deze map en run:

   ```
   python3 scripts/nieuwe-case.py
   ```

   Beantwoord de vragen (slug, clientnaam, type, categorie, beschrijving, YouTube-ID's + vorm per video). Het script maakt de casepagina aan en werkt automatisch bij: het grid op de homepage, het menu, de namen-ticker en de pijltjes-navigatie van de buurcases.

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

- **YouTube-ID** = het stukje na `watch?v=` in de video-URL (bv. `h-6NtHbFLJY`).
- **Case verwijderen**: map onder `cases/` weghalen, de tegel uit `index.html`, de regel uit `menu.html`, de naam uit de ticker (2×) en de pijltjes van de twee buurcases naar elkaar laten wijzen. (Of vraag Claude.)
- **Stijl wijzigen**: alle opmaak staat in `css/main.css`. Verhoog na élke CSS-wijziging het versienummer `?v=NN` in alle HTML-bestanden (staat in elke `<link rel="stylesheet">`), anders zien terugkerende bezoekers 10 minuten de oude stijl. Dit gaat in één keer met:

  ```
  grep -rl 'main.css?v=44' --include='*.html' . | xargs sed -i '' 's|main.css?v=44|main.css?v=45|'
  ```

  (pas de nummers aan naar het huidige en het volgende nummer)
- **Categorie AI**: zit al in de filter-code (`js/site.js`) maar staat bewust nog niet in het menu; toevoegen zodra er een eerste AI-project is.
