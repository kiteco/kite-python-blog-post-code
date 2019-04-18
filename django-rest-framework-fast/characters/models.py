"""
Character models
"""

import random

from django.db import models
from django.urls import reverse_lazy

from .constants import CHARACTER_TYPES, EXTRA


class Character(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    profession = models.CharField(max_length=50)  # Choices later
    mentor = models.ForeignKey('Character', models.DO_NOTHING, related_name='proteges', null=True, blank=True)
    team = models.ForeignKey('Team', models.DO_NOTHING, null=True, blank=True)
    type = models.CharField(max_length=20, choices=CHARACTER_TYPES, default=EXTRA)

    def __str__(self):
        return '{name} ({team_name})'.format(name=self.name, team_name=self.team.name)

    @staticmethod
    def get_random_line():
        try:
            return random.choice(Line.objects.all())
        except IndexError:
            return 'Say what..?'

    def get_random_line_modifier(self):
        try:
            return random.choice(self.line_modifiers.all())
        except IndexError:
            return ''

    def get_line(self):
        return '{} {}'.format(self.get_random_line(), self.get_random_line_modifier())

    def get_absolute_url(self):
        return reverse_lazy('characters:detail', kwargs={'pk': self.pk})


class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class LineModifier(models.Model):
    character = models.ForeignKey('Character', models.DO_NOTHING, related_name='line_modifiers')
    modifier = models.CharField(max_length=50)

    def __str__(self):
        return self.modifier


class Line(models.Model):

    line_text = models.TextField()

    def __str__(self):
        return self.line_text
