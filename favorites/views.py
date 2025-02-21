# favorites/views.py
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from eventify.permissions import IsOwnerOrReadOnly
from .models import Favorite
from .serializers import FavoriteSerializer

class FavoriteList(generics.ListCreateAPIView):
    """
    List favorites or create a favorite if logged in.
    Can filter by event and owner.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['event', 'owner']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FavoriteDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a favorite or remove it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
