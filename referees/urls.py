from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RefereeViewSet

# -------------------------------------------------------------------
# DefaultRouter() automatically creates all standard REST API routes
# for our RefereeViewSet (list, create, retrieve, update, delete).
#
# Example routes it generates:
#   GET     /referees/          → list of referees
#   POST    /referees/          → create a new referee
#   GET     /referees/{id}/     → get one referee by ID
#   PUT     /referees/{id}/     → update (replace) a referee
#   PATCH   /referees/{id}/     → partially update a referee
#   DELETE  /referees/{id}/     → delete a referee
# -------------------------------------------------------------------

# Create a router instance
router = DefaultRouter()

# Register the RefereeViewSet with the router
# 'referees' → the base URL prefix
# 'basename' → used to generate route names like 'referee-list' and 'referee-detail'
router.register(r'', RefereeViewSet, basename='referee')

# Include all the automatically generated URLs from the router
urlpatterns = [
    path('', include(router.urls)),
]

# -------------------------------------------------------------------
# Final URL behavior summary:
#   /referees/           → Handles GET (list) and POST (create)
#   /referees/<id>/      → Handles GET, PUT, PATCH, DELETE for a single referee
# 
# You don't need to manually define each route — DRF does it automatically
# using the router + ModelViewSet combo in your views.py.
# -------------------------------------------------------------------
