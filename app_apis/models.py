from django.db import models
from registration.models import TeamRegistration


class MatchManager(models.Manager):
    def create_match(self, team1, college1, team2, college2, venue, event, date, time):
        match = self.create(team1=team1, college1=college1, team2=team2, college2=college2,
                            venue=venue, event=event, date=date, time=time)
        return match


class Matches(models.Model):
    VENUE_CHOICES = (
        ('1', 'IITJ Football Ground'),
        ('2', 'Volleyball Ground'),
        ('3', 'Tennis Ground'),
        ('4', 'Indoor sports Complex'),
        ('5', 'Lecture Hall Complex'),
        ('6', 'Spartan Cricket Ground'),
        ('7', 'Pathan Cricket Academy'),
        ('8', 'VIRU Cricket Academmy'),
        ('9', 'L S Sankhla Sports Academy'),
    )
    EVENT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Chess'),
        ('5', 'Cricket'),
        ('6', 'Football'),
        ('7', 'Table Tenins'),
        ('8', 'Tennis'),
        ('9', 'Volleyball'),
        ('10', 'Badminton-Mixed doubles'),
        ('11', 'Kabaddi'),
        ('12', 'Squash'),
        ('13', 'Weightlifting'),
    )
    team1 = models.ForeignKey(TeamRegistration, on_delete=models.CASCADE, related_name="team_one")
    college1 = models.CharField(max_length=128, default="")
    team2 = models.ForeignKey(TeamRegistration, on_delete=models.CASCADE, related_name="team_two")
    college2 = models.CharField(max_length=128, default="")
    venue = models.CharField(max_length=3, choices=VENUE_CHOICES)
    event = models.CharField(max_length=2, choices=EVENT_CHOICES)
    # event = models.CharField(max_length=128)
    # venue = models.CharField(max_length=128)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)

    objects = MatchManager()

    def __str__(self):
        return str(self.date)+" "+str(self.time)+" "+self.college1+" v/s " + self.college2


class Sponsor(models.Model):
    name = models.CharField(max_length=128)
    logo = models.ImageField(upload_to='sponsor')
    # sponsor_type = models.CharField(max_length=128)
    link = models.URLField(help_text="Sponsor's website url", null=True, blank=True, default=None)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class InformalEvent(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    venue = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ScoreLinks(models.Model):
    name = models.CharField(max_length=128)
    link = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
