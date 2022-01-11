from django.urls import path

from .import views

app_name = 'main'

urlpatterns = [
    path('', views.BeginGameView.as_view(), name='begin'),
    path('summarizing', views.SummarizingView.as_view(), name='summarizing'),
    path('guesswork', views.GuessworkView.as_view(), name='guesswork'),
]
