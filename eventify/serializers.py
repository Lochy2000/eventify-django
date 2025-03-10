from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

class CurrentUserSerializer(UserDetailsSerializer):
    profile_id = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile_id', 'profile_image')

    def get_profile_id(self, obj):
        return obj.profile.id if hasattr(obj, 'profile') and obj.profile else None

    def get_profile_image(self, obj):
        if hasattr(obj, 'profile') and obj.profile and getattr(obj.profile, 'image', None):
            return obj.profile.image.url
        return None
