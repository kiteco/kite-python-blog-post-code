from django.core import serializers
from django.http import JsonResponse
from django.views.generic import UpdateView, CreateView, DetailView, ListView
from django.views.generic.detail import BaseDetailView

from characters.models import Character
from common.mixins import JsonResponseMixin


class CharacterListAPIView(JsonResponseMixin, ListView):
    model = Character

    def get_response(self):
        return serializers.serialize('json', self.object_list)

    def get_response_kwargs(self):
        return {'safe': False}


class CharacterDetailAPIView(JsonResponseMixin, DetailView):
    model = Character

    def get_response(self):
        return serializers.serialize('json', [self.object])

    def get_response_kwargs(self):
        return {'safe': False}


class CharacterCreateAPIView(CreateView):
    model = Character
    fields = ('name', 'description', 'profession', 'mentor', 'team', 'type',)

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse(serializers.serialize('json', [self.object]), safe=False)


class CharacterUpdateAPIView(UpdateView):
    model = Character
    fields = ('name', 'description', 'profession', 'mentor', 'team', 'type',)

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse(serializers.serialize('json', [self.object]), safe=False)


class CharacterDeleteAPIView(BaseDetailView):
    model = Character

    def post(self):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})
