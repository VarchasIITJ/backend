from .models import TeamRegistration
from rest_framework import serializers


class TeamsSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamRegistration
        fields = '__all__'
