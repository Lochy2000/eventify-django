from django.db import models
from django.contrib.auth.models import User

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
    cover = models.ImageField(upload_to='events/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} by {self.owner}"
    

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'event']

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
