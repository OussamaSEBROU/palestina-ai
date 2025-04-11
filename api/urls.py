from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('chat/', views.chat_api, name='chat_api'),
    path('generate-image/', views.generate_image, name='generate_image'),
    path('articles/', views.article_list_api, name='article_list_api'),
    path('articles/<int:article_id>/', views.article_detail_api, name='article_detail_api'),
    path('palestine-economic-data/', views.get_palestine_economic_data, name='palestine_economic_data'),
]
