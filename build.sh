#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias de Python
python -m pip install --upgrade pip
pip install setuptools wheel
pip install -r requirements.txt

# Instalar dependencias de Node
npm install

# Ejecutar el script de Python para generar el modelo
python model.py 