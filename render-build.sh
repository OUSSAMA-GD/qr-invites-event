#!/usr/bin/env bash

# Mise à jour de pip
pip install --upgrade pip

# Installation des outils nécessaires pour les builds
pip install wheel setuptools

# Installation des dépendances du projet
pip install -r requirements.txt