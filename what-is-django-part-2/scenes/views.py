from django.views.generic import TemplateView

from .constants import SCENES


class SceneView(TemplateView):
    template_name = 'scenes/scene.html'

    def get_context_data(self, **kwargs):
        context = super(SceneView, self).get_context_data(**kwargs)
        context['scenes'] = SCENES
        return context
