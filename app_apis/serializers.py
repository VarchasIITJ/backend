from rest_framework import serializers
from .models import InformalEvent, Matches, Sponsor


class MatchSerializer(serializers.ModelSerializer):
    # event = serializers.CharField(source="get_event_display")
    venue = serializers.CharField(source="get_venue_display")
    team1 = serializers.CharField(source="team1.teamId")
    team2 = serializers.CharField(source="team2.teamId")

    class Meta:
        model = Matches
        fields = ("team1", "team2", "college1", "college2", "event", "venue", "date", "time")


class SponsorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sponsor
        fields = "__all__"


class InformalSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformalEvent
        fields = "__all__"
