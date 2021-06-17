from django.urls import path
from . import views

app_name = 'basic_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('login1/', views.after_register, name='after_register'),
    path('clients/', views.clients, name='clients'),
    path('vision/', views.vision, name='vision'),
    path('principle/', views.principle, name='principle'),
    path('whatwedo/', views.whatwedo, name='whatwedo'),
    path('strength/', views.strength, name='strength'),
]