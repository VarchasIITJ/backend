from django.views.generic import TemplateView
from .models import OurTeam
from django.shortcuts import get_object_or_404, render
from accounts.models import  UserProfile
from .serializers import OurTeamSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response 
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import csv
from registration.models import TeamRegistration 

class IndexView(TemplateView):

    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        if self.request.user.username != "":
            context['page'] = "home"
        return context

class OurTeamViewSet(APIView):
    """
    API endpoint that allows core teams to be viewed, created, updated, or deleted.
    """
    # permission_classes=[IsAuthenticated]

    def post(self,request):
        serializer=OurTeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_402_PAYMENT_REQUIRED)
        
    def get(self, request):
        teams_data = OurTeam.objects.all()
        if not teams_data:
            return Response({"message": "No members found"}, status=status.HTTP_204_NO_CONTENT)
        grouped_data = {}
        for team_member in teams_data:
            position_id = team_member.position
            if position_id not in grouped_data:
                grouped_data[position_id] = []
            serialized_member = OurTeamSerializer(team_member).data
            grouped_data[position_id].append(serialized_member)
        return Response(grouped_data, status=status.HTTP_200_OK)

def error_404(request, exception):
    return render(request, 'main/error_404.html', status=404)

def error_500(request):
    return render(request, 'main/error_500.html', status=500)

# ✅ Helper: restrict to admin/superuser
def is_admin(user):
    return user.is_superuser or user.is_staff


# ✅ Admin dashboard page
@login_required(login_url='/login/')
@user_passes_test(is_admin)
def pr_data(request):
    """Render the PR admin dashboard page."""
    return render(request, 'pr.html')


# ✅ Serve user data (for AJAX requests)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_data(request):
    if not is_admin(request.user):
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    users = UserProfile.objects.all()
    data = []
    for u in users:
        data.append({
            "username": u.user.username,
            "uniqueId": u.uniqueId,
            "college": u.college,
            "phone": u.phone,
            "gender": u.get_gender_display(),  # use display value
            "accommodation_required": u.get_accommodation_required_display(),  # display value
            "accommodation_paid": u.get_accommodation_paid_display(),  # display value
            "amount_required": u.amount_required,
            "amount_paid": u.amount_paid
        })

    return Response(data, status=status.HTTP_200_OK)

# ✅ Serve team data
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teams_data(request):
    if not is_admin(request.user):
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    teams = TeamRegistration.objects.all()
    data = []
    for t in teams:
        data.append({
            "teamId": t.teamId,
            "team_name": t.team_name,
            "sport": t.get_sport_display(),
            "category": t.get_category_display(),
            "college": t.college,
            "payment_status": t.get_payment_status_display(),
            "teamsize": t.teamsize,
            "teamcount": t.teamcount,
            "captain_name": t.captain.user.get_full_name() if t.captain else "",
            "captain_email": t.captain.user.email if t.captain else "",
            "athletics_events": [e.get_event_name_display() for e in t.athletics_events.all()]
        })

    return Response(data, status=status.HTTP_200_OK)


# ✅ Serve allowed users data (those with accommodation paid)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allowed_users_data(request):
    if not is_admin(request.user):
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    allowed = UserProfile.objects.filter(accommodation_paid='2')  # '2' means Paid
    data = []
    for a in allowed:
        data.append({
            "user_id": a.user.id,
            "name": a.user.get_full_name(),
            "email": a.user.email,
            "college": a.college
        })

    return Response(data, status=status.HTTP_200_OK)

# ✅ CSV Downloads (still use HttpResponse)
@login_required(login_url='/login/')
@user_passes_test(is_admin)
def download_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Username', 'Unique ID', 'College', 'Phone', 'Gender',
        'Accommodation Required', 'Accommodation Paid', 'Amount Required', 'Amount Paid'
    ])

    users = UserProfile.objects.all()
    for u in users:
        writer.writerow([
            u.user.username, u.uniqueId, u.college, u.phone,
            u.get_gender_display(),  # display value
            u.get_accommodation_required_display(),  # display value
            u.get_accommodation_paid_display(),  # display value
            u.amount_required, u.amount_paid
        ])
    return response

@login_required(login_url='/login/')
@user_passes_test(is_admin)
def download_teams_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="teams.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Team ID', 'Team Name', 'Sport', 'Category', 'College',
        'Teamsize', 'Teamcount', 'Captain Name', 'Captain Email', 'Athletics Events'
    ])

    teams = TeamRegistration.objects.all()
    for t in teams:
        writer.writerow([
            t.teamId, t.team_name, t.get_sport_display(), t.get_category_display(),
            t.college, t.teamsize, t.teamcount,
            t.captain.user.get_full_name() if t.captain else "",
            t.captain.user.email if t.captain else "",
            ", ".join([e.get_event_name_display() for e in t.athletics_events.all()])
        ])
    return response


@login_required(login_url='/login/')
@user_passes_test(is_admin)
def download_allowed_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="allowed_users.csv"'
    writer = csv.writer(response)
    writer.writerow(['User ID', 'Name', 'Email', 'College'])

    allowed = UserProfile.objects.filter(accommodation_paid='2')
    for a in allowed:
        writer.writerow([
            a.user.id, a.user.get_full_name(), a.user.email, a.college
        ])
    return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment(request):
    user = request.user
    userprofile = get_object_or_404(UserProfile, user=user)

    # Get all teams where the user is the captain and payment is not yet made
    unpaid_teams = userprofile.teamId.filter(captain=userprofile, payment_status='1')

    if not unpaid_teams.exists():
        return Response(
            {"message": "No pending payments. All your teams are already paid or no teams found."},
            status=status.HTTP_200_OK
        )

    track_team = ["4x100m", "4x400m"]
    total_amount = 0

    for team in unpaid_teams:
        sport = team.sport
        category = team.category
        team_name = team.team_name or ""
        amount = 0

        # --- Athletics ---
        if sport == '1':
            if category == 'M':
                amount = 700 if team_name in track_team else 200
            elif category == 'W':
                amount = 500 if team_name in track_team else 150
            else :
                amount = 600 if team_name in track_team else 175    

        # --- Badminton ---
        elif sport == '2':
            if category == 'M':
                amount = 1300
            elif category == 'W':
                amount = 1200
            else :
                amount = 1500

        # --- Basketball ---
        elif sport == '3':
            amount = 3500 if category == 'M' else 2500

        # --- Cricket ---
        elif sport == '4' and category == 'M':
            amount = 5500

        # --- Football ---
        elif sport == '5':
            amount = 5500 if category == 'M' else 2500

        # --- Table Tennis ---
        elif sport == '6':
            amount = 1300 if category == 'M' else 1200

        # --- Lawn Tennis ---
        elif sport == '7':
            amount = 1000 if category == 'M' else 500

        # --- Volleyball ---
        elif sport == '8':
            amount = 3500 if category == 'M' else 2500

        # --- Kabaddi ---
        elif sport == '9':
            amount = 4000 if category == 'M' else 2000

        # --- Hockey ---
        elif sport == '10' and category == 'M':
            amount = 3500

        # --- Squash ---
        elif sport == '11':
            amount = 700 if category == 'M' else 500

        # --- Chess ---
        elif sport == '12':
            amount = 500

        # --- Esports ---
        elif sport == '13':
            amount = 99  # BGMI
        elif sport == '14':
            amount = 499  # Valorant
        elif sport == '15':
            amount = 250  # Clash Royale

        total_amount += amount

    # Save total to user profile
    userprofile.amount_required = total_amount
    userprofile.save()

    return Response(
        {"message": f"The total amount you have to pay: ₹{total_amount}", "pending_teams": list(unpaid_teams.values_list("teamId", flat=True))},
        status=status.HTTP_200_OK
    )