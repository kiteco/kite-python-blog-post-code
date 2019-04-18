from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView, ListView

from characters.models import Character


class CharacterListView(ListView):
    model = Character


class CharacterDetailView(DetailView):
    model = Character


class CharacterCreateView(CreateView):
    model = Character
    fields = ('name', 'description', 'profession', 'mentor', 'team', 'type',)


class CharacterUpdateView(UpdateView):
    model = Character
    fields = ('name', 'description', 'profession', 'mentor', 'team', 'type',)


class CharacterDeleteView(DeleteView):
    model = Character
    success_url = reverse_lazy('character:list')
