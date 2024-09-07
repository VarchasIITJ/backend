from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import UserProfile,PasswordResetRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username','password']



class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model=UserProfile
        fields='__all__'

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetRequest
        fields = '__all__'  # You can specify the fields you want to include here


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

#         {
#     "email":"sai@iitj.ac.in",
#     "password":"akarsh14831",
#     "confirm_password":"akarsh14831",
#     "
#     "phone": "82454360",
#     "gender": "M",
#     "college": "k",
#     "state": "1",
#     "accommodation_required": "Y",
#     "accomodation_type": "1",
#     "amount_required": 0,
#     "amount_paid": 0,
#     "no_of_days": "",
#     "id_issued": false,
#     "qr_code": null,
#     "user": 8,
#     "teamId": 12
#   }