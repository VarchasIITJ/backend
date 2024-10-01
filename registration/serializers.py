from .models import TeamRegistration
from rest_framework import serializers
from accounts.serializers import UserProfileSerailizerForTeam


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRegistration
        fields = '__all__'


class TeamsSerailizerForPR(serializers.ModelSerializer):
    captain_name = serializers.CharField(source='captain.user.first_name', read_only=True)
    captain_phone = serializers.CharField(source='captain.phone', read_only=True) 
    members = UserProfileSerailizerForTeam(many=True, read_only=True, source='member')
    class Meta:
        model = TeamRegistration
        fields = ['teamId','sport','category','teams','college','captain_name','captain_phone','members']