from django.contrib import admin
from .models import UserProfile,PasswordResetRequest


class UserProfileAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile

class OTPAdmin(admin.ModelAdmin):
    class Meta:
        model=PasswordResetRequest

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PasswordResetRequest,OTPAdmin)