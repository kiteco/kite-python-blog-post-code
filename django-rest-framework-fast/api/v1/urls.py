from django.urls import path, include

from api.v1 import views


character_api_patterns = [
    path('', views.CharacterListAPIView.as_view(), name='list'),
    path('<int:pk>', views.CharacterDetailAPIView.as_view(), name='detail'),
    path('create', views.CharacterCreateAPIView.as_view(), name='create'),
    path('<int:pk>/update', views.CharacterUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete', views.CharacterDeleteAPIView.as_view(), name='delete'),
]

v1_patterns = [
    path('characters/', include((character_api_patterns, 'characters')))
]
