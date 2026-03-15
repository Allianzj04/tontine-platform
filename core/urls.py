from django.urls import path
from . import views

urlpatterns = [
    path('groups/', views.list_groups, name='list_groups'),
    path('groups/create/', views.create_group, name='create_group'),
    path('groups/<int:pk>/', views.detail_group, name='detail_group'),
    path('groups/<int:pk>/add_member/', views.add_member, name='add_member'),
    path('signup/', views.signup, name='signup'),
    path('groups/<int:pk>/create_cycle/', views.create_cycle, name='create_cycle'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
