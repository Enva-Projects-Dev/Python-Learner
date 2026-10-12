#!/bin/bash
# doppelklick-wrapper: startet einfach build_mac_app.sh in diesem ordner
cd "$(dirname "$0")" || exit 1
bash build_mac_app.sh
echo ""
read -r -p "Press Enter to close"
