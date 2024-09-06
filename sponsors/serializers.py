from .models import Sponsor,SponsorType
from rest_framework import serializers


class SponsorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SponsorType
        fields = ['name','order']

class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = '__all__'
