# profiles / views.py

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
    
    def perform_update(self, serializer):
        """Override to add debugging for image uploads during profile updates"""
        # Debug logging for file uploads
        print("\n==== PROFILE UPDATE DEBUG ====")
        print(f"Request method: {self.request.method}")
        print(f"Request content type: {self.request.content_type}")
        print(f"Request FILES: {self.request.FILES}")
        if 'avatar' in self.request.FILES:
            print(f"Avatar file found: {self.request.FILES['avatar'].name}, size: {self.request.FILES['avatar'].size} bytes")
        else:
            print("No avatar file in update request")
            if 'avatar' in self.request.data:
                print(f"Avatar in request.data: {type(self.request.data['avatar'])}")
        print("===========================\n")
            
        # Save the profile
        profile = serializer.save()
        
        # Log the result
        print(f"Profile updated: {profile.id}, avatar: {profile.avatar}")
        return profile