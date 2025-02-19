from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from eventify.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer