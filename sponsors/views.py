
from .models import Sponsor,SponsorType
from rest_framework import viewsets, permissions
from .serializers import SponsorSerializer,SponsorTypeSerializer


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.AllowAny]

class SponsorSet(viewsets.ModelViewSet):
    queryset = SponsorType.objects.all()
    serializer_class = SponsorTypeSerializer
    permission_classes = [permissions.AllowAny]