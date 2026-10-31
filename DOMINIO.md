# DOMINIO.md - collegare microsystem.ipermark.com (RIMANDATO, 31/10/2026)

STATO: NON collegato. Il sito sta solo su https://cialdecompatibili-netizen.github.io/microsystem/ . Nessun file `CNAME` nella repo, Pages senza dominio personalizzato. Prima si sviluppa il sito, il dominio dopo.

## Cosa e' andato storto (31/10/2026)
- Ho messo il file `CNAME` + dominio in Pages PRIMA di avere il record DNS. Su `ipermark.com` c'e' un wildcard Cloudflare (qualsiasi `xxx.ipermark.com` risponde 200 con altro contenuto), quindi il dominio mostrava la pagina sbagliata e il sito risultava rotto (CSS non trovati: i percorsi del sito partono da `/microsystem/`, sul dominio la radice e' `/`).
- Fatto il rollback: CNAME tolto (commit 8d0e79b), Pages senza dominio. Il link github.io torna a funzionare.

## Come si fa, nell'ordine giusto (NON invertire)
1. Cloudflare > DNS di `ipermark.com` > nuovo record: tipo CNAME, nome `microsystem`, destinazione `cialdecompatibili-netizen.github.io`, nuvola GRIGIA (DNS only, niente proxy). Il record specifico vince sul wildcard.
2. Aspettare che risolva: `Resolve-DnsName microsystem.ipermark.com -Type CNAME` deve dare `cialdecompatibili-netizen.github.io`.
3. Solo dopo, nella repo: file `CNAME` con una riga `microsystem.ipermark.com` (senza a capo extra) e push; poi
   `gh api -X PUT repos/cialdecompatibili-netizen/microsystem/pages -f cname=microsystem.ipermark.com`
4. Aspettare la build (`gh api repos/cialdecompatibili-netizen/microsystem/pages/builds/latest`, status `built`) e il certificato; poi Settings > Pages > "Enforce HTTPS".
5. Verifica: aprire `https://microsystem.ipermark.com/` e controllare che CSS e immagini carichino (`/assets/css/main.css` deve dare 200, non 404). Se i percorsi hanno ancora `/microsystem/` serve un ultimo push per far ricostruire il sito con baseurl vuoto.
6. Se qualcosa non va: rollback = cancellare `CNAME`, `gh api -X DELETE repos/cialdecompatibili-netizen/microsystem/pages`, poi ricreare Pages (`-X POST ... -f "source[branch]=main" -f "source[path]=/"`).

Regola per i prossimi cloni: prima il DNS, poi il CNAME. Mai il contrario.
