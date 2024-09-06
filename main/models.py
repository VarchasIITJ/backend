from django.db import models
from django.core.validators import RegexValidator


class OurTeam(models.Model):
    POSITION_CHOICES = (
        (1, 'Festival Chief'),
        (2, 'Finance Head'),
        (3, 'Creativity'),
        (4, 'Informals'),
        (5, 'Marathon'),
        (6, 'Marketing'),
        (7, 'Public Relations and Hospitality'),
        (8, 'Publicity and Media'),
        (9, 'Pronite'),
        (10, 'Resources'),
        (11, 'Security'),
        (12, 'SOCH'),
        (13, 'Sport Coordinator'),
        (14, 'Transport'),
        (15, 'Web and APP'),
        (16, 'Vice President - Board of Student Sports'),
    )
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, validators=[contact])
    position = models.IntegerField(choices=POSITION_CHOICES,default=1)
    picture = models.ImageField(
        upload_to='teamPics/', blank=True, null=True, default="teamPics/default.jpg")
    insta = models.URLField(max_length=100, null=True, blank=True)
    fp = models.URLField(max_length=100, null=True, blank=True)
    linkedIn = models.URLField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['position']

