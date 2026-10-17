#!/bin/sh
# Rebuild the social cards with headless Chrome:
#   tools/og-card.html  -> site/og-image.png         (home page)
#   tools/og-shein.html -> site/shein-data/og.png    (SHEIN data page)
# The icons (favicon-32.png, favicon-64.png, apple-touch-icon.png) are made from
# site/assets/portrait.webp on an accent background; re-make them if the photo changes.
# Usage: sh tools/render.sh   (from the repo root)
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
PORT=8798
python3 -m http.server $PORT --bind 127.0.0.1 --directory "$ROOT/site" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER; rm -rf "$TMP" "$ROOT/site/_og.html"' EXIT
sleep 1
shot() {
  cp "$ROOT/tools/$1" "$ROOT/site/_og.html"
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run --user-data-dir="$TMP/profile" \
    --force-device-scale-factor=1 --virtual-time-budget=3000 --window-size=1200,630 \
    --screenshot="$ROOT/site/$2" "http://127.0.0.1:$PORT/_og.html" >/dev/null 2>&1
  echo "$2 rebuilt"
}
shot og-card.html og-image.png
shot og-shein.html shein-data/og.png
