import random
from .models import UserProfile,PasswordResetRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
from registration.models import TeamRegistration
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer,UserProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, redirect
from django.contrib.auth.hashers import make_password

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from django.http import JsonResponse
from django.contrib.auth import login
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import User
import os

import sys

# api method to register the user 

load_dotenv()

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

class RegisterUserView(APIView):
    def post(self, request):
        print("Request data:", request.data)  # Log incoming request data
        
        user1 = User.objects.filter(email=request.data.get('email')).first()
        if user1:
            print("Email already exists")
            return Response({"Error": "Email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('password') != request.data.get('confirm_password'):
            print("Password doesnt match")
            return Response({"Error": "Passwords don't match!"}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = make_password(request.data["password"])
        user_data = {
            "email": request.data["email"],
            "username":request.data["email"],
            "password": hashed_password,
        }
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            return Response({"message":'User created Successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
        # if user_serializer.is_valid():
        #     user = user_serializer.save()
        #     profile_data = {
        #         "user": user.id,
        #         "phone": request.data["phone"],
        #         "gender": request.data["gender"],
        #         "college": request.data["college"],
        #         "state": request.data["state"],
        #         "accommodation_required": request.data["accommodation_required"],
        #     }

        #     profile_serializer = UserProfileSerializer(data=profile_data)
        #     if profile_serializer.is_valid():
        #         profile_serializer.save()
        #         return Response({"message": 'User created Successfully'}, status=status.HTTP_201_CREATED)
        #     else:
        #         user.delete()
        #         print("Profile serializer errors:", profile_serializer.errors)  # Log profile serializer errors
        #         return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     print("User serializer errors:", user_serializer.errors)  # Log user serializer errors
        #     return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# api method to login the user 

@api_view(['POST'])
def LoginUserView(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        return Response({"message": 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
    
    if not user.check_password(password):
        return Response({"message": 'Invalid Password or Email'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a JWT token
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)  # Extract the refresh token value

    return Response({"message": 'User Logged in Successfully!', "access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def google_login(request):
    email_id=request.data.get('email')

    try:
        user = User.objects.get(email=email_id)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)  # Extract the refresh token value
        return Response({"message": 'User Logged in Successfully!', "access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'message': 'Account not existing in db'})
    

    

    





@api_view(['POST'])
def google_signup(request):
    email_id = request.data.get('email')
    if not email_id:
        return JsonResponse({'error': 'Email is required'}, status=400)
    # print(email_id)
    try:
        user = User.objects.get(email=email_id)
        return JsonResponse({'message': 'User already exists kindly login!'}, status=200)
    except User.DoesNotExist:
        # Create a new user if not found
       
        user = User(email=email_id)
        user.save()
        print("user created just now")
        return JsonResponse({'message': 'User created, please provide additional info'}, status=200)


class UpdateUserInfoView(APIView):
    def put(self, request):
        # Retrieve the user based on the email passed in the request
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"Error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        

        profile_data = {
                "user": user.id,
                "phone": request.data["phone"],
                "gender": request.data["gender"],
                "college": request.data["college"],
                "state": request.data["state"],
                "accommodation_required": request.data["accommodation_required"],
            }

        profile_serializer = UserProfileSerializer(data=profile_data)

        

        if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({"message": 'Profile Updated Successfully'}, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            print("Profile serializer errors:", profile_serializer.errors)  # Log profile serializer errors
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_superuser:
            return reverse('adminportal:dashboard')
        else:
            return reverse('main:home')

class PasswordReset(APIView):
    def post(self,request):
         email = request.data.get('email')
         user=get_object_or_404(User,email=email)
         if not user:
             return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
         otp = random.randint(1000, 9999)
         try :
             reset_request=PasswordResetRequest.objects.get(email=email)
             reset_request.otp=otp
             reset_request.save()
         except:
            reset_request = PasswordResetRequest(user=user,email=email,otp=otp)
            reset_request.save()
         subject='Varchas23 | OTP Verification'
         message = f'Hi {user.username}, Here is your otp {otp}.'
         email_from = settings.EMAIL_HOST_USER
         recipient_list = [user.email, ]
        
         print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}", file=sys.stderr)
         send_mail( subject, message, email_from, recipient_list )
         return Response({"message":"OTP sent Successfully!"},status=status.HTTP_201_CREATED)         

class OTPVerification(APIView):
    def post(self, request):
        email_req = request.data['email']
        otp = request.data.get('otp')

        try:
            reset_request =PasswordResetRequest.objects.filter(email=email_req).first()
        except PasswordResetRequest.DoesNotExist:
            return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
        if reset_request.expiration_time < timezone.now():
            return Response({"message": "OTP has expired."}, status=status.HTTP_400_BAD_REQUEST)

        if reset_request.otp != int(otp):
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def resendpassword(request):
    email_req=request.data.get('email')
    user=get_object_or_404(User,email=email_req)
    if not user:
        return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
    try:
        reset_request=PasswordResetRequest.objects.get(email=email_req)
    except:
        return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)     
    otp = random.randint(1000, 9999)
    reset_request.otp=otp
    reset_request.save()
    subject='Varchas23 | OTP Verification'
    message = f'Hi {user.username}, Here is your otp {otp}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )
    return Response({"message":"OTP sent Successfully!"},status=status.HTTP_201_CREATED) 

@api_view(['POST'])
def restpassword(request):
    email_req=request.data.get('email')
    password=request.data.get('password')
    try:
        user=User.objects.get(email=email_req)
    except:
        return Response({"message":"Sorry! User not found"},status=status.HTTP_404_NOT_FOUND)
    user.set_password(password)
    user.save()
    return Response({"message":"Successfully changed password"},status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userleaveTeam(request):
    user = get_object_or_404(UserProfile, user=request.user)
    teamId = user.teamId
    team = get_object_or_404(TeamRegistration, teamId=teamId)
    user.teamId = None
    user.save()
    team.delete()
    return Response({"message": "You have left the team successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userjoinTeam(request):
    user = request.user
    teamId = request.data.get('teamId')
    if user is not None:
        user = get_object_or_404(UserProfile, user=user)
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        sport = team.sport
        sport_info = int(sport) 
        if user.teamId.exists():
            if sport_info in [1,2,3,4,5,6,7,8,9,10,11,12] :
                teams=user.teamId.all()
                for team in teams:
                    if int(team.sport) in [1,2,3,4,5,6,7,8,9,10,11,12] :
                        message = "You are not able to join this team"
                        message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                        return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
            if sport_info in [13,14,15]:
                teams=user.teamId.all()
                for team in teams:
                    if int(team.sport) == sport_info :
                        message = "You are not able to join this team"
                        message += "\nYou have to register again to join another team. \nContact Varchas administrators."
                        return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        # if user.gender != team.captian.gender:
        #     return Response({"message":"Sorry,Gender not matched!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
        team = get_object_or_404(TeamRegistration, teamId=teamId)
        if(int(team.teamcount) < int(team.teamsize)):
            user.teamId.add(team)
            user.save()
            team.teamcount=team.teamcount+1
            team.save()
            return Response({"message": "Joined team Successfully!"}, status=status.HTTP_201_CREATED)
        else:
           return Response({"message":"Sorry,Team size exceeded!"},status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayteam(request):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        team_data = []
        if user_profile.teamId.exists():
            teams = user_profile.teamId.all()
            for team in teams:
                team_users_info = [
                    {
                        "user_id": user_data.user.id,
                        "email": user_data.user.username,
                        "phone": user_data.phone,
                        "name": user_data.user.first_name + user_data.user.last_name
                    }
                    for user_data in UserProfile.objects.filter(teamId=team)
                ]
                team_info = {
                    "team_id": team.teamId,
                    "sport": team.sport,
                    "college": team.college,
                    "captain_username": team.captian.user.first_name + team.captian.user.last_name if team.captian else None,
                    "score": team.score,
                    "category": team.category,
                    "players_info":team_users_info,
                    "captain": team.captian==user_profile
                }
                
                team_data.append(team_info)
        
        if not team_data:
            return Response({"message": "Join a team"}, status=status.HTTP_404_NOT_FOUND)
        
        response_data = {
            "team_data": team_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayProfile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user is None:
        return Response({"message":"User not found!"},status=status.HTTP_404_NOT_FOUND)
    response_data = {
                "team_id": [team.teamId for team in user.teamId.all()] if user.teamId.exists() else None,
                "college": user.college,
                "user_id": user.user.id,
                "email": user.user.username,
                "phone": user.phone,
                "name":user.user.first_name +user.user.last_name
         }
    return Response(response_data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]
