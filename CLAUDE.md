# mistraltemplate1 - guida per Claude (template Jekyll adattivo)

Template Jekyll per GitHub Pages: si clona, si cambia quasi solo `_config.yml` e il sito si adatta (lingua, URL, brand, menu, shop). Obiettivo e stato del lavoro: `PROGETTO_TEMPLATE.md`.

**CREARE UN SITO DA QUESTO TEMPLATE: leggi PRIMA `docs/CLONAZIONE.md` (un comando `nuovo_sito.ps1` + `personalizza_clone.py` fanno colori, logo, sfondo home; un solo commit). Ogni automazione che impari va scritta come script in `automation/` e annotata li' (regola nella sezione 5): obiettivo meno tempo e meno commit per ogni nuovo sito.**

## Prima di toccare un clone (checklist)
1. `_config.yml`: `brand`, `description`, `default_lang`, `languages`, `whatsapp`, `contact_endpoint`, `ecommerce`. NON scrivere `url:`/`baseurl:` (li imposta GitHub Pages).
2. Menu: `_data/navigation.yml` (voci) + `_data/sottomenu.yml` (tendine, chiave = title identico). Url interni SENZA nome repo.
3. Home a blocchi: `_data/blocks_home.json` (campi id, nome, enabled, html). Modificare solo `html`, mai la struttura. Backup prima, rileggere il JSON dopo.
4. Colori/tema: `_data/tema.json`; kit blocchi in `assets/css/gaming.css` (nome storico, non rinominare; accento = `--gc-acc`).
5. Shop: `ecommerce: true` accende tutto. Dati in `_data/catalogo.json` (prezzi in centesimi) + una pagina per prodotto/categoria in `_negozio/` (esempi inclusi: `prodotto-esempio.md`, `categoria-esempio.md`).
6. Contenuti: `_pages/`, `_posts/`. Ogni pagina/articolo ha `ref:` (chiave di collegamento tra lingue).

## Regole d'oro
- ZERO valori fissi: niente nome repo, utente, dominio, telefono scritti nei layout/include/JS. Si usa `relative_url`, `site.*`, `_includes/site-name.html`.
- Admin (`admin/index.html`): `detectRepo()` ricava utente/repo dall'URL. Su dominio personalizzato chiede il repo una volta (localStorage `cms_repo`). Non hardcodarlo.
- `automation/publish.py`: percorso e URL ricavati da soli (cartella del file + remote git).
- Valore vuoto in config = funzione spenta, mai errore: i layout controllano che il campo sia pieno.
- Nessun plugin fuori da GitHub Pages. Build locale non disponibile su questo PC: si controlla online dopo il deploy.
- COMMENTARE i punti critici (layout, include, JS, CSS, config): dire cosa fa, cosa legge, cosa NON toccare.
- HERO HOME ADATTIVO (OBBLIGATORIO, NON MODIFICARE): `.ent-hero` e `.gc-hero` in `assets/css/gaming.css` si adattano allo schermo come ora e restano cosi' in ogni clone e in ogni nuovo template. Comportamento: `min-height:calc(100svh - 80px)` (fallback `100vh`) + `display:flex;align-items:center` = riempie la prima schermata sotto l'header e centra il contenuto; padding `clamp(1.5rem,4vh,3.5rem)`; titolo `.ent-hero .gc-h1{font-size:clamp(2rem,3.2vw + 1.2vh,3.6rem)}` (scala con larghezza E altezza); sfondo `cover`; sotto 900px colonne in pila e velo verticale. Nei cloni si cambiano SOLO foto e colori, mai queste regole: niente altezze fisse in px, niente rimozione di `clamp`/`svh`/`flex`.

## Multilingua (dettagli in `docs/MULTILINGUA.md`)
IT alla radice, altre lingue in `/xx/` create da admin > Lingue. Cambiare solo `default_lang` e `languages`. Traduzioni: `tr: copia|tradotto|da_aggiornare`, `tr_hash`; `automation/traduzioni_sync.py` + workflow marcano `da_aggiornare`. In Liquid niente `a contains b == false`: usare `{% if a contains b %}{% continue %}{% endif %}`.
**Lingue = cartelle (rilevamento automatico).** Clonare/rinominare una cartella `xx/` basta: `_includes/lingue-attive.html` la mette nel selettore (bandiera), `admin/js/lingue.js` (`lgDetect` + `lgNormalizza`, una volta per sessione aprendo admin > Lingue) la registra in `_config.yml` (languages + defaults), `_data/languages.yml`, `ui-text.yml` e corregge `lang`/`locale`/`permalink` dei file e gli url in `_data/i18n/xx/`; `traduzioni_sync.py` la vede da solo. La cartella e' la fonte di verita': il campo `lang:` dei file dopo un clone e' vecchio.
**Admin con lingua di lavoro** (`admin/js/lingua-admin.js`): selettore lingua nella barra in alto; Articoli, Pagine, Home e Menu usano gli STESSI editor ma leggono/scrivono `xx/_posts`, `xx/*.md`, `_data/i18n/xx/*`. Intercetta `window.fetch` e rimappa i path solo se lingua != base e sezione attiva in Articoli/Pagine/Menu; se il file lingua manca parte dalla copia della base (menu con url `/xx/`). Al salvataggio sistema il front matter (lang, locale, permalink, ref, `tr: tradotto` + `tr_hash`). NON riscrivere i path dentro index.html: aggiungere nuovi file da mappare in `mappa()`. `admin/js/core.js` e `articoli.js` NON sono caricati da index.html (legacy): la logica vera e' nello script inline di index.html.

## Eta' e date
MAI a mano: `<span data-eta="AAAA-MM-GG">N</span> anni`, `<span data-anni-da="AAAA">N</span> anni` (script in `_includes/footer/custom.html`).

## Design
MAI bordi laterali colorati su box, citazioni, avvisi, CTA. Box puliti con sfondo leggero o bordo uniforme.

## Pubblicare e lavorare
- Pubblicare con `..\pubblica.ps1` con `-Files` espliciti. Dopo il push NON aspettare la build: Mirco verifica da solo.
- Sessione interrotta: prima `read_file` e `git status --short`; spesso manca solo commit e push.
- PowerShell lungo: salvare in .ps1 e lanciare con `-NoProfile -ExecutionPolicy Bypass -File`. Mai chiamare funzioni RD/WR/CD/LS (alias: RD cancella!).
- Traduzioni: NIENTE GitHub Actions. L'hook `.githooks/pre-commit` lancia `automation/traduzioni_sync.py` a ogni commit (attivo con `git config core.hooksPath .githooks`, una volta per clone).
- Risposte brevissime, modifiche in una sola chiamata.

## Cose che funzionano
- Test senza build locale: simulare la logica JS dell'admin con node + `vm` (stub di `lgText`/`lgCommit` e albero finto) e lanciare `node --check` sul file. Esempio: `claudetemp\test_lingue.js` (clone en -> de rinominato).
- Rilevare le lingue dalle CARTELLE (non dal config) e normalizzare tutto il resto da li': evita config e cartelle fuori sync.
- Liquid senza plugin: costruire un array con `split` + `concat` + `uniq` dentro un include che fa solo `assign` (le variabili restano visibili a chi lo include).- Patch su file grandi con CRLF (admin/index.html): script node con `readFileSync`/`replace`/`writeFileSync` su stringhe esatte, mai edit multiriga a mano; poi `node --check` sui .js. Mock del wrapper fetch: `claudetemp\test_lingua_admin.js`.

SEO e lingue (24/10/2026)
- SEO per lingua: _includes/seo.html fa un solo meta robots (noindex se noindex:true o tr: copia), description per lingua da _data/languages.yml (chiave description; se manca NON la scrive), og:locale. hreflang in _includes/head/custom.html: solo versioni tradotte (stesso ref), x-default = lingua base. sitemap.xml propria (sostituisce jekyll-sitemap) con alternates hreflang, esclude noindex/copia/admin/404.
- Slug tradotti: lo slug e' il permalink del front matter; MAI scrivere a mano lo slug di un'altra lingua nei link: usare {% include url-ref.html ref="shop-negozio" %} (URL per ref nella lingua della pagina). Inglese: /en/shop/, /en/about-us/, /en/contact/, /en/category/, /en/shop/example-product/. carrello/ordine/grazie restano con slug italiano (noindex, e carrello.js controlla /grazie/). Una lingua clonata da admin parte con gli slug della base: tradurli cambiando permalink (e i link in menu/home).
- Lingua browser: script in head/custom.html. Solo prima visita, solo da pagine in lingua base, solo se esiste la versione tradotta; localStorage lang_pref = scelta ricordata (il click su bandiera/selettore la aggiorna); niente redirect per bot, ?nolang=1 o referrer dello stesso sito.


Elementi per pagina (24/10/2026)
- UN solo valore per tutte le liste: `per_page` in _config.yml (default 20), si cambia da admin > Impostazioni (10, 20, 50, 100, 200, 500). L'admin lo copia in localStorage 'cms_per_page' (getPerPage in admin/index.html); NON reintrodurre limiti separati per elenco.
- Admin: elenchi Articoli, Pagine e Prodotti usano getPerPage(); le miniature/metadati si leggono a gruppi di 6 (metaQueue in wp-elenchi.js) per non finire il limite API con 200-500 voci.
- Sito: assets/js/paginazione.js impagina blog, negozio e pagina categoria (it e en) con gli attributi data-pg, data-pg-item, data-per sul contenitore; le voci restano tutte nell'HTML. Filtri che usano hidden (pillole negozio) chiamano PgLista.refresh. Se aggiungi un nuovo elenco lungo: stessi tre attributi, niente codice nuovo.


Lezioni dal clone "cybersecurity" (24/10/2026)
- Home, Chi siamo e Servizi sono a blocchi con testi SEGNAPOSTO neutri (IT in `_data/`, EN in `_data/i18n/en/`). Stile `ent-*` in `assets/css/gaming.css`; i colori seguono `_data/tema.json` (accent = `--gc-acc`, accent_dark = `--gc-ink`): NON mettere `<style>` con colori nei blocchi.
- I JSON dei blocchi si generano con uno script node (JSON.stringify + rilettura con JSON.parse), mai a mano; apostrofi e accenti nei blocchi come entita' HTML (&#39; &egrave;).
- Dopo aver scritto/tradotto a mano le pagine di una lingua: `python automation/allinea_hash.py en` (imposta `tr: tradotto` e `tr_hash`). Senza, l'hook le marca `da_aggiornare`.
- Ogni pagina/articolo ha `ref:` anche in italiano (serve al collegamento tra lingue e al selettore).
- Dati, cifre e fonti nei testi: solo verificati sul web (cerca prima). Mai loghi clienti, recensioni, certificazioni o prezzi inventati.
- Il modulo contatti resta spento finche' `contact_endpoint` e' vuoto: chiederlo subito al cliente. Lo stesso per `whatsapp` ed `email`.
- Clone: `..\nuovo_sito.ps1` tiene `en/` di default (it,en). Con `-Lingue it` la cartella `en/` viene tolta: farlo solo se richiesto. `-Accento "#rrggbb"` imposta il colore.
- Pubblicare piu' file: `& ..\pubblica.ps1 -Repo x -Msg "..." -Files 'a','b'` (ora accetta anche `-Files a,b` da `-File`).


Lezioni dalla migrazione "pelletteria" -> "pelletteria2" (24/10/2026)
- Migrare un sito esistente in un clone: 1) mappare le due repo (menu, `_data/catalogo.json`, `_negozio/`, `blocks_home.json`, `_posts/`); 2) generare TUTTO con script node (accenti come `\uXXXX`, nei blocchi HTML entita' numeriche con una funzione `ent()`; JSON con `JSON.stringify` e rilettura); 3) `python automation/allinea_hash.py en`; 4) pubblicare con `..\pubblica.ps1 -Files ...`. Script di esempio: `claudetemp\build_pelletteria2\` (`dati.js` = categorie IT/EN, `build.js` = dati/menu, `build2.js` = blocchi/pagine/patch).
- Categorie a DUE LIVELLI: campo `genitore` in `catalogo.json` (il reparto non ha genitore; la sua pagina mostra le sottocategorie e i prodotti di tutte). Nome inglese in `tr.en.nome`. Ogni categoria ha DUE file con `ref: shop-cat-<id>`: `_negozio/categoria-<id>.md` (permalink `/negozio/categoria/<id>/`) e `en/negozio/categoria/<id>.md` (permalink `/en/shop/category/<slug-inglese>/`).
- Link dello shop: MAI `nz_lh | append: 'negozio/'` (in inglese puntava a `/en/negozio/`, che non esiste). Usare `{% include shop-url.html k="shop" %}`, `k="cat" id=...`, `k="prod" id=...`: cerca il `ref` (`shop-negozio`, `shop-cat-<id>`, `shop-prod-<id>`) nella lingua della pagina, poi nella base, poi la vecchia formula. Prodotti/categorie creati da admin senza `ref` in inglese ricadono sulla formula: aggiungere il `ref` a mano ai file.
- Il clone con `nuovo_sito.ps1 -File` storpia le virgole (`default_lang: it,en`) e CANCELLA `en/` e `_data/i18n/en`: dopo il clone controllare `default_lang` e che `en/` esista, altrimenti ripristinare dal template.
- Non portare nei blocchi i `<style>` del vecchio sito: si usano le classi `gc-*`/`ent-*` e `_data/tema.json` (copiare il tema.json del vecchio sito per mantenere i colori).
- Togliere i segnaposto che non servono (`_pages/servizi.md`, articolo di esempio, categoria/prodotto di esempio): restano online e indicizzati.
- Il modulo contatti resta spento senza `contact_endpoint` (il vecchio sito usava il worker del modello: non riusarlo, serve il worker del cliente).
- Questo template ha molti file non committati: le modifiche shop (shop-url.html, negozio-categoria, patch ai link) sono nel working tree ma NON committate; non usare `pubblica.ps1 -Tutto` qui.

## Lezioni dal clone pelletteria2 (24/10/2026)
- FOOTER: _includes/footer/custom.html mette di default © anno nome-sito - Design, Development & Digital Marketing by webtomars.it; site.footer_text nel _config.yml lo sovrascrive. Nei cloni non serve rifarlo.
- TEMA/COLORI: mai hex hardcoded (niente azzurri/teal/ghiaccio in menu.css, gaming.css, head/custom.html, layout): usare _data/tema.json (accent, accent_dark). Dopo il clone: cercare con grep i vecchi colori e sostituirli con la palette del nuovo sito.
- HOME: sfondo hero = assets/images/*-hero.jpg referenziato in gaming.css (.ent-hero). Nei cloni sostituirlo con una texture a tema (esempio: automation/genera_texture.py di pelletteria2, Pillow+numpy) e cambiare logo con automation/genera_logo.py.
- ORDINE CLONE: 1) tema.json 2) logo+texture 3) menu/categorie IT+EN 4) home/chi siamo 5) footer e segnaposto 6) commit+push+verifica online.

## Articoli e categorie del blog (logica da cybersecurity)
- Indirizzi: articolo = /blog/<categoria>/<titolo>/ (EN: /en/blog/...), categoria = /blog/<categoria>/, categoria `blog` = /blog/<titolo>/.
- Dopo ogni nuovo articolo o nuova categoria lancia `python automation/permalink_articoli.py --apply`: scrive il permalink nel front matter, crea i redirect dai vecchi indirizzi e le pagine categoria mancanti (_pages/cat-*.md, en/category-*.md). Idempotente.
- Nomi EN delle categorie: _data/i18n/en/categorie.json (stesso ordine di _data/categorie.json).
- Liste: _includes/lista-categoria.html (blog e categorie), link categoria: _includes/page__taxonomy.html, barra laterale: post-sidebar.html.
- Gli articoli `2026-10-26-*-prova` / `*-test` sono di prova: cancellali (e i loro redirect/ e le categorie Guide/Novità se non servono).

- 31/10/2026 ERRORE CATALOGO: scrivere `_data/*.json` con `ensure_ascii=False` (emoji letterali). Con le escape `\\ud83d...` la build Jekyll si rompe. Vedi docs/ERRORI_NOTI.md punto 23.
- 31/10/2026 DOMINIO: prima DNS, poi CNAME. Vedi docs/ERRORI_NOTI.md punto 24 e DOMINIO.md.


## Flusso che FUNZIONA: categoria + prodotto con foto, IT+EN (31/10/2026, provato su microsystem)
Tutto da Desktop Commander sul PC di Mirco, con Python. Il connettore GitHub non serve (non compare); git e `gh` si lanciano da terminale.
1. Ricerca di mercato sul web PRIMA (cosa si vende davvero), poi scelta di UNA categoria e UN prodotto per la demo.
2. Foto prodotto: `python C:\Users\mirco\Desktop\gemini_auto\img.py "<soggetto>" --profilo prodotto --nome <id> --out assets\images\prodotti --extra "No text, no logos, no brand names anywhere on the device."` (per elettronica NON usare `foto_sito.py`: il suo prompt e' per bottiglie). Foto categoria: stesso comando con `--profilo categoria --out assets\images\categorie`. Guardare SEMPRE la foto (read_file di Desktop Commander) prima di pubblicare.
3. Script Python che scrive `_data/catalogo.json` (categoria + prodotto con `tr.en`, prezzi in centesimi, `immagine: assets/images/prodotti/<id>.webp`) e le 4 pagine: `_negozio/categoria-<id>.md`, `en/negozio/categoria/<id>.md`, `_negozio/<id>.md`, `en/negozio/<id>.md` (ref `shop-cat-<id>` / `shop-prod-<id>`, permalink EN `/en/shop/...`). Esempio completo: `automation/esempio_demo_shop.py`. JSON SEMPRE con `ensure_ascii=False` (vedi docs/ERRORI_NOTI.md punto 23).
4. `python automation/allinea_hash.py en`, poi `git add -A`, commit, push.
5. Aspettare la build: `gh api repos/<utente>/<repo>/pages/builds/latest` deve dare `built` sul commit giusto. Se `errored`/falliti: `gh run list --limit 3` e `gh run view <id> --log-failed`.
6. Verificare online con Invoke-WebRequest: shop, categoria, prodotto IT e EN, le due immagini (200 e contenuto giusto), poi dare i link a Mirco. Dire che la resa grafica non e' stata vista.
- Prezzi e specifiche della demo sono SEGNAPOSTO da confermare con Mirco: nei testi solo cose generiche, niente portate o numeri inventati.
- Per molti prodotti: lo script e' da generalizzare in `aggiungi_prodotti.py` (input = elenco con nome, categoria, prezzo, testi IT/EN, soggetto foto), proposto a Mirco, non ancora fatto.
- Idee categorie dal mercato (ricerca 31/10/2026): nodi e schede Meshtastic (Heltec V3/V4, LILYGO T-Beam), ripetitori solari, kit modulari RAK WisBlock, tracker GPS, comunicatori portatili, kit con Raspberry Pi.

- 31/10/2026 FOTO PRODOTTI: prodotti commerciali col marchio MICROSYSTEM (wordmark pulito sul case, grigio scuro opaco + accento blu #0b6cf0, sfondo bianco). Mai marche altrui, etichette con seriali/IMEI/frequenze (le foto di Gemini le inventano): usare --extra come in automation/aggiungi_prodotti.py e GUARDARE sempre la foto. Elenco prodotti: python automation/aggiungi_prodotti.py elenco.json --foto --push.


## Listino prodotti inseriti il 3/11/2026 (11 prodotti, SENZA foto, prezzi = stime da correggere)
Inseriti con `aggiungi_prodotti.py` da `cercareprodotti\progetti\microsystem\elenco4.json` (generato da `gen_elenco4.py` nella stessa cartella). Senza foto `immagine` e' vuota nel catalogo: la scheda mostra l'icona (vedi `_layouts/negozio-prodotto.html`). Quando si fanno le foto: rilanciare con `--foto` solo per questi id e rimettere `immagine: assets/images/prodotti/<id>.webp`. URL = https://cialdecompatibili-netizen.github.io/microsystem/negozio/<id>/

| Id | Prodotto | Categoria | Prezzo |
|---|---|---|---|
| homevault | HomeVault: server privato per foto e file (Immich + Nextcloud, SSD 2 TB) | privacy-rete | 449 euro |
| kit-allarme-ha | Kit sistema di avviso per casa con Home Assistant (NON antifurto certificato) | smart-home | 349 euro |
| hubbox-lorawan | HubBox: gateway LoRaWAN con ChirpStack (EU868) | mesh-lora | 299 euro |
| box-home-assistant | Box Home Assistant pronto all'uso | smart-home | 249 euro |
| remotekvm | RemoteKVM: controllo remoto server/PC (nome nostro, non PiKVM) | privacy-rete | 199 euro |
| irrigazione-smart-solare | Controller irrigazione 4 zone a batteria con pannello solare | smart-home | 169 euro |
| kit-emergenza-lora | Kit emergenza comunicazione LoRa con power bank solare (non sostituisce il 112) | mesh-lora | 139 euro |
| irrigazione-smart | Controller irrigazione 8 zone con sensore pioggia | smart-home | 129 euro |
| assistente-vocale-locale | Assistente vocale locale per Home Assistant | smart-home | 89 euro |
| misuratore-consumi | Misuratore consumi a pinza per Home Assistant (montaggio nel quadro da persona esperta) | zigbee-sensori | 79 euro |
| kit-luci-wled | Kit luci LED con controller WLED | smart-home | 69 euro |

Totale shop dopo l'inserimento: 67 prodotti.

## PROSSIMA SESSIONE: 30 prodotti da sviluppare (solo nome custom + repo da cui prendere le info)
Ricerca del 3/11/2026, repo verificate esistenti col connettore GitHub. Ordine = stima di profitto per vendita. Per ogni prodotto, nella prossima sessione: leggere il README della repo, scrivere testi IT+EN (senza numeri inventati), prezzo, categoria, poi `gen_elenco5.py` + `aggiungi_prodotti.py`. Regola: versione a corrente e solare/batteria dove ha senso.

| # | Nome custom | Prodotto | Repo da cui prendere le info |
|---|---|---|---|
| 1 | GuardWall | Firewall per piccoli uffici su mini PC con OPNsense | https://github.com/opnsense/core |
| 2 | ReefControl | Controller acquario marino con Raspberry | https://github.com/reef-pi/reef-pi |
| 3 | StorageBox | NAS casalingo a 2 dischi | https://github.com/openmediavault/openmediavault |
| 4 | PriceTag | Etichette prezzi elettroniche e-paper per negozi | https://github.com/OpenEPaperLink/OpenEPaperLink |
| 5 | ScreenPoint | Digital signage per negozi e studi | https://github.com/Screenly/Anthias |
| 6 | SolarLink | Gateway inverter fotovoltaico verso Home Assistant (Modbus) | https://github.com/wills106/homeassistant-solax-modbus |
| 7 | HeatLink | Termostato OpenTherm per caldaia | https://github.com/ihormelnyk/opentherm_library |
| 8 | DualLink 4G | Router doppia SIM con failover | https://github.com/openwrt/packages (pacchetto mwan3) |
| 9 | CineBox | Mediacenter pronto | https://github.com/jellyfin/jellyfin |
| 10 | HiFiStream | Streamer audio Hi-Fi con Raspberry | https://github.com/moode-player/moode |
| 11 | MeterEye | Lettore contatore acqua/gas/luce con camera ESP32 | https://github.com/jomjol/AI-on-the-edge-device |
| 12 | OpenCam | Telecamera IP con firmware aperto | https://github.com/OpenIPC/firmware |
| 13 | NetScope | Sonda di rete per vedere il traffico | https://github.com/ntop/ntopng |
| 14 | PowerGuard | Mini UPS per router e NAS con spegnimento automatico | https://github.com/networkupstools/nut |
| 15 | RoomSync | Kit audio multiroom sincronizzato | https://github.com/snapcast/snapcast |
| 16 | ShipTrack | Ricevitore AIS per barche e porti | https://github.com/jvde-github/AIS-catcher |
| 17 | SkyWatch | Kit ricezione satelliti meteo | https://github.com/SatDump/SatDump |
| 18 | ThreadHub | Border router Thread/Matter | https://github.com/openthread/ot-br-posix |
| 19 | PrintBox | Box con camera per stampanti 3D | https://github.com/OctoPrint/OctoPrint |
| 20 | PingBox | Box monitoraggio uptime siti e server | https://github.com/louislam/uptime-kuma |
| 21 | WeatherPro | Stazione meteo completa con anemometro (diversa dalla e-paper) | https://github.com/weewx/weewx |
| 22 | AccessTag | Controllo accessi con tessere RFID | https://github.com/esphome/esphome |
| 23 | FloodStop | Kit antiallagamento con sensori perdite ed elettrovalvola | https://github.com/esphome/esphome |
| 24 | SwitchBox | Modulo relè WiFi da incasso (installazione da elettricista) | https://github.com/arendst/Tasmota |
| 25 | ZWaveStick | Chiavetta Z-Wave pronta per Home Assistant | https://github.com/zwave-js/zwave-js-ui |
| 26 | KnowledgeBox | Wikipedia e biblioteca offline con hotspot WiFi | https://github.com/kiwix/kiwix-tools |
| 27 | PixelClock | Orologio smart a matrice LED | https://github.com/Blueforcer/awtrix-ng |
| 28 | MacroPad | Macropad meccanico programmabile (da saldare) | https://github.com/qmk/qmk_firmware |
| 29 | RoomTrack | Nodi di presenza per stanza via Bluetooth | https://github.com/ESPresense/ESPresense |
| 30 | AirOutdoor | Centralina polveri sottili da esterno | https://github.com/opendata-stuttgart/sensors-software |

Note ricerca: AWTRIX 3 (Blueforcer/awtrix3) e' DISMESSO, usare awtrix-ng. Scartate perche' non trovate sul connettore: MMDVMHost (radioamatori), OpenWebRX, esp-rfid, its-a-plane-python. Le stelle non si leggono dal connettore: da controllare sul sito quando serve. HeatLink: ultima modifica della libreria nel 2024, verificare che sia ancora valida. Attenzione legale: relè da incasso, termostato caldaia, gateway inverter e misure in quadro toccano impianti a 230 V o gas: sempre "montaggio da persona esperta" nei testi.
