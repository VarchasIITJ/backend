from django.db import models
from accounts.models import UserProfile

class TeamRegistration(models.Model):
    SPORT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Cricket'),
        ('5', 'Football'),
        ('6', 'Table Tennis'),
        ('7', 'Lawn Tennis'),
        ('8', 'Volleyball'),    
        ('9', 'Kabaddi'),
        ('10', 'Hockey'),
        ('11', 'Squash'),
        ('12', 'Chess'),
        ('13', 'BGMI'),
        ('14','Valorant'),
        ('15', 'Clash Royale'),
    )
    CATEGORY_CHOICES = (
        ('S', 'Singles'),
        ('M', 'Mens'),
        ('W', 'Womens'),
        ('X', 'Mixed'),
    )
    PAYMENT_CHOICES=(
        ('1', 'Not Paid'),
        ('2','Registration Paid')
    )
    teamId = models.CharField(max_length=25, unique=True, blank=True, null=True)
    sport = models.CharField(max_length=2, choices=SPORT_CHOICES)
    college = models.CharField(max_length=128, blank=True, null=True)
    payment_status=models.CharField(max_length=25,choices=PAYMENT_CHOICES,default='1')
    captain = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    score = models.IntegerField(default=-1)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    team_name = models.CharField(blank=True, null=True,max_length=100)
    teamsize=models.IntegerField(default=1,blank=True,null=True)
    teamcount=models.IntegerField(default=1,blank=True,null=True)
    def __str__(self):
        if (self.teamId == None):
            return "None"
        return self.teamId

class AthleticsSubEvent(models.Model):
    EVENT_CHOICES = (
        ('100m', '100m Race'),
        ('200m', '200m Race'),
        ('400m', '400m Race'),
        ('800m', '800m Race'),
        ('1500m', '1500m Race'),
        ('5000m', '5000m Race'),
        ('Long Jump', 'Long Jump'),
        ('Triple Jump', 'Triple Jump'),
        ('High Jump', 'High Jump'),
        ('Discuss Throw', 'Discuss Throw'),
        ('Javelin Throw', 'Javelin Throw'),
        ('Shot Put', 'Shot Put'),
        ('4x100m', '4x100m Relay'),
        ('4x400m', '4x400m Relay'),
    )

    team = models.ForeignKey(
        TeamRegistration,
        on_delete=models.CASCADE,
        related_name='athletics_events'
    )
    event_name = models.CharField(max_length=50, choices=EVENT_CHOICES)
    score = models.IntegerField(default=-1, blank=True, null=True)

    def __str__(self):
        return f"{self.team.team_name} - {self.event_name}"

