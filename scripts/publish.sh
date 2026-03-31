#!/bin/bash
# Push updated site to GitHub Pages
cd ~/penny-stock-oracle || exit 1

git add -A
git commit -m "Update: $(date +%Y-%m-%d %H:%M)"
git push origin main
