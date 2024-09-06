from django.contrib import admin
from app_apis.models import Matches, Sponsor, InformalEvent, ScoreLinks


admin.site.register(Matches)
admin.site.register(Sponsor)
admin.site.register(InformalEvent)
admin.site.register(ScoreLinks)
