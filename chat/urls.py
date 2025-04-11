from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('history/', views.chat_history, name='chat_history'),
    path('search/', views.chat_search, name='chat_search'),
    path('process/', views.process_message, name='process_message'),
    path('delete-history/', views.delete_history, name='delete_history'),
]
