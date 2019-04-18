"""
Urls for the characters app
"""
from django.urls import path

from .views import (
    CharacterListView, CharacterDetailView, CharacterCreateView,
    CharacterUpdateView, CharacterDeleteView,
)

character_patterns = [
    path('', CharacterListView.as_view(), name='list'),
    path('<int:pk>', CharacterDetailView.as_view(), name='detail'),
    path('create', CharacterCreateView.as_view(), name='create'),
    path('<int:pk>/update', CharacterUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', CharacterDeleteView.as_view(), name='delete'),
]
