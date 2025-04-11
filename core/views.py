from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import GeneratedImage

def home(request):
    """Vue pour la page d'accueil"""
    return render(request, 'core/home.html')

def about(request):
    """Vue pour la page à propos de la cause palestinienne"""
    return render(request, 'core/about.html')

def support(request):
    """Vue pour la page des moyens de soutien"""
    return render(request, 'core/support.html')
