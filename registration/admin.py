from django.contrib import admin
from .models import TeamRegistration


class TeamAdmin(admin.ModelAdmin):
    class Meta:
        model = TeamRegistration




admin.site.register(TeamRegistration, TeamAdmin)
