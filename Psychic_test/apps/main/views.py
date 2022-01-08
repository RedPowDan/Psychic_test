from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
from .services.psychic_service import PsychicService

KEY_FOR_PSYCHICS = "psychics"
KEY_FOR_ENDGAME = "is_end"
KEY_FOR_HISTORY_PLAYER = "history_player"


def index(request: HttpRequest):
    psychic_service = PsychicService()
    psychics = []
    desired_value = None
    is_gamed = "is_gamed" in request.session
    if not is_gamed:
        request.session[KEY_FOR_HISTORY_PLAYER] = ""

    request.session['buf'] = 'buf'
    if KEY_FOR_PSYCHICS not in request.session:
        psychics = psychic_service.generate_psychics()
        request.session[KEY_FOR_PSYCHICS] = psychic_service.psychics_to_list_in_dict(psychics)
    else:
        psychics = psychic_service.psychics_from_dict_to_list(request.session[KEY_FOR_PSYCHICS])

    if request.method == "POST":
        request.session["is_gamed"] = True
        desired_value = request.POST.get("desired_value", None)
        if desired_value is not None:
            request.session[KEY_FOR_HISTORY_PLAYER] += desired_value + " "
            desired_value = int(desired_value)
            psychics = psychic_service.get_psychic_with_predictions(psychics)
            psychics = psychic_service.summarizing(desired_value, psychics)
            request.session[KEY_FOR_PSYCHICS] = psychic_service.psychics_to_list_in_dict(psychics)
            request.session[KEY_FOR_ENDGAME] = True

    return render(request, 'main/index.html', {"desired_value": desired_value, "is_gamed": is_gamed})
