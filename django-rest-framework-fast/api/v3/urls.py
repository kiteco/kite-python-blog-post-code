from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'characters', views.CharacterViewSet)

v3_patterns = [
    path('', include(router.urls)),
]
