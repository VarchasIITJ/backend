from rest_framework import serializers
from .models import Referee

class RefereeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(allow_blank=True)
    sport = serializers.CharField(allow_blank=True)
    account_holder_name = serializers.CharField(allow_blank=True)
    ifsc_code = serializers.CharField(allow_blank=True)
    bank_account_number = serializers.CharField(allow_blank=True)

    class Meta:
        model = Referee
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'sport',
            'account_holder_name',
            'ifsc_code',
            'bank_account_number',
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
            'account_holder_name',
            'ifsc_code',
            'bank_account_number',
        ]
