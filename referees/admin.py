from django.contrib import admin
from .models import Referee

# -------------------------------------------------------------------
# RefereeAdmin allows you to manage Referee objects from the Django admin panel.
# You can customize the display, search, filters, and more.
# -------------------------------------------------------------------
class RefereeAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('id', 'name', 'email', 'phone', 'sport', 'created_at')
    
    # Fields that can be searched using the search bar
    search_fields = ('name', 'email', 'sport', 'phone')
    
    # Filters to appear on the right-hand sidebar in admin
    list_filter = ('sport', 'created_at')
    
    # Automatically populate 'created_at' and 'updated_at' as read-only
    readonly_fields = ('created_at', 'updated_at')
    
    class Meta:
        model = Referee

# Register Referee with the admin site
admin.site.register(Referee, RefereeAdmin)
