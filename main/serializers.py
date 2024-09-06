from .models import OurTeam
from rest_framework import serializers

class OurTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = ['name','email','phone','insta','fp','linkedIn','picture','position','id']
