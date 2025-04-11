from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import uuid
from .models import ChatSession, ChatMessage
from api.gemini_service import GeminiService

# Initialiser le service Gemini
gemini_service = GeminiService()

def chat_home(request):
    """Vue pour la page principale du chat"""
    return render(request, 'chat/chat_home.html')

def chat_history(request):
    """Vue pour afficher l'historique des conversations"""
    # Récupérer les sessions de chat (limité aux 10 dernières)
    sessions = ChatSession.objects.all().order_by('-updated_at')[:10]
    return render(request, 'chat/chat_history.html', {'sessions': sessions})

def chat_search(request):
    """Vue pour rechercher dans l'historique des conversations"""
    query = request.GET.get('q', '')
    messages = []
    
    if query:
        # Rechercher dans les messages
        messages = ChatMessage.objects.filter(content__icontains=query).order_by('-created_at')
        
    return render(request, 'chat/chat_search.html', {
        'messages': messages, 
        'query': query
    })

@csrf_exempt
@require_http_methods(["POST"])
def process_message(request):
    """API pour traiter les messages du chat"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '')
        session_id = data.get('session_id', '')
        
        # Créer ou récupérer une session de chat
        if not session_id:
            session = ChatSession.objects.create(session_id=uuid.uuid4().hex)
        else:
            session, created = ChatSession.objects.get_or_create(session_id=session_id)
        
        # Enregistrer le message de l'utilisateur
        ChatMessage.objects.create(
            session=session,
            role='user',
            content=message
        )
        
        # Mettre à jour la date de dernière modification de la session
        session.save()  # Cela met à jour le champ updated_at
        
        # Vérifier si le message est lié à la cause palestinienne
        is_palestine_related = gemini_service.is_palestine_related(message)
        
        if is_palestine_related:
            # Générer une réponse liée à la Palestine
            response_text = gemini_service.get_palestine_response(message)
        else:
            # Réponse standard pour les requêtes hors sujet
            response_text = gemini_service.get_non_palestine_response()
        
        # Enregistrer la réponse de l'assistant
        ChatMessage.objects.create(
            session=session,
            role='assistant',
            content=response_text
        )
        
        response = {
            'status': 'success',
            'message': response_text,
            'session_id': session.session_id,
            'is_palestine_related': is_palestine_related
        }
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def delete_history(request):
    """API pour supprimer l'historique des conversations"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', '')
        
        if session_id:
            # Supprimer une session spécifique
            session = get_object_or_404(ChatSession, session_id=session_id)
            session.delete()
        else:
            # Supprimer toutes les sessions
            ChatSession.objects.all().delete()
        
        return JsonResponse({'status': 'success', 'message': 'تم حذف المحادثات بنجاح'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
