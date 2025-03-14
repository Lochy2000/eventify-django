#events/models.py

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.files.uploadedfile import InMemoryUploadedFile

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('tech', 'Technology'),
        ('sports', 'Sports'),
        ('arts', 'Arts'),
        ('food', 'Food'),
        ('outdoors', 'Outdoors'),
        ('other', 'Other'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    cover = CloudinaryField(
        'event_image', 
        folder='events', 
        blank=True, 
        null=True,
        format='jpg',
        use_filename=True,
        transformation={
            'width': 800,
            'height': 600,
            'crop': 'fill'
        }
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} by {self.owner}"


# Add a signal to debug Cloudinary uploads
@receiver(pre_save, sender=Event)
def log_cloudinary_upload(sender, instance, **kwargs):
    """Log Cloudinary upload attempt for debugging"""
    print(f"\n==== CLOUDINARY DEBUG ====")
    print(f"Event being saved: {instance.title}")
    print(f"Current cover value: {instance.cover}")
    
    # Check if this is a file upload
    if hasattr(instance.cover, 'file') and isinstance(instance.cover.file, InMemoryUploadedFile):
        print(f"File detected: {instance.cover.name}, size: {instance.cover.size} bytes")
        try:
            # Force CloudinaryField to process the file
            print("Attempting to process file...")
            # Get resource type (required for Cloudinary to process)
            resource_type = getattr(instance.cover, 'resource_type', 'image')
            print(f"Resource type: {resource_type}")
        except Exception as e:
            print(f"ERROR processing file: {str(e)}")
    else:
        print("No file attached or file already processed")
    
    print("===========================\n")


# Model to track event attendance/registration
class EventAttendee(models.Model):
    """
    Allows users to register for events.
    Links users to events they plan to attend.
    Ensures a user can only register once for a given event.
    """
    owner = models.ForeignKey(
        User,
        related_name='attending',
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        related_name='attendees',
        on_delete=models.CASCADE
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-registered_at']
        unique_together = ['owner', 'event']  # Prevents duplicate registrations

    def __str__(self):
        return f'{self.owner} attending {self.event}'