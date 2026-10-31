# Aggiunge categorie e prodotti (IT+EN) da un file JSON. Non cancella nulla: aggiorna se l'id esiste.
# Uso: python automation/aggiungi_prodotti.py elenco.json [--foto] [--push]
# elenco.json: {"categorie":[{id,nome,nome_en,icona,descrizione,descrizione_en,slug_en,foto}],
#               "prodotti":[{id,nome,nome_en,categoria,prezzo(euro),descrizione,descrizione_en,
#                            completa,completa_en,slug_en,foto}]}   (foto = soggetto per img.py)
import json, os, sys, subprocess
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = r"C:\Users\mirco\Desktop\gemini_auto\img.py"
cat_path = os.path.join(R, "_data", "catalogo.json")
elenco = json.load(open(sys.argv[1], encoding="utf-8"))
d = json.load(open(cat_path, encoding="utf-8"))
d.setdefault("categorie", []); d.setdefault("prodotti", [])

def w(rel, txt):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8", newline="\n").write(txt)

def upsert(lst, item):
    for i, x in enumerate(lst):
        if x["id"] == item["id"]: lst[i] = item; return
    lst.append(item)

def foto(soggetto, nome, profilo, out, extra=None):
    if "--foto" not in sys.argv: return
    subprocess.run(["python", IMG, soggetto, "--profilo", profilo, "--nome", nome, "--out", os.path.join(R, out),
                    "--extra", extra or "No text, no logos, no brand names anywhere on the device."], check=True)

for c in elenco.get("categorie", []):
    i = c["id"]
    upsert(d["categorie"], {"nome": c["nome"], "id": i, "icona": c.get("icona", "\U0001F4E6"),
        "descrizione": c["descrizione"], "immagine": f"assets/images/categorie/{i}.webp",
        "tr": {"en": {"nome": c["nome_en"], "descrizione": c["descrizione_en"]}}})
    foto(c.get("foto", c["nome_en"]), i, "categoria", "assets/images/categorie")
    se = c["slug_en"]
    w(f"_negozio/categoria-{i}.md", f'---\nlayout: negozio-categoria\ntitle: "{c["nome"]}"\ncid: {i}\npermalink: /negozio/categoria/{i}/\ndescription: "{c["descrizione"]}"\nref: shop-cat-{i}\n---\n')
    w(f"en/negozio/categoria/{i}.md", f'---\nlayout: negozio-categoria\ntitle: "{c["nome_en"]}"\ncid: {i}\npermalink: /en/shop/category/{se}/\ndescription: "{c["descrizione_en"]}"\nlang: en\nlocale: en\nref: shop-cat-{i}\n---\n')

for p in elenco.get("prodotti", []):
    i = p["id"]; ic = p.get("icona", "\U0001F4E6")
    upsert(d["prodotti"], {"tipo": "fisico", "id": i, "nome": p["nome"], "categoria": p["categoria"],
        "prezzo_centesimi": int(round(p["prezzo"] * 100)), "descrizione": p["descrizione"],
        "descrizione_completa": p["completa"], "immagine": f"assets/images/prodotti/{i}.webp",
        "icona": ic, "visibile": True,
        "tr": {"en": {"nome": p["nome_en"], "descrizione": p["descrizione_en"], "descrizione_completa": p["completa_en"]}}})
    foto(p.get("foto", p["nome_en"]), i, "prodotto", "assets/images/prodotti", p.get("extra"))
    se = p["slug_en"]
    w(f"_negozio/{i}.md", f'---\nlayout: negozio-prodotto\ntitle: "{p["nome"]}"\npid: {i}\npermalink: /negozio/{i}/\ndescription: "{p["descrizione"][:150]}"\nref: shop-prod-{i}\n---\n')
    w(f"en/negozio/{i}.md", f'---\nlayout: negozio-prodotto\ntitle: "{p["nome_en"]}"\npid: {i}\npermalink: /en/shop/{se}/\ndescription: "{p["descrizione_en"][:150]}"\nlang: en\nlocale: en\nref: shop-prod-{i}\n---\n')

# MAI ensure_ascii=True (punto 23 ERRORI_NOTI): le escape rompono la build Jekyll
txt = json.dumps(d, ensure_ascii=False, indent=2)
assert "\\ud8" not in txt.lower(), "escape unicode nel catalogo"
open(cat_path, "w", encoding="utf-8", newline="\n").write(txt)
json.load(open(cat_path, encoding="utf-8"))
subprocess.run(["python", os.path.join(R, "automation", "allinea_hash.py"), "en"], cwd=R)
if "--push" in sys.argv:
    subprocess.run("git add -A && git commit -m \"Aggiunti categorie/prodotti\" && git push", shell=True, cwd=R, check=True)
    print("Push fatto: aspetta 'built' con gh api repos/cialdecompatibili-netizen/microsystem/pages/builds/latest")
print("OK")
