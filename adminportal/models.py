from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class AdminProfile(models.Model):
    DEPARTMENT_CHOICES = (
        ('NONE', 'None'),
        ('FLAG', 'Flagship'),
        ('ONL9', 'Online'),
        ('PUBR', 'Public Relations'),
        ('MAR', 'Marketing'),
        ('EVNT', 'Sports Events'),
    )

    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True},
                                verbose_name='username')
    phone = models.CharField(max_length=10, validators=[contact])
    department = models.CharField(choices=DEPARTMENT_CHOICES, default='NONE', max_length=8)

    def __str__(self):
        return self.user.username

    @property
    def name(self):
        return self.user.get_full_name()


class DepartmentTeam(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(AdminProfile, through='DepartmentTeamMembership',
                                     through_fields=('department_team', 'profile'))
    hierarchy = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['hierarchy']

    def __str__(self):
        return self.name


class DepartmentTeamMembership(models.Model):
    department_team = models.ForeignKey(DepartmentTeam, on_delete=models.CASCADE)
    profile = models.ForeignKey(AdminProfile, on_delete=models.CASCADE)
    hierarchy = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['hierarchy']

    def __str__(self):
        return self.profile.name


class email(models.Model):
    RECIPIENT_CHOICES = (
        ('1', 'Athletics'),
        ('2', 'Badminton'),
        ('3', 'Basketball'),
        ('4', 'Chess'),
        ('5', 'Cricket'),
        ('6', 'Football'),
        ('7', 'Table Tenis'),
        ('8', 'Tenis'),
        ('9', 'Volleyball'),
        ('10', 'All Teams'),
        ('11', 'All Users'),
    )
    recipient = models.CharField(max_length=3, choices=RECIPIENT_CHOICES)
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=180)
