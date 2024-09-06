from django.urls import path

from . import views

urlpatterns = [
    # path('create_match/', views.create_match, name='create_match'),
    path('get_matches/', views.get_matches, name='get_match'),
    path('sponsors/', views.get_sponsors, name="get_sponsors"),
    path('informals/', views.get_informal_events, name='get_informal_events'),
    path('score/', views.get_scorelinks, name="get_scorelinks"),
]
