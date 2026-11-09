#!/usr/bin/env python3
"""Redirections 301 de lux-taxi.com, générées depuis redirects.csv.

  python3 tools/redirects.py build   # réécrit le bloc REDIRECTIONS dans .htaccess
  python3 tools/redirects.py test    # vérifie chaque ancienne adresse (1 seul saut, page qui existe)

Le test reproduit les règles écrites dans .htaccess (mêmes expressions régulières, même ordre).
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "redirects.csv"
HTACCESS = ROOT / ".htaccess"
HOST = "www.lux-taxi.com"
BASE = f"https://{HOST}"
BEGIN = "# >>> REDIRECTIONS 301 (généré par tools/redirects.py depuis redirects.csv — ne pas modifier à la main)"
END = "# <<< FIN REDIRECTIONS 301"


def load():
    rules = []  # (kind, pattern_or_path, target, line_no)
    with CSV.open(encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            old, new = [x.strip() for x in next(csv.reader([line]))]
            if old.startswith("motif:"):
                rules.append(("motif", old[len("motif:"):], new, n))
            else:
                rules.append(("exact", old, new, n))
    return rules


def to_regex(kind, old):
    """Expression appliquée au chemin sans "/" initial, comme mod_rewrite dans un .htaccess."""
    if kind == "motif":
        return old
    p = old.strip("/")
    return "^" + re.escape(p).replace("\\-", "-") + "/?$"


def block(rules):
    out = [BEGIN, "<IfModule mod_rewrite.c>", "    RewriteEngine On"]
    for kind, old, new, _ in rules:
        rx = to_regex(kind, old)
        target = BASE + new
        if old == "/index.html":
            # Seulement si index.html est tapé dans l'adresse (évite une boucle avec DirectoryIndex)
            out.append("    RewriteCond %{THE_REQUEST} \\s/index\\.html[\\s?]")
        out.append(f"    RewriteRule {rx} {target} [R=301,L,QSD,NE]")
    out += [
        "",
        "    # Une seule version du site : https://www.lux-taxi.com (en un seul saut)",
        "    RewriteCond %{HTTPS} off [OR]",
        "    RewriteCond %{HTTP_HOST} ^lux-taxi\\.com$ [NC]",
        f"    RewriteRule ^(.*)$ {BASE}/$1 [R=301,L,NE]",
        "</IfModule>",
        END,
    ]
    return "\n".join(out)


def build():
    rules = load()
    text = HTACCESS.read_text(encoding="utf-8")
    new_block = block(rules)
    if BEGIN in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda m: new_block, text, flags=re.S)
    else:
        raise SystemExit("Marqueur REDIRECTIONS absent de .htaccess")
    HTACCESS.write_text(text, encoding="utf-8")
    print(f"{len(rules)} règles écrites dans .htaccess")


def exists(path):
    path = path.split("?")[0]
    if path == "/":
        return (ROOT / "index.html").exists()
    return (ROOT / path.lstrip("/")).is_file()


def resolve(path, host=HOST, https=True, typed_index=False):
    """Retourne (code, destination) pour une requête, selon les règles du .htaccess."""
    rel = path.split("?")[0].lstrip("/")
    for kind, old, new, _ in load():
        if old == "/index.html" and not typed_index:
            continue
        if re.search(to_regex(kind, old), rel):
            return 301, BASE + new
    if not https or host.lower() == "lux-taxi.com":
        return 301, BASE + "/" + path.lstrip("/")
    return (200, None) if exists(path) else (404, None)


def test():
    rules = load()
    errors = []
    checked = 0
    # 1. Chaque ancienne adresse exacte : 1 saut vers une page qui existe, sur www comme sans www
    for kind, old, new, n in rules:
        if not exists(new):
            errors.append(f"ligne {n} : destination {new} absente du site")
        if kind != "exact":
            continue
        variants = {old, old.rstrip("/"), old.rstrip("/") + "/", old + "?rCH=2"} - {""}
        for v in variants:
            for host in (HOST, "lux-taxi.com"):
                code, dest = resolve(v, host=host, typed_index=(old == "/index.html"))
                checked += 1
                if code != 301 or dest != BASE + new:
                    errors.append(f"{host}{v} -> {code} {dest} (attendu 301 {BASE + new})")
                    continue
                code2, _ = resolve(dest[len(BASE):])
                if code2 != 200:
                    errors.append(f"{v} : chaîne ou destination cassée ({dest} -> {code2})")
    # 2. Exemples couverts par les motifs
    samples = {
        "/ourfleet/business-electric-tesla-t/": "/pages/flotte.html",
        "/fr/ourfleet/tesla-t/": "/pages/flotte.html",
        "/service_category/lux-taxi-service/": "/pages/services.html",
        "/category/chauffeur/": "/",
        "/fr/category/voyage/": "/",
        "/blog/?start=0": "/",
        "/ru/blog?start=0": "/",
        "/it/": "/",
        "/it/blog?rCH=2": "/",
        "/fr/une-page-inconnue/": "/",
    }
    for v, new in samples.items():
        code, dest = resolve(v)
        checked += 1
        if dest != BASE + new:
            errors.append(f"motif : {v} -> {code} {dest} (attendu {BASE + new})")
    # 3. Les pages actuelles ne doivent PAS être redirigées
    for p in ["/", "/pages/services.html", "/pages/flotte.html", "/pages/destinations.html",
              "/pages/contact.html", "/404.html", "/sitemap.xml", "/robots.txt", "/api/contact.php",
              "/assets/css/vitesse-prestige.css"]:
        code, dest = resolve(p)
        checked += 1
        if code != 200:
            errors.append(f"page actuelle {p} -> {code} {dest}")
        code, dest = resolve(p, host="lux-taxi.com")
        if dest != BASE + p:
            errors.append(f"lux-taxi.com{p} -> {dest} (attendu {BASE + p})")
        code, dest = resolve(p, https=False)
        if dest != BASE + p:
            errors.append(f"http://www{p} -> {dest} (attendu {BASE + p})")
    # 4. Une adresse inconnue hors ancien WordPress reste en 404
    code, _ = resolve("/nimporte-quoi-xyz/")
    if code != 404:
        errors.append(f"/nimporte-quoi-xyz/ -> {code} (attendu 404)")
    print(f"{checked} cas vérifiés, {len(errors)} erreur(s)")
    for e in errors:
        print("  -", e)
    return 1 if errors else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "test"
    if cmd == "build":
        build()
    else:
        sys.exit(test())
