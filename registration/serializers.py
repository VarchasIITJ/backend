from .models import TeamRegistration, AthleticsSubEvent
from accounts.models import UserProfile
from rest_framework import serializers
from accounts.serializers import UserProfileSerailizerForTeam

class MultiTeamSerializer(serializers.Serializer):
    sport = serializers.IntegerField()
    categories = serializers.ListField(
        child=serializers.ChoiceField(choices=TeamRegistration.CATEGORY_CHOICES)
    )
    teams = serializers.ListField(child=serializers.CharField(max_length=100))
    teamsize = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate(self, data):
        if not (len(data['categories']) == len(data['teams']) == len(data['teamsize'])):
            raise serializers.ValidationError("Length of categories, teams, and teamsize must match.")
        return data


class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamRegistration
        fields = '__all__'


class TeamsSerailizerForPR(serializers.ModelSerializer):
    captain_name = serializers.CharField(source='captain.user.first_name', read_only=True)
    captain_email = serializers.EmailField(source='captain.user.email', read_only=True)
    captain_phone = serializers.CharField(source='captain.phone', read_only=True)
    members = serializers.SerializerMethodField()
    athletics_events = serializers.SerializerMethodField()  # 👈 added

    class Meta:
        model = TeamRegistration
        fields = [
            'teamId',
            'sport',
            'category',
            'team_name',
            'college',
            'payment_status',
            'teamsize',
            'teamcount',
            'captain_name',
            'captain_email',
            'captain_phone',
            'members',
            'athletics_events',
        ]

    def get_members(self, obj):
        members = UserProfile.objects.filter(teamId=obj)
        return [
            {
                "name": member.user.first_name,
                "email": member.user.email,
                "phone": member.phone,
                "college": member.college,
            }
            for member in members
        ]

    def get_athletics_events(self, obj):
        # only include for athletics sport
        if str(obj.sport) == '1':
            sub_events = obj.athletics_events.all()  # assumes related_name='athletics_events'
            return [event.event_name for event in sub_events]
        return []
