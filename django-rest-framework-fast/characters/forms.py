"""
Forms for Character model
"""
from django import forms

from characters.models import Character


class CharacterCreateView(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'description', 'profession', 'mentor', 'team', 'type',)


class CharacterUpdateView(forms.ModelForm):
    class Meta:
        model = Character
        fields = ('name', 'description', 'profession', 'mentor', 'team', 'type',)
