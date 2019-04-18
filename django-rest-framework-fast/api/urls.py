from django.urls import path, include

from .v1.urls import v1_patterns
from .v2.urls import v2_patterns
from .v3.urls import v3_patterns

api_patterns = [
    path('v1/', include((v1_patterns, 'v1'))),
    path('v2/', include((v2_patterns, 'v2'))),  # Uses Django REST Framework Generic Views
    path('v3/', include((v3_patterns, 'v3'))),  # Uses Django REST Framework ViewSets
]
