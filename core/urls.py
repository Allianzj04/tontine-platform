from django.urls import path
from . import views

urlpatterns = [
    path('groupes/', views.liste, name='liste_groupes'),
    path('groupes/creer/', views.creer_groupe, name='creer_groupe'),
    path('groupes/<int:pk>/', views.detail_groupe, name='detail_groupe'),
    path('groupes/<int:pk>/ajouter_membre/', views.ajouter_membre, name='ajouter_membre'),
    path('inscription/', views.inscription, name='inscription'),
    path('groupes/<int:pk>/creer_cycle/', views.creer_cycle, name='creer_cycle'),
]
