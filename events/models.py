#events/models.py

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

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
        default='default_post_o0lbny'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} by {self.owner}"
    
    def save(self, *args, **kwargs):
        """Override save method to handle Cloudinary cover field"""
        try:
            # Call parent save method
            super().save(*args, **kwargs)
        except Exception as e:
            # If error is related to Cloudinary, try to save without the image
            if 'cover' in str(e).lower() or 'cloudinary' in str(e).lower():
                # Set cover to default value
                self.cover = None
                # Try saving again without triggering this custom save method
                super(Event, self).save(*args, **kwargs)
            else:
                # Re-raise other errors
                raise


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