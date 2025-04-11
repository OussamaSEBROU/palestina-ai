#!/bin/bash

# Script de déploiement pour Palestina-ai

echo "Démarrage du déploiement de Palestina-ai..."

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Collecter les fichiers statiques
echo "Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Appliquer les migrations
echo "Application des migrations..."
python manage.py migrate

# Configurer pour la production
echo "Configuration pour la production..."
export DJANGO_SETTINGS_MODULE=palestina_ai.settings_prod
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export GEMINI_API_KEY="AIzaSyChkuipfn1VLK_YifhIxm6aSxJj"

# Démarrer Gunicorn
echo "Démarrage de Gunicorn..."
gunicorn palestina_ai.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120

echo "Déploiement terminé!"
