#!/bin/bash
set -eux

# Installa le dipendenze di sistema necessarie per Chromium
apt-get update
apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxi6 \
    libxtst6 \
    libxrandr2 \
    libdbus-glib-1-2 \
    libgtk-3-0 \
    libgbm1

# Installa Chromium tramite Playwright
playwright install chromium

# Installa le librerie Python
pip install -r requirements.txt
