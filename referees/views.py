from rest_framework import viewsets, permissions
from .models import Referee
from .serializers import RefereeSerializer, RefereeCreateSerializer

# -------------------------------------------------------------------
# RefereeViewSet is the main class that handles all CRUD operations
# (Create, Read, Update, Delete) for the Referee model.
#
# Because we’re using ModelViewSet (provided by Django REST Framework),
# we automatically get the following methods:
#
#   list()          → GET    /referees/           → return all referees
#   retrieve()      → GET    /referees/<id>/      → return one referee
#   create()        → POST   /referees/           → create new referee
#   update()        → PUT    /referees/<id>/      → replace a referee
#   partial_update()→ PATCH  /referees/<id>/      → update some fields
#   destroy()       → DELETE /referees/<id>/      → delete referee
#
# The DefaultRouter in urls.py automatically maps all these routes.
# -------------------------------------------------------------------

class RefereeViewSet(viewsets.ModelViewSet):
    # Queryset defines which data this ViewSet operates on.
    # Here, we’re working with all referees, newest first.
    queryset = Referee.objects.all().order_by('-created_at')

    # Define which users can access this API.
    # You can use:
    #   - permissions.AllowAny      → no login required
    #   - permissions.IsAuthenticated → login required
    #   - permissions.IsAdminUser   → only admins
    # permission_classes = [permissions.IsAuthenticated]

    # ----------------------------------------------------------------
    # get_serializer_class() dynamically decides which serializer to use
    #
    # - When creating a referee (POST), use RefereeCreateSerializer
    #   → This serializer is simpler and expects a 'user' field (foreign key).
    #
    # - For all other actions (GET, PUT, PATCH, DELETE),
    #   use RefereeSerializer (the detailed one that includes user info).
    # ----------------------------------------------------------------
    def get_serializer_class(self):
        if self.action == 'create':
            return RefereeCreateSerializer
        return RefereeSerializer
