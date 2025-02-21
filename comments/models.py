# comments/models.py
from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class Comment(models.Model):
    """
    Comment model, related to User and Event.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, 
        related_name='comments', 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f'{self.owner} commented on {self.event}'
