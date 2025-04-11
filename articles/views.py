from django.shortcuts import render, get_object_or_404
from .models import Article, Category

def article_list(request):
    """Vue pour afficher la liste des articles"""
    articles = Article.objects.all()
    categories = Category.objects.all()
    return render(request, 'articles/article_list.html', {
        'articles': articles,
        'categories': categories
    })

def article_detail(request, article_id):
    """Vue pour afficher le détail d'un article"""
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'articles/article_detail.html', {'article': article})

def category_list(request):
    """Vue pour afficher la liste des catégories"""
    categories = Category.objects.all()
    return render(request, 'articles/category_list.html', {'categories': categories})

def category_detail(request, category_id):
    """Vue pour afficher les articles d'une catégorie spécifique"""
    category = get_object_or_404(Category, id=category_id)
    articles = category.articles.all()
    return render(request, 'articles/category_detail.html', {
        'category': category,
        'articles': articles
    })
