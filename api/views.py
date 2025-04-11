from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from articles.models import Article
import os
import sys
sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

# Initialiser le service Gemini
from .gemini_service import GeminiService
gemini_service = GeminiService()

# Initialiser le client API pour les données économiques
data_client = ApiClient()

@csrf_exempt
@require_http_methods(["POST"])
def chat_api(request):
    """API pour le chat avec Gemini"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        session_id = data.get('session_id', '')
        
        # Vérifier si le message est lié à la cause palestinienne
        is_palestine_related = gemini_service.is_palestine_related(message)
        
        if is_palestine_related:
            # Générer une réponse liée à la Palestine
            response_text = gemini_service.get_palestine_response(message)
        else:
            # Réponse standard pour les requêtes hors sujet
            response_text = gemini_service.get_non_palestine_response()
        
        response = {
            'status': 'success',
            'message': response_text,
            'is_palestine_related': is_palestine_related
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def generate_image(request):
    """API pour générer des images avec Gemini"""
    try:
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        
        # Vérifier si le prompt est lié à la cause palestinienne
        is_palestine_related = gemini_service.is_palestine_related(prompt)
        
        if not is_palestine_related:
            return JsonResponse({
                'status': 'error',
                'message': 'Le prompt doit être lié à la cause palestinienne.'
            }, status=400)
        
        # Générer l'image (simulation pour le moment)
        # Dans une version réelle, cela utiliserait gemini_service.generate_image(prompt)
        
        response = {
            'status': 'success',
            'image_url': '/static/img/placeholder.jpg',
            'message': 'Image générée avec succès (simulation)'
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def article_list_api(request):
    """API pour récupérer la liste des articles"""
    try:
        articles = Article.objects.all()
        data = [{
            'id': article.id,
            'title': article.title,
            'summary': article.summary,
            'category': article.category.name,
            'created_at': article.created_at.strftime('%Y-%m-%d')
        } for article in articles]
        return JsonResponse({'articles': data})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def article_detail_api(request, article_id):
    """API pour récupérer le détail d'un article"""
    try:
        article = Article.objects.get(id=article_id)
        data = {
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'summary': article.summary,
            'category': article.category.name,
            'created_at': article.created_at.strftime('%Y-%m-%d'),
            'updated_at': article.updated_at.strftime('%Y-%m-%d')
        }
        return JsonResponse(data)
    except Article.DoesNotExist:
        return JsonResponse({'error': 'Article non trouvé'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def get_palestine_economic_data(request):
    """API pour récupérer des données économiques sur la Palestine"""
    try:
        # Récupérer les données du PIB pour la Palestine (PSE est le code ISO pour la Palestine)
        gdp_data = data_client.call_api('DataBank/indicator_data', query={
            'indicator': 'NY.GDP.MKTP.CD',
            'country': 'PSE'
        })
        
        # Récupérer les données de population pour la Palestine
        population_data = data_client.call_api('DataBank/indicator_data', query={
            'indicator': 'SP.POP.TOTL',
            'country': 'PSE'
        })
        
        # Récupérer les données de chômage pour la Palestine
        unemployment_data = data_client.call_api('DataBank/indicator_data', query={
            'indicator': 'SL.UEM.TOTL.ZS',
            'country': 'PSE'
        })
        
        return JsonResponse({
            'status': 'success',
            'gdp': gdp_data,
            'population': population_data,
            'unemployment': unemployment_data
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
