# events/views.py
from django.db.models import Count
from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer
from eventify.permissions import IsOwnerOrReadOnly

class EventList(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )
    search_fields = ['title', 'owner__username', 'category']
    ordering_fields = ['date', 'likes_count', 'comments_count']
    filterset_fields = ['category', 'owner__profile']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )