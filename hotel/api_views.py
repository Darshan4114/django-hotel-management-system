from .models import Room
from .serializers import RoomSerializer

from rest_framework import viewsets

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
