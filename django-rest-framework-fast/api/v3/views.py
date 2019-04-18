"""
Views for the Character API
"""
from characters.models import Character
from characters.serializers import CharacterSerializer
from rest_framework import viewsets


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer
