from django.urls import path, include
from rest_framework import routers
from .views import SponsorViewSet, SponsorSet

app_name = 'sponsor'

router = routers.DefaultRouter()
router.register(r'sponsor', SponsorViewSet, basename='sponsor')
router.register(r'sponsortype', SponsorSet, basename='sponsortype')


urlpatterns = [
    path('sponsorapi/', include((router.urls, 'sponsor'), namespace='sponsor-api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
