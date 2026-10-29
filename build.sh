#!/bin/sh
# Publish only website files, never the repository root or internal documents.
set -eu
rm -rf dist
mkdir -p dist
cp index.html privacy.html sitemap.xml favicon*.png favicon.ico _headers dist/
cp -R terrax gaia data-sources privacy el assets dist/
