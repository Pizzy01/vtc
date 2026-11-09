#!/bin/bash
# Mise en ligne de lux-taxi.com depuis GitHub, à lancer dans la console SSH Infomaniak.
#
#   bash ~/tmp/vtc-deploy/tools/deployer.sh <branche> --essai   # montre ce qui changerait, ne touche à rien
#   bash ~/tmp/vtc-deploy/tools/deployer.sh <branche>           # sauvegarde, puis met en ligne
#
# Prérequis (faits le 9 nov. 2026) : clé ~/.ssh/deploy_vtc + hôte « github-vtc » dans ~/.ssh/config,
# clé ajoutée en Deploy key (lecture/écriture) sur github.com/Pizzy01/vtc.
set -euo pipefail

BRANCHE="${1:?Usage : deployer.sh <branche> [--essai]}"
ESSAI="${2:-}"
SITE="$HOME/sites/lux-taxi.com"
TRAVAIL="$HOME/tmp/vtc-deploy"
DATE="$(date +%Y%m%d-%H%M%S)"

rm -rf "$TRAVAIL"
git clone -q --depth 1 -b "$BRANCHE" github-vtc:Pizzy01/vtc.git "$TRAVAIL"
cd "$TRAVAIL"
echo "Branche $BRANCHE : $(git log -1 --oneline)"

# Les redirections doivent passer le test avant toute mise en ligne
python3 tools/redirects.py test

# Fichiers jamais envoyés ou jamais effacés sur le serveur
EXCLUS=(--exclude .git --exclude tools/ --exclude '*.md' --exclude redirects.csv --exclude .gitignore
        --exclude 'api/data/*.csv' --exclude 'api/data/limite_*' --exclude 'google*.html' --exclude '*.zip')

if [ "$ESSAI" = "--essai" ]; then
  echo "ESSAI : fichiers qui seraient modifiés ou supprimés"
  rsync -a --delete --dry-run --itemize-changes "${EXCLUS[@]}" "$TRAVAIL"/ "$SITE"/
  exit 0
fi

mkdir -p "$HOME/sauvegardes"
tar czf "$HOME/sauvegardes/lux-taxi.com-$DATE.tar.gz" -C "$HOME/sites" lux-taxi.com
echo "Sauvegarde : ~/sauvegardes/lux-taxi.com-$DATE.tar.gz"

rsync -a --delete "${EXCLUS[@]}" "$TRAVAIL"/ "$SITE"/
echo "En ligne. Contrôle :"
for u in / /pages/contact.html /fr/ /service/airport-transfer-geneva/ /sitemap.xml; do
  curl -s -o /dev/null -w "%{http_code} %{redirect_url}  <- $u\n" "https://www.lux-taxi.com$u"
done
echo "Pour revenir en arrière : rm -rf $SITE && tar xzf ~/sauvegardes/lux-taxi.com-$DATE.tar.gz -C ~/sites"
