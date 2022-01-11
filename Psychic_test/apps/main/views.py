from django.http import HttpRequest
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

from .services.psychic_service import PsychicService

KEY_FOR_PSYCHICS = "psychics"
KEY_FOR_ENDGAME = "is_end"
KEY_FOR_HISTORY_PLAYER = "history_player"
KEY_FOR_DESIRED_VALUE = "desired_value"


class BeginGameView(TemplateResponseMixin, ContextMixin, View):
    template_name = "main/begin.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})


class GuessworkView(TemplateResponseMixin, ContextMixin, View):
    template_name = 'main/guesswork.html'
    psychic_service = PsychicService()

    def get(self, request, *args, **kwargs):
        if KEY_FOR_PSYCHICS not in self.request.session:
            psychics = self.psychic_service.generate_psychics()
            self.request.session[KEY_FOR_PSYCHICS] = self.psychic_service.psychics_to_list_in_dict(psychics)
        else:
            psychics = self.psychic_service.psychics_from_dict_to_list(self.request.session[KEY_FOR_PSYCHICS])
        psychics = self.psychic_service.get_psychic_with_predictions(psychics)
        self.request.session[KEY_FOR_PSYCHICS] = self.psychic_service.psychics_to_list_in_dict(psychics)

        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        is_gamed = "is_gamed" in request.session
        if not is_gamed:
            request.session[KEY_FOR_HISTORY_PLAYER] = ""
        desired_value = request.POST.get(KEY_FOR_DESIRED_VALUE, None)
        if not self.psychic_service.validate_desired_value(desired_value):
            return redirect("/")
        self.request.session[KEY_FOR_DESIRED_VALUE] = desired_value
        request.session[KEY_FOR_HISTORY_PLAYER] += desired_value + " "
        request.session['is_gamed'] = "true"
        return redirect("/summarizing")


class SummarizingView(TemplateResponseMixin, ContextMixin, View):
    template_name = "main/summarizing.html"
    psychic_service = PsychicService()

    def get(self, request, *args, **kwargs):
        if KEY_FOR_PSYCHICS not in self.request.session:
            return redirect('/')
        psychics = self.psychic_service.psychics_from_dict_to_list(self.request.session[KEY_FOR_PSYCHICS])
        desired_value = int(self.request.session[KEY_FOR_DESIRED_VALUE])
        psychics = self.psychic_service.summarizing(desired_value, psychics)
        self.request.session[KEY_FOR_PSYCHICS] = self.psychic_service.psychics_to_list_in_dict(psychics)
        return self.render_to_response({"desired_value": desired_value})

    def post(self, request, *args, **kwargs):
        return redirect('/guesswork')
