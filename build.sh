#!/bin/sh
# Publish only website files, never the repository root or internal documents.
set -eu
mkdir -p dist/assets
cp index.html privacy.html favicon*.png favicon.ico _headers dist/
cp assets/*.png assets/*.css assets/*.js dist/assets/
