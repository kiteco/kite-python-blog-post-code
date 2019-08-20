"""
Serializers for Character model
"""

from rest_framework import serializers

from characters.models import Character


class CharacterSerializer(serializers.ModelSerializer):
    mentor = serializers.StringRelatedField()
    team = serializers.StringRelatedField()
    random_line = serializers.SerializerMethodField()

    @staticmethod
    def get_random_line(obj):
        return obj.get_line()

    class Meta:
        model = Character
        fields = (
            'name', 'description', 'profession', 'mentor', 'team', 'type', 'random_line',
        )
