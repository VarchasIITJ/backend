from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Referee

class RefereeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(allow_blank=True)
    sport = serializers.CharField(allow_blank=True)

    class Meta:
        model = Referee
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'sport',
            'created_at',
            'updated_at',
        ]


class RefereeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referee
        # Only include fields needed during creation
        fields = [
            'name',
            'email',
            'phone',
            'sport',
        ]
