
from django.shortcuts import get_object_or_404
from accounts.models import UserProfile
from .models import TeamRegistration, AthleticsSubEvent
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework import viewsets,generics
from .serializers import TeamsSerializer,TeamsSerailizerForPR, MultiTeamSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes  
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from random import randint
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail



class TeamRegistrationListAPIView(generics.ListAPIView):
    queryset = TeamRegistration.objects.all()
    serializer_class = TeamsSerailizerForPR
    # permission_classes = [IsAdminUser]



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTeamView(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    serializer = MultiTeamSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Input
    sport = int(request.data.get('sport'))
    categories = request.data.get('categories', [])
    teamsize_list = request.data.get('teamsize', [])
    teams_data = request.data.get('teams', [])
    team_id_data = request.data.get('team_id', {})
    event_data = request.data.get('event_data', [])  # for esports in-game IDs

    # Athletics sub-events
    track_single = [
        "100m", "200m", "400m", "800m", "1500m", "5000m",
        "Long Jump", "Triple Jump", "High Jump", "Discuss Throw", "Javelin Throw", "Shot Put"
    ]
    track_team = ["4x100m", "4x400m"]

    existing_teams = user_profile.teamId.all()

    # --- Restriction checks ---
    if sport == 1:  # Athletics
        registered_events = [
            subevent.event_name
            for team in existing_teams.filter(sport='1')
            for subevent in team.athletics_events.all()
        ]

        for new_event in teams_data:
            if new_event in registered_events:
                return Response(
                    {"message": f"You are already registered for Athletics - {new_event}."},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )

        if len(registered_events) + len(teams_data) > 3:
            return Response(
                {"message": "You can register for a maximum of 3 athletics events."},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

    elif sport in range(2, 13):  # Normal sports
        for i, team_name in enumerate(teams_data):
            cat = categories[i]
            for team in existing_teams.filter(sport=str(sport)):
                if team.category == cat:
                    return Response(
                        {"message": f"You are already registered for {team.get_sport_display()} - category {team.get_category_display()}."},
                        status=status.HTTP_406_NOT_ACCEPTABLE
                    )

    elif sport in [13, 14, 15]:  # Esports
        if existing_teams.filter(sport=str(sport)).exists():
            return Response(
                {"message": f"You are already registered for {existing_teams.filter(sport=str(sport)).first().get_sport_display()}."},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

    spor = TeamRegistration.SPORT_CHOICES[sport - 1][1][:3]
    created_teams = []

    # --- Create teams ---
    for i, team_name in enumerate(teams_data):
        category = categories[i]
        size = teamsize_list[i] if i < len(teamsize_list) else 1

        # Generate team ID
        if category == "X":  # Mixed
            team_id = f"V-{spor.upper()}-D-{team_name[:1].upper()}-{user.username[:3].upper()}-{randint(1,99)}-{randint(1,9)}"
        elif team_name in track_single:
            team_id = f"V-{spor.upper()}-{category[:1]}-I-{user.username[:3].upper()}-{randint(1,99)}-{randint(1,9)}"
        elif team_name in track_team:
            team_id = f"V-{spor.upper()}-{category[:1]}-T-{user.username[:3].upper()}-{randint(1,99)}-{randint(1,9)}"
        else:
            team_id = f"V-{spor.upper()}-{category[:1]}-{team_name[:1].upper()}-{user.username[:3].upper()}-{randint(1,99)}-{randint(1,9)}"

        # Create TeamRegistration
        team = TeamRegistration.objects.create(
            teamId=team_id,
            sport=sport,
            college=user_profile.college,
            captain=user_profile,
            score=-1,
            category=category,
            teamsize=size,
            teamcount=1,
            team_name=team_name
        )

        # Add captain to the team
        user_profile.teamId.add(team)

        # --- Athletics-specific ---
        if sport == 1:
            if i < len(event_data):
                sub_event_name = event_data[i]
                AthleticsSubEvent.objects.create(team=team, event_name=sub_event_name)
            else:
                return Response(
                    {"message": f"No athletics event provided for team {team_name}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # --- Esports in-game ID handling ---
        if sport in [13, 14, 15]:
            # Set esports flag
            user_profile.isesports = True

            # For BGMI
            if sport == 13:
                user_profile.team_member1_bgmi_ingame_id = team_id_data.get('id1')
                user_profile.team_member2_bgmi_ingame_id = team_id_data.get('id2')
                user_profile.team_member3_bgmi_ingame_id = team_id_data.get('id3')
                user_profile.team_member4_bgmi_ingame_id = team_id_data.get('id4')

            # For Valorant
            elif sport == 14:
                user_profile.team_member1_val_ingame_id = team_id_data.get('id1')
                user_profile.team_member2_val_ingame_id = team_id_data.get('id2')
                user_profile.team_member3_val_ingame_id = team_id_data.get('id3')
                user_profile.team_member4_val_ingame_id = team_id_data.get('id4')
                user_profile.team_member5_val_ingame_id = team_id_data.get('id5')

            # For Clash Royale
            elif sport == 15:
                user_profile.team_member1_cr_ingame_id = team_id_data.get('id1')

            team.save()
            user_profile.save()

        # --- Email confirmation ---
        subject = 'Varchas24 | Team Registration Confirmation'
        message = (
            f"Hi {user.first_name}, your Team ID for {team.get_sport_display()} "
            f"({team_name}) in category {team.get_category_display()} is {team_id}."
        )
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        created_teams.append(team_id)

    return Response(
        {"message": "Team(s) created successfully. Check your profile.", "Teams": created_teams},
        status=status.HTTP_201_CREATED
    )

# This view is commented for reference purpose. This view restrict player to only one offline and one online event.
# def CreateTeamView(request):
#     user = request.user
#     user_profile = UserProfile.objects.get(user=user)
#     sport = request.data['sport']
#     sport_info = int(sport)
#     if user_profile.teamId.exists():
#         if sport_info in [1,2,3,4,5,6,7,8,9,10,11,12] :
#             teams=user_profile.teamId.all()
#             for team in teams:
#                 if int(team.sport) in [1,2,3,4,5,6,7,8,9,10,11,12] :
#                     message = "You are not able to create a new team"
#                     message += "\nYou have to register again to join another team. \nContact Varchas administrators."
#                     return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
#         if sport_info in [13,14,15]:
#             teams=user_profile.teamId.all()
#             for team in teams:
#                 if int(team.sport) == sport_info :
#                     message = "You are not able to create a new team"
#                     message += "\nYou have to register again to join another team. \nContact Varchas administrators."
#                     return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)
#     requested_data = {
#         "sport": sport_info,
#         "category": request.data['category'],
#         "teamsize": request.data['teamsize'],
#     }
#     serializer = TeamsSerializer(data=requested_data)
#     if serializer.is_valid():
#         category = serializer.validated_data['category']
#         teamsize = serializer.validated_data['teamsize']
#         sport = serializer.validated_data['sport']
#         spor = TeamRegistration.SPORT_CHOICES[int(sport)-1][1][:3]
#         teams_data = request.data.get('teams', [])

#         # Generate the team ID
#         track_single=["100m", "200m", "400m", "800m", "1500m", "5000m","Long Jump","Triple Jump","High Jump","Discuss Throw","Javelin Throw","Shot Put"]
#         track_team=["4x100m","4x400m"] 

#         for team_name in teams_data: 

#             if category=="mixed":
#                 team_id="V-{}-{}-{}-{}-{}-{}".format(spor[:3].upper(), 'D', team_name[:1].upper(),user.username[:3].upper(),randint(1, 99), randint(1, 9))

#             elif team_name in track_single:
#                 team_id="V-{}-{}-{}-{}-{}-{}".format(spor[:3].upper(), category[:1].upper(), 'I',user.username[:3].upper(),randint(1, 99), randint(1, 9))
            
#             elif team_name in track_team:
#                 team_id="V-{}-{}-{}-{}-{}-{}".format(spor[:3].upper(), category[:1].upper(), 'T',user.username[:3].upper(),randint(1, 99), randint(1, 9))

#             elif team_name=="Blitz" or team_name=="Classical":
#                 team_id="V-{}-{}-{}-{}-{}-{}-{}".format(spor[:3].upper(), category[:1].upper(),'I',team_name[:1].upper(),user.username[:3].upper(),randint(1, 99), randint(1, 9))
            
#             elif spor=="Tab" and team_name=="Team":
#                 team_id="V-{}-{}-{}-{}-{}-{}".format(spor[:3].upper(), category[:1].upper(), 'I',user.username[:3].upper(),randint(1, 99), randint(1, 9))

#             else:
#                 team_id = "V-{}-{}-{}-{}-{}-{}".format(spor[:3].upper(), category[:1].upper(), team_name[:1].upper(),user.username[:3].upper(),randint(1, 99), randint(1, 9))
#             team = TeamRegistration.objects.create(
#                 teamId=team_id,
#                 sport=sport,
#                 college=user_profile.college,
#                 captain=user_profile,
#                 score=-1,
#                 category=category,
#                 teamsize=teamsize,
#                 teamcount=1,
#                 teams=team_name
#             )
#             user1=request.user
#             subject='Varchas24 | Confirmation of Team registration'
#             message = f'Hi {user1.first_name}, Thank you for being part of Varchas24 . The TeamId of {TeamRegistration.SPORT_CHOICES[int(sport)-1][1]} {team_name} is {team_id}.'
#             email_from = settings.EMAIL_HOST_USER
#             recipient_list = [user1.email,]
#             send_mail( subject, message, email_from, recipient_list )
#             user_profile.teamId.add(team)
#             if sport_info in [13, 15]:
#                     # team.teamcount = team.teamsize
#                     team.save()
#                     if sport_info == 13:
#                         user_profile.team_member1_bgmi_ingame_id = request.data.get('team_id', {}).get('id1')
#                         user_profile.team_member2_bgmi_ingame_id = request.data.get('team_id', {}).get('id2')
#                         user_profile.team_member3_bgmi_ingame_id = request.data.get('team_id', {}).get('id3')
#                         user_profile.team_member4_bgmi_ingame_id = request.data.get('team_id', {}).get('id4')
#                     if sport_info == 14:
#                         user_profile.team_member1_val_ingame_id = request.data.get('team_id', {}).get('id1')
#                         user_profile.team_member2_val_ingame_id = request.data.get('team_id', {}).get('id2')
#                         user_profile.team_member3_val_ingame_id = request.data.get('team_id', {}).get('id3')
#                         user_profile.team_member4_val_ingame_id = request.data.get('team_id', {}).get('id4')
#                         user_profile.team_member5_val_ingame_id = request.data.get('team_id', {}).get('id5')
#                     if sport_info ==15 :
#                         user_profile.team_member1_cr_ingame_id =request.data.get('team_id', {}).get('id1')


#                     user_profile.isesports = True
                
#             user_profile.save()
#             print(user_profile)
#         return Response({"message": "Team(s) created successfully.Check your Profile"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removeplayer(request):
    user = request.user
    user_profile = get_object_or_404(UserProfile, user=user)
    
    # Ensure teamId is provided
    team_id = request.data.get('teamId')
    if not team_id:
        return Response({"message": "teamId is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Get the team
    team = get_object_or_404(TeamRegistration, teamId=team_id)

    # Only captain can remove players
    if user_profile != team.captain:
        return Response({"message": "Only the captain can remove a player from the team."},
                        status=status.HTTP_403_FORBIDDEN)

    # Get the user to remove
    user_to_remove_id = request.data.get('user')
    if not user_to_remove_id:
        return Response({"message": "user ID is required to remove a player."}, status=status.HTTP_400_BAD_REQUEST)

    # Captain cannot remove themselves
    if str(user_profile.user.id) == str(user_to_remove_id):
        return Response({"message": "Captain cannot remove themselves."}, status=status.HTTP_400_BAD_REQUEST)

    # Get the player to remove
    try:
        user_to_remove = User.objects.get(id=user_to_remove_id)
        player_to_remove = UserProfile.objects.get(user=user_to_remove)
    except (User.DoesNotExist, UserProfile.DoesNotExist):
        return Response({"message": "The specified user does not exist or is not a member."},
                        status=status.HTTP_404_NOT_FOUND)

    # Check if player is in the team
    if not team.member.filter(id=player_to_remove.id).exists():
        return Response({"message": "The specified user is not part of this team."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Remove player from team
    player_to_remove.teamId.remove(team)
    team.teamcount = max(team.teamcount - 1, 0)
    team.save()

    return Response(
        {"message": f"{player_to_remove.user.username} has been removed from the team."},
        status=status.HTTP_200_OK
    )
# def removeplayer(request):
#     user = request.user
#     user_profile = UserProfile.objects.get(user=user)
#     print("User Profile:", user_profile)
#     team_id = request.data.get('teamId') # this is done because one person now have enrolled in multiple teams so we have to specify from which team captain is removing player.
#     # team_id = user_profile.teamId.all()   this was fetching all teams of user but user previously was allowed to have only one team so directly accessed it.
#     print("User's Team ID:", team_id)

#     if user_profile.teamId is None:
#         return Response({"message": "You must be registered in a team to complete this operation."},
#                         status=status.HTTP_400_BAD_REQUEST)

#     team = TeamRegistration.objects.get(teamId=team_id)
#     if user_profile != team.captain:
#         return Response({"message": "Only the captain can remove a player from the team."},
#                         status=status.HTTP_401_UNAUTHORIZED)

#     user_to_remove_id = request.data.get('user')
#     user_to_remove = User.objects.filter(id=user_to_remove_id).first()  # Get the User object
    
#     if user_to_remove is None:
#         return Response({"message": "The specified user does not exist."},
#                         status=status.HTTP_400_BAD_REQUEST)

#     player_to_remove = UserProfile.objects.filter(user=user_to_remove).first()  # Get the associated UserProfile
    
#     if player_to_remove is None:
#         return Response({"message": "The specified user is not in the team."},
#                         status=status.HTTP_400_BAD_REQUEST)
#     if user_profile == player_to_remove:
#         return Response({"message": "You can not remove your self"},
#                         status=status.HTTP_400_BAD_REQUEST)

#     player_to_remove.teamId = None
#     player_to_remove.save()
#     team.teamcount=team.teamcount-1
#     team.save()
#     return Response({"message": "Player removed from the team successfully."},
#                     status=status.HTTP_200_OK)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = TeamRegistration.objects.all() 
    serializer_class = TeamsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
