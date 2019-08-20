from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


character_drf_patterns = [
    path('', views.CharacterListView.as_view(), name='list_create'),
    path('<int:pk>', views.CharacterDetailView.as_view(), name='get_update_delete'),
]

# append suffix specifiers for drf
character_drf_patterns = format_suffix_patterns(character_drf_patterns)

v2_patterns = [
    path('characters/', include((character_drf_patterns, 'characters')))
]
