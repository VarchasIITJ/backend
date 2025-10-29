import random
from .models import UserProfile,PasswordResetRequest
from django.utils import timezone
from django.shortcuts import get_object_or_404
from registration.models import TeamRegistration
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets,permissions,generics
from .serializers import UserSerializer, GroupSerializer,UserProfileSerializer,UserProfileSerailizerForPR
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth.views import LoginView
from django.shortcuts import reverse, redirect
from django.contrib.auth.hashers import make_password

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import login
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import UserProfile
import os

import sys
User = get_user_model()

# api method to register the user 

class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerailizerForPR
    # permission_classes = [IsAdminUser]

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
        
        # avoiding this as with another post request this will updated
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

    print("Login attempt for email:", email)
    print("Login attempt for password:", password)
    
    user = User.objects.filter(username=email).first()
    print(user)
    
    if user is None:
        return Response({"message": 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
    userProfile=UserProfile.objects.filter(user=user).first()
    print(userProfile)
    
    if userProfile is None:
        
        return Response({
            "message":'User Profile not created',
            "profile_required": True
        }, status=status.HTTP_200_OK)
    
    
    if not user.check_password(password):
        return Response({"message": 'Invalid Password or Email'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a JWT token
    uniqueId=userProfile.uniqueId if userProfile else None
    refresh = RefreshToken.for_user(user)   
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)  # Extract the refresh token value

    return Response({"message": 'User Logged in Successfully!', "access_token": access_token, "refresh_token": refresh_token, "profile_required": False, "uniqueId": uniqueId}, status=status.HTTP_200_OK)

# API to edit user profile
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
class EditUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        # Get the authenticated user profile
        user_profile = get_object_or_404(UserProfile, user=request.user)
        
        # Update user fields (first_name, last_name)
        user = user_profile.user
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.save()

        # Update profile fields
        user_profile.phone = request.data.get('phone', user_profile.phone)
        user_profile.gender = request.data.get('gender', user_profile.gender)
        user_profile.college = request.data.get('college', user_profile.college)
        user_profile.state = request.data.get('state', user_profile.state)
        user_profile.accommodation_required = request.data.get('accommodation_required', user_profile.accommodation_required)
        
        # Save the updated profile
        user_profile.save()

        # Serialize the updated profile data
        profile_serializer = UserProfileSerializer(user_profile)
        
        return Response({
            "message": "Profile updated successfully!",
            "profile_data": profile_serializer.data
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
def google_signup(request):
    email_id = request.data.get('email')
    if not email_id:
        return JsonResponse({'error': 'Email is required'}, status=400)
    # print(email_id)
    try:
        user = User.objects.get(email=email_id)
        user_profile=UserProfile.objects.get(user=user)
        # return JsonResponse({'message': 'User already exists kindly login!'}, status=200)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)  # Extract the refresh token value
        return Response({"message": 'User Logged in Successfully!', "access_token": access_token, "refresh_token": refresh_token}, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({"message": 'User Created now needs additional information'})


    except User.DoesNotExist:
        # Create a new user if not found
       
        user_data = {
            "email": email_id,
            "username": email_id,  # Set email as the username
        }
        
        user = User(email=email_id, username=email_id)


        user.set_unusable_password()  # No password required for Google login
        user.save()

        return Response({"message": 'User Created now needs additional information'}, status=status.HTTP_201_CREATED)

class UpdateUserInfoView(APIView):
    def put(self, request):
        # Retrieve the user based on the email passed in the request
        email = request.data['email']
        print(email)
        print(request.data)
        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"Error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
         
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.save()

        first_name = request.data.get('first_name', '').strip().upper()
        last_name = request.data.get('last_name', '').strip().upper()
        college = request.data.get('college', '').strip().upper()

        initials_name = first_name[:3] if len(first_name) >= 3 else first_name
        initials_surname = last_name[:3] if len(last_name) >= 3 else last_name
        initials_college = college[:3] if len(college) >= 3 else college

        prefix = "VAR25"

        # Generate uniqueID inline (no helper function)
        uniqueId = f"{prefix}-{initials_name}-{initials_college}-{random.randint(1000, 9999)}"

        # Ensure uniqueId uniqueness
        while UserProfile.objects.filter(uniqueId=uniqueId).exists():
            uniqueId = f"{prefix}-{initials_surname}-{initials_college}-{random.randint(1000, 9999)}"

        profile_data = {
                "user": user.id,
                "phone": request.data["phone"],
                "gender": request.data["gender"],
                "college": request.data["college"],
                "state": request.data["state"],
                "account_holder_name": request.data["account_holder_name"],
                "ifsc_code": request.data["ifsc_code"],
                "bank_account_number": request.data["bank_account_number"],
                "uniqueId": uniqueId,
                "accommodation_required": request.data["accommodation_required"],
            }

        profile_serializer = UserProfileSerializer(data=profile_data)

        

        if profile_serializer.is_valid():
                profile_serializer.save()
                return Response({"message": 'Profile Updated Successfully', "uniqueId": uniqueId}, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            print("Profile serializer errors:", profile_serializer.errors)  # Log profile serializer errors
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_redirect_url(self):
        if self.request.user.is_staff:
            return reverse('adminportal:dashboard')
        else:
            return reverse('main:home')

class PasswordReset(APIView):
    def post(self,request):
         email = request.data.get('email')
         print(email)
         user=User.objects.get(email=email)
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
         subject='Varchas24 | OTP Verification'
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
    subject='Varchas24 | OTP Verification'
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
    user_profile = get_object_or_404(UserProfile, user=request.user)
    team_id = request.data.get('teamId')  # User must specify which team to leave

    if not team_id:
        return Response({"message": "teamId is required to leave a team."},
                        status=400)

    team = get_object_or_404(TeamRegistration, teamId=team_id)

    # Prevent captain from leaving their own team
    if user_profile == team.captain:
        return Response({"message": "Captain cannot leave their own team. Transfer captainship or remove the team instead."},
                        status=403)

    # Check if user is actually a member of this team
    if not team.member.filter(id=user_profile.id).exists():
        return Response({"message": "You are not a member of this team."},
                        status=400)

    # Remove user from team
    user_profile.teamId.remove(team)
    team.teamcount = max(team.teamcount - 1, 0)
    team.save()

    return Response({"message": f"You have successfully left the team {team.teamId}."},
                    status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def userjoinTeam(request):
    user = request.user
    if not user:
        return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

    user_profile = get_object_or_404(UserProfile, user=user)
    team_id = request.data.get('teamId')
    if not team_id:
        return Response({"message": "teamId is required."}, status=status.HTTP_400_BAD_REQUEST)

    team = get_object_or_404(TeamRegistration, teamId=team_id)
    sport_info = int(team.sport)
    existing_teams = user_profile.teamId.all()

    # --- Check if user already joined a team in the same sport/category ---
    if sport_info == 1:  # Athletics
        # User can join max 3 events
        athletics_events_count = sum(
            t.athletics_events.count() for t in existing_teams.filter(sport='1')
        )
        if athletics_events_count >= 3:
            return Response(
                {"message": "You can join a maximum of 3 Athletics events."},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        # Check if user already joined this sub-event
        sub_event_names = [e.event_name for t in existing_teams.filter(sport='1') for e in t.athletics_events.all()]
        for sub_event in team.athletics_events.all():
            if sub_event.event_name in sub_event_names:
                return Response(
                    {"message": f"You are already registered for Athletics - {sub_event.event_name}."},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

    elif sport_info in range(2, 13):  # Normal sports
        for t in existing_teams.filter(sport=str(sport_info)):
            if t.category == team.category:
                return Response(
                    {"message": f"You are already registered in {team.get_sport_display()} for category {team.get_category_display()}."},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

    elif sport_info in [13, 14, 15]:  # Esports
        if existing_teams.filter(sport=str(sport_info)).exists():
            return Response(
                {"message": f"You are already registered for {team.get_sport_display()}. Cannot join another team."},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

    # --- Check team size ---
    if team.teamcount >= team.teamsize:
        return Response({"message": "Sorry, the team is full!"}, status=status.HTTP_406_NOT_ACCEPTABLE)

    # --- Add user to the team ---
    user_profile.teamId.add(team)
    user_profile.save()

    # Increment teamcount
    team.teamcount += 1
    team.save()

    return Response({"message": f"Joined team {team.teamId} successfully!"}, status=status.HTTP_201_CREATED)

# allowing user to join only one sport or one event.
# def userjoinTeam(request):
#     user = request.user
#     teamId = request.data.get('teamId')
#     if user is not None:
#         user = get_object_or_404(UserProfile, user=user)
#         team = get_object_or_404(TeamRegistration, teamId=teamId)
#         sport = team.sport
#         sport_info = int(sport) 
#         if user.teamId.exists():
#             if sport_info in [1,2,3,4,5,6,7,8,9,10,11,12] :
#                 teams=user.teamId.all()
#                 for team in teams:
#                     if int(team.sport) in [1,2,3,4,5,6,7,8,9,10,11,12] :
#                         message = "You are not able to join this team"
#                         message += "\nYou have to register again to join another team. \nContact Varchas administrators."
#                         return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
#             if sport_info in [13,14,15]:
#                 teams=user.teamId.all()
#                 for team in teams:
#                     if int(team.sport) == sport_info :
#                         message = "You are not able to join this team"
#                         message += "\nYou have to register again to join another team. \nContact Varchas administrators."
#                         return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
#         # if user.gender != team.captain.gender:
#         #     return Response({"message":"Sorry,Gender not matched!"},status=status.HTTP_406_NOT_ACCEPTABLE)
        
#         team = get_object_or_404(TeamRegistration, teamId=teamId)
#         if(int(team.teamcount) < int(team.teamsize)):
#             user.teamId.add(team)
#             user.save()
#             team.teamcount=team.teamcount+1
#             team.save()
#             return Response({"message": "Joined team Successfully!"}, status=status.HTTP_201_CREATED)
#         else:
#            return Response({"message":"Sorry,Team size exceeded!"},status=status.HTTP_406_NOT_ACCEPTABLE)
#     return Response({"message": "User not found!"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayteam(request):
    try:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        team_data = []

        if user_profile.teamId.exists():
            teams = user_profile.teamId.all()
            for team in teams:
                # Members of the team
                team_users_info = [
                    {
                        "user_id": member.user.id,
                        "email": member.user.email,
                        "phone": member.phone,
                        "name": f"{member.user.first_name} {member.user.last_name}".strip()
                    }
                    for member in UserProfile.objects.filter(teamId=team)
                ]

                # Athletics events (if applicable)
                athletics_events = []
                if team.sport == "1":  # Athletics
                    athletics_events = [e.event_name for e in team.athletics_events.all()]

                team_info = {
                    "team_id": team.teamId,
                    "sport": team.get_sport_display(),
                    "college": team.college,
                    "captain_name": f"{team.captain.user.first_name} {team.captain.user.last_name}".strip() if team.captain else None,
                    "score": team.score,
                    "category": team.get_category_display(),
                    "players_info": team_users_info,
                    "captain": team.captain == user_profile,
                    "athletics_events": athletics_events,  # empty list for non-athletics
                    "payment_information": team.get_payment_status_display(),
                }

                team_data.append(team_info)

        if not team_data:
            return Response({"message": "Join a team"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"team_data": team_data}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userDisplayProfile(request):
    user = get_object_or_404(UserProfile, user=request.user)
    if user is None:
        return Response({"message":"User not found!"},status=status.HTTP_404_NOT_FOUND)
    
    team_ids = [team.teamId for team in user.teamId.all()] if user.teamId.exists() else None
    if user.accommodation_required == "Y":
        
        has_accom_payment = any(
            team.payment_status in ['2', '4']  
            for team in TeamRegistration.objects.filter(teamId__in=team_ids) 
        )
        accom_payment = "Yes" if has_accom_payment else "No"
    else:
        accom_payment = "NA"

    response_data = {
                "team_id": [team.teamId for team in user.teamId.all()] if user.teamId.exists() else None,
                "college": user.college,
                "user_id": user.user.id,
                "email": user.user.username,
                "phone": user.phone,
                "first_name":user.user.first_name,
                "last_name":user.user.last_name,
                "accomadation":user.accommodation_required,
                "accomadation_payment":accom_payment
            
         }
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def sendEmailToAllParticipants(request):
    users = UserProfile.objects.all()

    file_path = os.path.join('particpant_emails', 'accom_paid.txt')


    with open(file_path, 'w') as file:
        for user in users:
            for team in user.teamId.all():
                if team.payment_status in ['2', '4']:
                    # subject = 'Varchas24 | Cancellation of all Informal Events'
                    # message = f'Hi {user.user.first_name}, Thank you for being part of Varchas24. All the informal events are cancelled.'
                    # email_from = settings.EMAIL_HOST_USER
                    # recipient_list = [user.user.email]
                    # send_mail(subject, message, email_from, recipient_list)
                    file.write(f'{user.user.email}\n')
                
                    break
            
    return JsonResponse({"message": "All emails successfully saved."}, status=200)




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
