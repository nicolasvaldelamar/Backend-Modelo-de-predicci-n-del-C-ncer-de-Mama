#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias de Python
pip install -r requirements.txt

# Instalar dependencias de Node
npm install

# Ejecutar el script de Python para generar el modelo
python model.py 