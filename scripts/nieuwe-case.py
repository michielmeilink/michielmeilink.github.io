#!/usr/bin/env python3
# Nieuwe case toevoegen aan michielmeilink.com
#
# Gebruik:  python3 scripts/nieuwe-case.py
# Beantwoord de vragen; het script maakt de casepagina aan en werkt
# index.html, menu.html en de pijltjes-navigatie van de buurcases bij.
# Zet vooraf (of daarna) de thumbnail klaar als thumbs/<slug>.jpg (800x800).

import re
import sys
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://michielmeilink.com"


def vraag(label, default=None, verplicht=True):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        v = input(f"{label}{suffix}: ").strip()
        if not v and default is not None:
            return default
        if v or not verplicht:
            return v
        print("  (verplicht veld)")


def main():
    print("=== Nieuwe case voor michielmeilink.com ===\n")

    slug = vraag("Mapnaam/slug (kleine letters, bv. 'nieuweklant')")
    if not re.fullmatch(r"[a-z0-9_]+", slug):
        sys.exit("FOUT: slug mag alleen kleine letters, cijfers en _ bevatten.")
    case_dir = ROOT / "cases" / slug
    if case_dir.exists():
        sys.exit(f"FOUT: cases/{slug}/ bestaat al.")

    client = vraag("Clientnaam zoals in grid/menu/ticker (bv. 'Nieuwe Klant')")
    h1 = vraag("Paginatitel (h1)", default=client)
    typ = vraag("Type werk (bv. '2D animation')")
    cat = vraag("Categorie: animation of video", default="animation")
    if cat not in ("animation", "video"):
        sys.exit("FOUT: categorie moet 'animation' of 'video' zijn (voor 'ai': vraag Claude, die categorie staat nog niet in het menu).")
    agency = vraag("Agency (leeg laten = geen Agency-regel)", default="Brand Builders", verplicht=False)
    role = vraag("Role (bv. 'Animation')")
    intro = vraag("Korte beschrijving (1-3 zinnen, Engels)")

    print("\nVideo's. Per video: een mp4-bestandsnaam die in de casemap staat (bv. 'nieuweklant.mp4',")
    print("aanbevolen: eigen speler zonder YouTube-branding) OF een YouTube-ID (bv. 'h-6NtHbFLJY').")
    videos = []
    while True:
        vid = vraag(f"Video {len(videos) + 1}: mp4-naam of YouTube-ID (leeg = klaar)", verplicht=False)
        if not vid:
            if videos:
                break
            print("  (minimaal 1 video nodig)")
            continue
        vorm = vraag("  Vorm: liggend / vierkant / staand", default="liggend")
        if vorm not in ("liggend", "vierkant", "staand"):
            print("  (onbekende vorm, kies liggend/vierkant/staand)")
            continue
        videos.append((vid, vorm))

    # --- Huidige volgorde en css-versie uit index.html ---
    index_path = ROOT / "index.html"
    index_html = index_path.read_text()
    orde = re.findall(r'href="/cases/([a-z0-9_]+)/', index_html)
    orde = list(dict.fromkeys(orde))
    eerste, laatste = orde[0], orde[-1]
    versie = re.search(r'main\.css\?v=(\d+)', index_html).group(1)
    js_versie = re.search(r'site\.js\?v=(\d+)', index_html).group(1)

    # --- Videoblokken: liggende los, vierkant/staand samen in een rij ---
    def player_blok(mp4, vorm):
        shape = {"liggend": "", "vierkant": " player-square", "staand": " player-portrait"}[vorm]
        return (f'    <div class="case">\n'
                f'      <div class="player is-muted{shape}">\n'
                f'        <video src="/cases/{slug}/{mp4}" autoplay muted loop playsinline preload="metadata" controls></video>\n'
                f'        <div class="player-ui">\n'
                f'          <button class="player-play" type="button" aria-label="Pause">\n'
                f'            <svg class="ic-play" viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>\n'
                f'            <svg class="ic-pause" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg>\n'
                f'          </button>\n'
                f'          <button class="player-mute" type="button" aria-label="Unmute">\n'
                f'            <svg class="ic-muted" viewBox="0 0 24 24" aria-hidden="true"><path d="M16.5 12A4.5 4.5 0 0 0 14 7.97v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51A8.8 8.8 0 0 0 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3 3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06a8.99 8.99 0 0 0 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4 9.91 6.09 12 8.18V4z"/></svg>\n'
                f'            <svg class="ic-unmuted" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3A4.5 4.5 0 0 0 14 7.97v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>\n'
                f'          </button>\n'
                f'          <div class="player-progress"><div class="player-track"><div class="player-progress-fill"></div></div></div>\n'
                f'          <button class="player-fs" type="button" aria-label="Fullscreen">\n'
                f'            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>\n'
                f'          </button>\n'
                f'        </div>\n'
                f'      </div>\n'
                f'    </div>')

    def youtube_blok(vid, vorm):
        wrapper = {"liggend": "video-responsive-wrapper",
                   "vierkant": "video-square-wrapper",
                   "staand": "video-portrait-wrapper"}[vorm]
        return (f'    <div class="case">\n'
                f'      <div class="{wrapper}">\n'
                f'        <iframe src="https://www.youtube.com/embed/{vid}?autoplay=1&mute=1&loop=1&playlist={vid}&playsinline=1&rel=0" '
                f'title="{client} — {typ}" allowfullscreen loading="lazy"></iframe>\n'
                f'      </div>\n'
                f'    </div>')

    losse, samen = [], []
    for vid, vorm in videos:
        if vid.endswith(".mp4"):
            if not (ROOT / "cases" / slug / vid).exists():
                print(f"LET OP: cases/{slug}/{vid} bestaat nog niet — zet het bestand er zelf neer voor je pusht.")
            blok = player_blok(vid, vorm)
        else:
            blok = youtube_blok(vid, vorm)
        (losse if vorm == "liggend" else samen).append(blok)
    video_html = "\n".join(losse)
    if samen:
        if len(samen) > 1:
            binnen = "\n".join("  " + b.replace("\n", "\n  ") for b in samen)
            video_html += ('\n    <div class="video-container-horizontal">\n'
                           + binnen + '\n    </div>')
        else:
            video_html += "\n" + samen[0]
    video_html = video_html.strip("\n")

    agency_regel = f'      <div><dt>Agency</dt><dd>{agency}</dd></div>\n' if agency else ""

    # --- Casepagina ---
    pagina = f'''<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
<meta charset="utf-8">
<title>{h1} — Michiel Meilink</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{intro}">
<meta property="og:title" content="{h1} — Michiel Meilink">
<meta property="og:description" content="{intro}">
<meta property="og:image" content="{SITE}/thumbs/{slug}.jpg">
<meta property="og:url" content="{SITE}/cases/{slug}/{slug}.html">
<meta property="og:type" content="article">
<link rel="icon" href="/favicon.ico">
<link rel="stylesheet" href="/css/main.css?v={versie}">
<script src="/js/site.js?v={js_versie}" defer></script>
</head>
<body>
<aside id="site-menu" class="sidebar"></aside>
<noscript><nav class="noscript-nav"><a href="/index.html">Work</a><a href="/about.html">About</a></nav></noscript>
<main class="content">
  <article class="case-article">
    <h1>{h1}</h1>
    <dl class="case-meta">
      <div><dt>Client</dt><dd>{client}</dd></div>
{agency_regel}      <div><dt>Role</dt><dd>{role}</dd></div>
      <div><dt>Type</dt><dd>{typ}</dd></div>
    </dl>
    <p class="case-intro">{intro}</p>
{video_html}
    <nav class="case-nav" aria-label="More work">
      <a class="case-nav-prev" href="/cases/{laatste}/{laatste}.html" aria-label="Previous case"></a>
      <a class="case-nav-next" href="/cases/{eerste}/{eerste}.html" aria-label="Next case"></a>
    </nav>
  </article>
</main>
</body>
</html>
'''
    case_dir.mkdir(parents=True)
    (case_dir / f"{slug}.html").write_text(pagina)

    # --- Buurcases bijwerken (nieuwe case komt achteraan) ---
    laatste_pad = ROOT / "cases" / laatste / f"{laatste}.html"
    laatste_pad.write_text(re.sub(
        r'(case-nav-next" href=")/cases/[a-z0-9_]+/[a-z0-9_]+\.html',
        rf'\g<1>/cases/{slug}/{slug}.html', laatste_pad.read_text()))
    eerste_pad = ROOT / "cases" / eerste / f"{eerste}.html"
    eerste_pad.write_text(re.sub(
        r'(case-nav-prev" href=")/cases/[a-z0-9_]+/[a-z0-9_]+\.html',
        rf'\g<1>/cases/{slug}/{slug}.html', eerste_pad.read_text()))

    # --- Tegel in index.html (achteraan het grid) ---
    tegel = (f'    <a class="tile" data-category="{cat}" href="/cases/{slug}/{slug}.html">\n'
             f'      <span class="tile-media"><img src="/thumbs/{slug}.jpg" alt="{client} — {typ}" loading="lazy" width="800" height="800"></span>\n'
             f'      <span class="tile-caption"><span class="tile-client">{client}</span><span class="tile-type">{typ}</span></span>\n'
             f'    </a>\n')
    nieuw_index, n = re.subn(r'(  </div>\n  <div class="ticker")', tegel + r'\1', index_html, count=1)
    if n != 1:
        sys.exit("FOUT: kon het einde van het grid in index.html niet vinden.")

    # --- Naam in de ticker (beide groepen) ---
    nieuw_index, n = re.subn(r'(&#183;</span>)(</div>)',
                             rf'\g<1><span>{client}</span><span class="ticker-dot">&#183;</span>\g<2>',
                             nieuw_index)
    if n != 2:
        sys.exit(f"FOUT: ticker-groepen niet gevonden (verwacht 2, gevonden {n}).")
    index_path.write_text(nieuw_index)

    # --- Menuregel in de juiste categorie ---
    menu_path = ROOT / "menu.html"
    menu = menu_path.read_text()
    li = f'        <li><a href="/cases/{slug}/{slug}.html">{client}</a></li>\n'
    kop = f'href="/#{cat}"'
    pos = menu.find(kop)
    if pos == -1:
        sys.exit(f"FOUT: categorie {cat} niet gevonden in menu.html.")
    einde_ul = menu.rfind("\n", 0, menu.find("</ul>", pos)) + 1
    menu = menu[:einde_ul] + li + menu[einde_ul:]
    menu_path.write_text(menu)

    thumb = ROOT / "thumbs" / f"{slug}.jpg"
    print(f"\nKLAAR. Aangemaakt/bijgewerkt: cases/{slug}/{slug}.html, index.html, menu.html, {laatste} en {eerste} (pijltjes).")
    if not thumb.exists():
        print(f"LET OP: thumbs/{slug}.jpg ontbreekt nog! Exporteer een vierkante jpg (800x800) naar die plek.")
    print("\nDaarna:")
    print("  1. Check lokaal:  python3 -m http.server 8000  →  http://localhost:8000/")
    print("  2. Publiceer:     git add -A && git commit -m 'feat: add case <naam>' && git push")


if __name__ == "__main__":
    main()
