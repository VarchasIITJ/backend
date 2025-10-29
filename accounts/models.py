from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from django.utils import timezone

class PasswordResetRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120)
    otp = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    expiration_time = models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return self.user.email

    def save(self, *args, **kwargs):
        now = timezone.now()
        self.expiration_time = now + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    ACCOMMODATION_CHOICES = (
        ('N', 'No'),
        ('Y', 'Yes'),
    )
    ACCOMMODATION_PAID = (
        ('1', 'Not Paid'),
        ('2', 'Paid'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Other'),
    )
    DAYS_CHOICES = (
        ('1', 'One'),
        ('2', 'Two'),
        ('3', 'Three'),
        ('4', 'Four'),
    )
    STATE_CHOICES = (
        ('1', 'Andhra Pradesh'),
        ('2', 'Arunachal Pradesh'),
        ('3', 'Assam'),
        ('4', 'Bihar'),
        ('5', 'Chhattisgarh'),
        ('6', 'Goa'),
        ('7', 'Gujarat'),
        ('8', 'Haryana'),
        ('9', 'Himachal Pradesh'),
        ('10', 'Jammu & Kashmir'),
        ('11', 'Jharkhand'),
        ('12', 'Karnataka'),
        ('13', 'Kerala'),
        ('14', 'Madhya Pradesh'),
        ('15', 'Maharashtra'),
        ('16', 'Manipur'),
        ('17', 'Meghalaya'),
        ('18', 'Mizoram'),
        ('19', 'Nagaland'),
        ('20', 'Odisha'),
        ('21', 'Punjab'),
        ('22', 'Rajasthan'),
        ('23', 'Sikkim'),
        ('24', 'Tamil Nadu'),
        ('25', 'Telangana'),
        ('26', 'Tripura'),
        ('27', 'Uttarakhand'),
        ('28', 'Uttar Pradesh'),
        ('29', 'West Bengal'),
        ('30', 'Andaman & Nicobar Islands'),
        ('31', 'Delhi'),
        ('32', 'Chandigarh'),
        ('33', 'Dadra & Naagar Haveli'),
        ('34', 'Daman & Diu'),
        ('35', 'Lakshadweep'),
        ('36', 'Puducherry'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uniqueId = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=11, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    college = models.CharField(max_length=128, blank=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES, blank=True)

    account_holder_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=11)
    bank_account_number = models.CharField(max_length=20)
    
    accommodation_required = models.CharField(max_length=1, choices=ACCOMMODATION_CHOICES, blank=True)
    accommodation_paid = models.CharField(max_length=1, choices=ACCOMMODATION_PAID, blank=True, default='1')
    amount_required = models.PositiveSmallIntegerField(default=0, blank=True)
    amount_paid = models.PositiveSmallIntegerField(default=0, blank=True)
    no_of_days = models.CharField(max_length=1, choices=DAYS_CHOICES,blank=True)
    id_issued = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_code', blank=True, null=True)
    teamId = models.ManyToManyField("registration.TeamRegistration", blank=True, related_name="member",) 
    isesports=models.BooleanField(default=False)
    team_member1_cr_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member1_bgmi_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member2_bgmi_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member3_bgmi_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member4_bgmi_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member1_val_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member2_val_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member3_val_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member4_val_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    team_member5_val_ingame_id = models.CharField(max_length=128, blank=True, null=True)
    def __str__(self):
        return self.user.username

