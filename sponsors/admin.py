from django.contrib import admin
from .models import SponsorType, Sponsor


class SponsorInline(admin.StackedInline):
    model = Sponsor
    can_delete = True
    verbose_name_plural = 'Sponsor'


class SponsorAdmin(admin.ModelAdmin):
    inlines = (SponsorInline,)
    list_display = ('__str__', 'order',)

    class Meta:
        model = SponsorType


admin.site.register(SponsorType, SponsorAdmin)
