from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    avatar = CloudinaryField(
        'avatar',
        folder='profiles',
        blank=True,
        null=True,
        default='default_profile_ju9xum',
        # Explicitly set the resource type to auto so it can handle different file types
        resource_type='auto',
        # Make sure transformation works
        transformation={
            'crop': 'fill',
            'width': 400,
            'height': 400
        }
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"
    
    def save(self, *args, **kwargs):
        """Override save method to handle Cloudinary avatar field"""
        try:
            # Call parent save method
            super().save(*args, **kwargs)
        except Exception as e:
            # If error is related to Cloudinary, try to save without the image
            if 'avatar' in str(e).lower() or 'cloudinary' in str(e).lower():
                # Set avatar to default value
                self.avatar = None
                # Try saving again without triggering this custom save method
                super(Profile, self).save(*args, **kwargs)
            else:
                # Re-raise other errors
                raise

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)