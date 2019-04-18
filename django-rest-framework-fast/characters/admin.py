from django.contrib import admin

from characters.models import Character, Team, Line, LineModifier

admin.site.register(Character)
admin.site.register(Team)
admin.site.register(Line)
admin.site.register(LineModifier)
