from django.urls import path
from . import views

urlpatterns = [
    path('groupes/', views.liste, name='liste_groupes'),
    path('groupes/<int:pk>/', views.detail_groupe, name='detail_groupe'),
    path('inscription/', views.inscription, name='inscription'),
]
