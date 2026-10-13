#!/bin/sh
# Rebuild og-image.png and the icon PNGs with headless Chrome.
# Usage: sh tools/render.sh   (from the repo root; needs ImageMagick)
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd)
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
PORT=8798
python3 -m http.server $PORT --bind 127.0.0.1 --directory "$ROOT/site" >/dev/null 2>&1 &
SERVER=$!
trap 'kill $SERVER; rm -rf "$TMP" "$ROOT/site/_og.html" "$ROOT/site/_icon.html"' EXIT
sleep 1
cp "$ROOT/tools/og-card.html" "$ROOT/site/_og.html"
printf '%s' '<!DOCTYPE html><html><head><style>html,body{margin:0;background:#fff;overflow:hidden}img{display:block;width:600px;height:600px}</style></head><body><img src="/favicon.svg" alt=""></body></html>' > "$ROOT/site/_icon.html"
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --no-first-run --user-data-dir="$TMP/profile" \
  --force-device-scale-factor=1 --virtual-time-budget=3000 --window-size="$2" --screenshot="$3" "http://127.0.0.1:$PORT/$1" >/dev/null 2>&1; }
shot _og.html 1200,630 "$ROOT/site/og-image.png"
shot _icon.html 600,600 "$TMP/icon600.png"
magick "$TMP/icon600.png" -fuzz 10% -fill '#17171c' -draw 'color 0,0 floodfill' -draw 'color 599,0 floodfill' \
  -draw 'color 0,599 floodfill' -draw 'color 599,599 floodfill' -resize 180x180 -strip "$ROOT/site/apple-touch-icon.png"
magick "$TMP/icon600.png" -fuzz 2% -transparent white -resize 32x32 -strip "$ROOT/site/favicon-32.png"
echo "og-image.png, apple-touch-icon.png, favicon-32.png rebuilt"
