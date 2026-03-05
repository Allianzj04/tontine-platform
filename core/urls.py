from django.urls import path
from . import views

urlpatterns = [
    path('groupes/', views.liste, name='liste_groupes'),
]
