# idee.md - idee prodotto Microsystem (1/11/2026)

Appunti dalla ricerca del 1/11/2026: repo GitHub piu' stellate del settore (dati API GitHub) + problemi reali letti su forum e community. Da riprendere, non decisioni prese.

## Regola d'oro emersa
Le stelle GitHub dicono cosa la gente si costruisce da sola (spesso preferisce il fai-da-te, non paga). I forum dicono dove soffre: affidabilita' e configurazione, non l'hardware. Si vende meglio il prodotto GIA' TARATO E FUNZIONANTE, con un piccolo abbonamento (servizio, dashboard, voucher), non i componenti.

## Tabella 1 - Cosa funziona su GitHub e prodotti da assemblare

| Repo (settore) | Stelle / issue aperte | Segnale | Prodotto da assemblare |
|---|---|---|---|
| traccar/traccar (tracking GPS) | 8.000 / 404 | Piattaforma piu' usata, 200+ protocolli | Tracker 4G + servizio Traccar gia' pronto (abbonamento) |
| meshtastic/firmware (mesh LoRa) | 8.504 / 415 | Community enorme, ma 415 issue aperte | Nodi/ripetitori gia' configurati bene |
| tzapu/WiFiManager (captive portal ESP) | 7.295 / 674 | Provisioning WiFi dei dispositivi sentitissimo | Dispositivi che si configurano da soli da telefono |
| lmarzen/esp32-weather-epd (e-paper) | 6.332 / 43 | Stazione meteo e-paper molto replicata | Stazione e-paper gia' montata (nel catalogo) |
| OpenMQTTGateway (BLE/433/868/LoRa -> MQTT) | 4.115 / 68 | Gateway multi-protocollo molto richiesto | Gateway universale per Home Assistant, ~59-89 euro |
| ESP32-Paxcounter (conteggio persone WiFi/BLE) | 2.127 / 19 | Conta i passanti con schede da pochi euro | PeopleCount senza sensori dedicati (attenzione privacy) |
| chirpstack/chirpstack (LoRaWAN) | 1.125 / 35 | Server LoRaWAN open source di riferimento | HubBox: gateway con ChirpStack gia' pronto |
| apfree-wifidog (captive portal) | 940 / 2 (agg. 25/10) | Portale attivo e curato | Base per il portale di PayNet |
| openwisp-radius | 453 / 25 | Gestione utenti e RADIUS | Pannello pagamenti/voucher di PayNet |
| Repo "billing hotspot" a pagamento | 0-1 stelle | Nessun progetto open source consolidato | Portale + pagamenti = il vuoto da riempire |
| Sensori mmWave per ESPHome | 18-135 / 0-1 | Interesse piccolo, fai-da-te | Gia' nel catalogo, margine basso |
| OpenWrt + router 4G | 0-6 | Quasi nulla | Nessun segnale (non vuol dire poca domanda) |

## Tabella 2 - Problemi reali su forum e community

| Settore | Problema ricorrente | Cosa significa per il prodotto |
|---|---|---|
| Mesh Meshtastic | Congestione in zone dense, pochi usano client_mute (i nodi ritrasmettono troppo). Salti consigliati scesi da 7 a 3. Oltre 50-100 nodi la rete fatica | Nodi GIA' con ruoli e salti configurati bene + consulenza sul posizionamento dei ripetitori. Valutare anche MeshCore |
| Presenza mmWave in Home Assistant | Falsi positivi (ventilatori, tende, pareti), due sensori vicini si disturbano. Bluetooth instabile, con cavo UART va bene. Il sensore a volte resta bloccato "acceso" | Sensore gia' tarato, cablato via UART, mmWave + PIR insieme |
| Configurazione ESPHome | Chi parte da zero si perde tra YAML, pin e WiFi che cade dopo il flash | "Plug & play" vale piu' dell'hardware |
| WiFi per piccole attivita' | Separare ospiti e rete aziendale, evitare rallentamenti, nessuna isolamento = rischio. Un locale usa il 5G come backup con failover | PayNet deve includere isolamento ospiti, QoS e failover |
| Hotspot a pagamento | All'estero esiste gia' un box LTE con mini stampante di voucher a tempo o a traffico | Aggiungere voucher stampabili a PayNet: idea gia' validata |

## Priorita' che ne esce
1. PayNet con voucher, isolamento ospiti e failover (vuoto open source).
2. Nodi/ripetitori Meshtastic configurati + servizio di posizionamento.
3. Presenza mmWave + PIR pre-tarata.
4. Tracker 4G con Traccar ospitato (ricavo ricorrente).
5. Gateway universale OpenMQTTGateway.

## PayNet (gia' online nel negozio)
Categoria hotspot-wifi: PayNet Box 4G/5G (249 euro), PayNet Link ponte (149 euro), PayNet Event Kit (349 euro).
- Link ed Event Kit usano ancora la foto del Box: da rigenerare.
- Note legali verificate (da riconfermare con un professionista): se offrire WiFi e' attivita' secondaria (B&B, bar, negozi) non servono autorizzazione ne' identificazione; se vendere internet e' l'attivita' principale serve l'autorizzazione generale MIMIT. Meglio vendere box + portale ai gestori dei locali e non fare gli operatori. Da controllare: SIM che vietano la rivendita, conservazione dei log, privacy.

## Altre idee dalla sessione (LoRaWAN / HaLow)
ColdLog HACCP (sensore temperatura frigo/celle per bar e ristoranti), VendLink (telemetria macchinette, cabinati, juke-box), MeshBridge (gateway Meshtastic -> Telegram/MQTT), HubBox (gateway LoRaWAN pronto), PeopleCount, LivelloAcqua, Pager LoRa, ESL-Lite (etichette prezzo e-paper), HaLow Bridge e HaLow Hub. Le due HaLow sono in fondo per rischio normativo UE (duty cycle) ed ecosistema ancora acerbo.

## Limiti della ricerca
Campione dei forum piccolo (Lemmy, Home Assistant community, qualche snapshot Reddit), segnale qualitativo. Non ancora cercato su macchinette/HACCP, e-paper e tracker. Giro successivo: stessa tabella su quei tre, con date di aggiornamento delle repo.
