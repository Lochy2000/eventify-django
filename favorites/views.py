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
    serializer_class = FavoriteSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['event', 'owner', 'owner__username']
    ordering_fields = ['created_at']

    def get_queryset(self):
        """
        Return all favorites, but filter by owner if 'owner' parameter is present
        This ensures that favorites are user-specific
        """
        queryset = Favorite.objects.all()
        
        # If we're not in a list/filter context, return the basic queryset
        if not self.request or not self.request.query_params:
            return queryset
            
        # If user is filtering by 'favorite=true', only show their own favorites
        if self.request.query_params.get('favorite') == 'true':
            return queryset.filter(owner=self.request.user)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class FavoriteDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a favorite or remove it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
