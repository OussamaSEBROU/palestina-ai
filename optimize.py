"""
Script pour optimiser les performances de l'application Palestina-ai
"""

import os
import sys
import django

# Configurer l'environnement Django
sys.path.append('/home/ubuntu/palestina-ai')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'palestina_ai.settings')
django.setup()

from django.conf import settings
from django.core.cache import cache
from django.db import connection
from django.db.models import Count, Q
from articles.models import Article, Category
from chat.models import ChatSession, ChatMessage
from core.models import GeneratedImage

def optimize_database_queries():
    """Optimiser les requêtes de base de données"""
    print("Optimisation des requêtes de base de données...")
    
    # Vérifier les requêtes les plus courantes et ajouter des index si nécessaire
    try:
        with connection.cursor() as cursor:
            # Vérifier si les tables existent avant d'ajouter des index
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_chatsession';")
            if cursor.fetchone():
                # Ajouter un index sur le champ session_id de ChatSession
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS chat_session_session_id_idx 
                ON chat_chatsession (session_id);
                """)
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='chat_chatmessage';")
            if cursor.fetchone():
                # Ajouter un index sur le champ content de ChatMessage pour la recherche
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS chat_message_content_idx 
                ON chat_chatmessage (content);
                """)
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles_category';")
            if cursor.fetchone():
                # Ajouter un index sur le champ slug de Category
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS category_slug_idx 
                ON articles_category (slug);
                """)
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articles_article';")
            if cursor.fetchone():
                # Ajouter un index sur le champ slug de Article
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS article_slug_idx 
                ON articles_article (slug);
                """)
    except Exception as e:
        print(f"Erreur lors de l'optimisation des requêtes: {e}")
    
    print("Indexes ajoutés avec succès.")

def optimize_static_files():
    """Optimiser les fichiers statiques"""
    print("Optimisation des fichiers statiques...")
    
    # Vérifier que les fichiers statiques sont correctement collectés
    static_root = settings.STATIC_ROOT
    if not os.path.exists(static_root):
        os.makedirs(static_root)
    
    # Vérifier que le répertoire media existe
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        os.makedirs(media_root)
    
    print(f"Répertoires statiques vérifiés: {static_root} et {media_root}")

def optimize_security():
    """Optimiser la sécurité de l'application"""
    print("Optimisation de la sécurité...")
    
    # Vérifier les paramètres de sécurité dans settings.py
    security_settings = {
        'DEBUG': settings.DEBUG,
        'SECRET_KEY': settings.SECRET_KEY,
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
        'CSRF_COOKIE_SECURE': getattr(settings, 'CSRF_COOKIE_SECURE', False),
        'SESSION_COOKIE_SECURE': getattr(settings, 'SESSION_COOKIE_SECURE', False),
        'SECURE_BROWSER_XSS_FILTER': getattr(settings, 'SECURE_BROWSER_XSS_FILTER', False),
        'SECURE_CONTENT_TYPE_NOSNIFF': getattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF', False),
    }
    
    print("Paramètres de sécurité actuels:")
    for key, value in security_settings.items():
        print(f"  {key}: {value}")
    
    print("\nRecommandations de sécurité pour la production:")
    print("  - Définir DEBUG = False")
    print("  - Utiliser une SECRET_KEY forte et unique")
    print("  - Limiter ALLOWED_HOSTS aux domaines spécifiques")
    print("  - Activer CSRF_COOKIE_SECURE et SESSION_COOKIE_SECURE")
    print("  - Activer SECURE_BROWSER_XSS_FILTER et SECURE_CONTENT_TYPE_NOSNIFF")

def run_optimizations():
    """Exécuter toutes les optimisations"""
    print("Démarrage des optimisations pour Palestina-ai...")
    
    optimize_database_queries()
    print("-" * 50)
    
    optimize_static_files()
    print("-" * 50)
    
    optimize_security()
    print("-" * 50)
    
    print("Optimisations terminées avec succès!")

if __name__ == "__main__":
    run_optimizations()
