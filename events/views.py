# events/views.py
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Like, Comment
from .serializers import EventSerializer, CommentSerializer
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

    template_name = None 

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    )

class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

class LikeCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)

        # Check if the user has already liked this event
        like, created = Like.objects.get_or_create(owner=request.user, event=event)

        if not created:  # If like already exists, return 400 Bad Request
            return Response({'detail': 'You have already liked this event.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)    

class LikeDestroy(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Like.objects.all()