#!/usr/bin/env bash
set -euo pipefail

rm -rf build/latex
make latexpdf
mkdir -p source/_static/pdfs
cp build/latex/*.pdf source/_static/pdfs/

echo "PDF copied to source/_static/pdfs/."
