from django.contrib.auth.decorators import login_required
from django.shortcuts import render
# from requests import request

# from events.models import Cricket, Match
from .forms import EmailForm
from registration.models import TeamRegistration
import xlwt
from django.http import HttpResponse
from django.core.mail import send_mail
from accounts.models import UserProfile
from django.views.generic import CreateView


@login_required(login_url='login')
def dashboard(request):
    if not request.user.is_superuser:
        return render(request, "404")
    teams = TeamRegistration.objects.all()
    nteams = teams.count()
    users = UserProfile.objects.all()
    nusers = users.count()
    context = {'user': request.user, 'nteams': nteams, 'nusers': nusers}
    return render(request, 'adminportal/dashboard.html', context)

@login_required(login_url='login')
def dashboardTeams(request, sport=0):
    if not request.user.is_superuser:
        return render(request, "404")
    if request.method == 'POST':
        sport = request.POST.get('sport')
    if sport == 0 or sport == '0':
        teams = TeamRegistration.objects.all()
    else:
        teams = TeamRegistration.objects.filter(sport=sport).order_by('-captian__user__date_joined')
    users = UserProfile.objects.all()
    sports = ['All', 'Athletics', 'Badminton', 'Basketball', 'Cricket', 'Football',
              'Table Tenis', 'Lawn Tenis', 'Volleyball','Kabaddi','Hockey','Squash',
              'Chess','BGMI','Valorant','Clash Royale']
    members = {}
    for team in teams:
        member = []
        for user in users:
            if user.teamId == team:
                member.append(user.user.first_name)
        members[team.teamId] = (len(member))
    return render(request, 'adminportal/dashboardTeams.html', {'teams': teams, 'users': users, 'members': members, 'sports': sports, 'sport_select': sport})


def updateScore(request, sport=0):
    if not request.user.is_superuser:
        return render(request, "404")
    if sport == 0 or sport == '0':
        teams = TeamRegistration.objects.all()
    else:
        teams = TeamRegistration.objects.filter(sport=sport)
    sports = ['All', 'Athletics', 'Badminton', 'Basketball', 'Cricket', 'Football',
              'Table Tennis', 'Lawn Tennis', 'Volleyball', 'Kabaddi', 'Hockey', 'Squash',
              'Chess', 'BGMI', 'Valorant', 'Clash Royale']
    if request.method == 'POST':
        teamId = request.POST.get('teamId')
        team = TeamRegistration.objects.get(teamId=teamId)
        team.score = request.POST.get('score')
        team.save()
    return render(request, 'adminportal/updateScore.html', {'teams': teams, 'sports': sports})


# def updateCricketScore():
#     match = Match.objects.all().filter(event='5')
#     if request.method == 'POST':
#         matchCric = Match.objects.get(event_id = request.POST.get('matchId'))
#         matchCric.winner = request.POST.get('winner')
#         cric = Cricket.objects.all.filter(match=matchCric)
#         cric.run1 = request.POST.get('run1')
#         cric.run2 = request.POST.get('run2')
#         cric.wicket1 = request.POST.get('wicket1')
#         cric.wicket2 = request.POST.get('wicket2')
#         cric.save()
#     return render(request, 'adminportal/CricketScore.html', {'matchs': match})


# @login_required(login_url='login')
# def dashboardEsportsTeams(request, sport=0):
#     if not request.user.is_superuser:
#         return render(request, "404")
#     if request.method == 'POST':
#         sport = request.POST.get('sport')
#     if sport == 0 or sport == '0':
#         teams = EsportsTeamRegistration.objects.all().order_by('-captian__user__date_joined')
#     elif sport == '4':
#         teams = EsportsTeamRegistration.objects.all().exclude(college__iexact='IITJ').exclude(
#             college__iexact='IIT Jodhpur').order_by('-captian__user__date_joined')
#     else:
#         teams = EsportsTeamRegistration.objects.filter(sport=sport).order_by('-captian__user__date_joined')
#     users = EsportsUserProfile.objects.all()
#     sports = ['All', 'Valorant', 'BGMI', 'Chess', 'Exclude IITJ']
#     members = {}
#     for team in teams:
#         member = [team.captian.team_member2, team.captian.team_member3,
#                   team.captian.team_member4, team.captian.team_member5, team.captian.team_member6]
#         lenmember = 0
#         for i in member:
#             if (i != None):
#                 lenmember += 1
#         members[team.teamId] = lenmember + 1
#     return render(request, 'adminportal/dashboardEsportsTeams.html', {'teams': teams, 'users': users, 'members': members, 'sports': sports, 'sport_select': sport})


@login_required(login_url='login')
def dashboardUsers(request):
    if not request.user.is_superuser:
        return render(request, "404")
    users = UserProfile.objects.all().order_by('-user__date_joined')
    return render(request, 'adminportal/dashboardUsers.html', {'users': users})

@login_required(login_url='login')
def downloadExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Varchas.xls"'
    wb = xlwt.Workbook(encoding='utf-8')

    ws = wb.add_sheet("Teams")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['TeamID', 'Sport', 'Category','Sub Event', 'Captain', 'Captain no.', 'College','Members']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    teams = TeamRegistration.objects.all().order_by('-captian__user__date_joined')
    users = UserProfile.objects.all()
    for team in teams:
        if team.captian != None:
            team_members = []
            for user in users:
                if user.teamId.filter(teamId=team.teamId).exists():
                    team_members.append(user.user.first_name)
            team_members_str = ', '.join(team_members) if team_members else ""
            members = team_members_str
            row_num = row_num + 1
            ws.write(row_num, 0, team.teamId, font_style)
            ws.write(row_num, 1, team.get_sport_display(), font_style)
            ws.write(row_num, 2, team.category, font_style)
            ws.write(row_num, 3, team.teams, font_style)
            ws.write(row_num, 4, team.captian.user.first_name, font_style)
            ws.write(row_num, 5, team.captian.phone, font_style)
            ws.write(row_num, 6, team.college, font_style)
            ws.write(row_num, 7, members, font_style)

    ws = wb.add_sheet("Users")
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Email', 'Name', 'Phone Number', 'Gender', 'College', 'teamId', 'Accomodation']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    users = UserProfile.objects.all().order_by('-user__date_joined')
    for user in users:
        row_num = row_num + 1
        ws.write(row_num, 0, user.user.email, font_style)
        ws.write(row_num, 1, user.user.first_name+" "+user.user.last_name, font_style)
        ws.write(row_num, 2, user.phone, font_style)
        ws.write(row_num, 3, user.gender, font_style)
        ws.write(row_num, 4, user.college, font_style)
        team_ids = [team.teamId for team in user.teamId.all()] if user.teamId.exists() else []
        team_ids_str = ', '.join(team_ids) if team_ids else ""
        ws.write(row_num, 5, team_ids_str, font_style)
        ws.write(row_num, 7, user.accommodation_required, font_style)
    wb.save(response)
    return response


# @login_required(login_url='login')
# def downloadEsportsExcel(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="Varchas.xls"'
#     wb = xlwt.Workbook(encoding='utf-8')

#     ws = wb.add_sheet("Teams")
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['TeamID', 'Sport', 'Captain', 'Captain no.', 'College',
#                'Members', 'Created on', 'Members Rank', 'Members Ingame Id']
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#     font_style = xlwt.XFStyle()
#     teams = EsportsTeamRegistration.objects.all().order_by('-captian__user__date_joined')
#     users = EsportsUserProfile.objects.all()
#     for team in teams:
#         if team.captian != None:
#             members = []
#             membersRank = []
#             membersId = []
#             if team.captian.team_member2 != None:
#                 members.append(team.captian.team_member2)
#                 if team.captian.team_member2_rank != None:
#                     membersRank.append(team.captian.team_member2_rank)
#                 if team.captian.team_member2_ingame_id != None:
#                     membersId.append(team.captian.team_member2_ingame_id)
#             if team.captian.team_member3 != None:
#                 members.append(team.captian.team_member3)
#                 if team.captian.team_member3_rank != None:
#                     membersRank.append(team.captian.team_member3_rank)
#                 if team.captian.team_member3_ingame_id != None:
#                     membersId.append(team.captian.team_member3_ingame_id)
#             if team.captian.team_member4 != None:
#                 members.append(team.captian.team_member4)
#                 if team.captian.team_member4_rank != None:
#                     membersRank.append(team.captian.team_member4_rank)
#                 if team.captian.team_member4_ingame_id != None:
#                     membersId.append(team.captian.team_member4_ingame_id)
#             if team.captian.team_member5 != None:
#                 members.append(team.captian.team_member5)
#                 if team.captian.team_member5_rank != None:
#                     membersRank.append(team.captian.team_member5_rank)
#                 if team.captian.team_member5_ingame_id != None:
#                     membersId.append(team.captian.team_member5_ingame_id)
#             if team.captian.team_member6 != None:
#                 members.append(team.captian.team_member6)
#                 if team.captian.team_member6_rank != None:
#                     membersRank.append(team.captian.team_member6_rank)
#                 if team.captian.team_member6_ingame_id != None:
#                     membersId.append(team.captian.team_member6_ingame_id)
#             row_num = row_num + 1
#             ws.write(row_num, 0, team.teamId, font_style)
#             ws.write(row_num, 1, team.get_sport_display(), font_style)
#             ws.write(row_num, 2, team.captian.user.first_name, font_style)
#             ws.write(row_num, 3, team.captian.phone, font_style)
#             ws.write(row_num, 4, team.college, font_style)
#             ws.write(row_num, 5, ", ".join(members), font_style)
#             ws.write(row_num, 6, str(team.captian.user.date_joined)[:11])
#             ws.write(row_num, 7, ", ".join(membersRank), font_style)
#             ws.write(row_num, 8, ", ".join(membersId), font_style)

#     ws = wb.add_sheet("Users")
#     row_num = 0
#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True
#     columns = ['Email', 'Name', 'Phone Number', 'Gender', 'College', 'teamId', 'Date Joined']
#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)
#     font_style = xlwt.XFStyle()
#     users = EsportsUserProfile.objects.all().order_by('-user__date_joined')
#     for user in users:
#         row_num = row_num + 1
#         ws.write(row_num, 0, user.user.email, font_style)
#         ws.write(row_num, 1, user.user.first_name+" "+user.user.last_name, font_style)
#         ws.write(row_num, 2, user.phone, font_style)
#         ws.write(row_num, 3, user.gender, font_style)
#         ws.write(row_num, 4, user.college, font_style)
#         ws.write(row_num, 5, user.teamId.teamId if user.teamId != None else "", font_style)
#         ws.write(row_num, 7, str(user.user.date_joined)[:11])

#     wb.save(response)
#     return response


class sendMail(CreateView):
    form_class = EmailForm
    template_name = 'adminportal/email.html'
    success_url = '/admin'

    def form_valid(self, form):
        data = self.request.POST.copy()
        recipient = []
        if int(data['recipient']) < 10:
            teams = TeamRegistration.objects.all()
            for team in teams:
                if int(team.sport) == int(data['recipient']):
                    recipient.append(team.captian.user.email)
        elif int(data['recipient']) == 10:
            teams = TeamRegistration.objects.all()
            for team in teams:
                if team.captian:
                    message = '''<!DOCTYPE html> <html><body><p>{}</p>
                              <h3>{}</h3></body></html>'''.format(data['message'], "Your Team ID:" + team.teamId)
                    send_mail(data['subject'], message, 'noreply@varchas22.in',
                              [team.captian.user.email], fail_silently=False, html_message=message)
            return super(sendMail, self).form_valid(form)
        else:
            users = UserProfile.objects.all()
            for user in users:
                recipient.append(user.user.email)
                message = '''<!DOCTYPE html> <html><body>Hi {}!<br><p>{}</p>
                             <p>Team Varchas</p></body></html>'''.format(user.user.first_name, data['message'])
                send_mail(data['subject'], message, 'noreply@varchas22.in',
                          [user.user.email], fail_silently=False, html_message=message)
            return super(sendMail, self).form_valid(form)
        send_mail(data['subject'], data['message'], 'noreply@varchas22.in', recipient, fail_silently=False)
        return super(sendMail, self).form_valid(form)
