import os
import google.generativeai as genai
from django.conf import settings

class GeminiService:
    """
    Service pour interagir avec l'API Gemini de Google
    """
    
    def __init__(self):
        # Initialiser l'API avec la clé
        api_key = settings.GEMINI_API_KEY
        if not api_key:
            # Utiliser une clé de test pour le développement
            api_key = "DUMMY_API_KEY_FOR_DEVELOPMENT"
        
        genai.configure(api_key=api_key)
        self.text_model = settings.GEMINI_TEXT_MODEL
        self.image_model = settings.GEMINI_IMAGE_MODEL
    
    def is_palestine_related(self, text):
        """
        Vérifie si le texte est lié à la cause palestinienne
        
        Args:
            text (str): Le texte à vérifier
            
        Returns:
            bool: True si le texte est lié à la Palestine, False sinon
        """
        try:
            model = genai.GenerativeModel(self.text_model)
            prompt = f"""
            Détermine si le texte suivant est lié à la cause palestinienne ou à la Palestine.
            Réponds uniquement par 'oui' ou 'non'.
            
            Texte: {text}
            """
            response = model.generate_content(prompt)
            result = response.text.strip().lower()
            return 'oui' in result or 'نعم' in result or 'yes' in result
        except Exception as e:
            print(f"Erreur lors de la vérification du texte: {e}")
            # En cas d'erreur, on suppose que c'est lié pour éviter de bloquer l'utilisateur
            return True
    
    def generate_text(self, prompt):
        """
        Génère du texte à partir d'un prompt
        
        Args:
            prompt (str): Le prompt pour générer du texte
            
        Returns:
            str: Le texte généré
        """
        try:
            model = genai.GenerativeModel(self.text_model)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erreur lors de la génération de texte: {e}")
            return "Désolé, je n'ai pas pu générer de réponse. Veuillez réessayer."
    
    def generate_image(self, prompt):
        """
        Génère une image à partir d'un prompt
        
        Args:
            prompt (str): Le prompt pour générer l'image
            
        Returns:
            bytes: Les données de l'image générée
        """
        try:
            model = genai.GenerativeModel(self.image_model)
            response = model.generate_content(prompt)
            return response.image
        except Exception as e:
            print(f"Erreur lors de la génération d'image: {e}")
            return None
    
    def get_palestine_response(self, query):
        """
        Génère une réponse liée à la Palestine
        
        Args:
            query (str): La requête de l'utilisateur
            
        Returns:
            str: La réponse générée
        """
        try:
            model = genai.GenerativeModel(self.text_model)
            prompt = f"""
            Tu es un assistant spécialisé dans la cause palestinienne. 
            Réponds à la question suivante avec des informations précises et factuelles sur la Palestine.
            Assure-toi que ta réponse est informative, respectueuse et soutient la cause palestinienne.
            
            Question: {query}
            """
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erreur lors de la génération de la réponse: {e}")
            return "Désolé, je n'ai pas pu générer de réponse. Veuillez réessayer."
    
    def get_non_palestine_response(self):
        """
        Génère une réponse pour les requêtes non liées à la Palestine
        
        Returns:
            str: La réponse standard pour les requêtes hors sujet
        """
        return """
        عذراً، هذا المشروع مخصص فقط لدعم القضية الفلسطينية وتقديم معلومات حولها.
        
        يرجى طرح أسئلة متعلقة بفلسطين، تاريخها، ثقافتها، أو طرق دعم القضية الفلسطينية.
        
        شكراً لتفهمك.
        """
