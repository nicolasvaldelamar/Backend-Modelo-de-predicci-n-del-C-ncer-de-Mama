#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias de Python
python -m pip install --upgrade pip
pip install -r requirements.txt

# Instalar dependencias de Node
npm install