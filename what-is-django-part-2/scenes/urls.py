from django.urls import path

from .views import SceneView


scene_patterns = [
    path('scene', SceneView.as_view()),
]
