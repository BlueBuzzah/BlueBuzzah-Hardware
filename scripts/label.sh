#!/bin/sh
# usage: label.sh <bounds.json> <base.png> <labels.json> <out.png>
# Builds the labeled image with headless Chrome: pass 1 measures the canvas the labels need, pass 2 screenshots it
# at 2x with a transparent background.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
WORK=${WORK:-$(mktemp -d)}
CH=${CHROME:-"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"}
python3 "$HERE/labels.py" "$WORK" "$2" "$HERE/fonts" "$1" "$3"
SIZE=$("$CH" --headless=new --disable-gpu --allow-file-access-from-files --window-size=1200,1800 --virtual-time-budget=3000 \
  --dump-dom "file://$WORK/labels.html" 2>/dev/null | sed -n 's:.*<title>\([0-9x]*\)</title>.*:\1:p')
"$CH" --headless=new --disable-gpu --hide-scrollbars --allow-file-access-from-files --force-device-scale-factor=2 \
  --window-size=$(echo "$SIZE" | tr x ,) --virtual-time-budget=3000 --default-background-color=00000000 \
  --screenshot="$4" "file://$WORK/labels.html" >/dev/null 2>&1
