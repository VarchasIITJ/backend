from .views import TeamViewSet,removeplayer,CreateTeamView,TeamRegistrationListAPIView
from rest_framework import routers
from django.urls import path, include

app_name = 'registration'
router = routers.DefaultRouter()
router.register('teamsApi', TeamViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('removeplayer/',removeplayer,name='removeplayer'),
    path('createteam/',CreateTeamView,name='CreateTeamView'),
    path('teams/', TeamRegistrationListAPIView.as_view(), name='teamregistration-list'),
    # url(r'team/(?P<username>[a-zA-Z0-9]+)$',TeamFormationView),
]
