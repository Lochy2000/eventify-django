# favorites/models.py
from django.db import models
from django.contrib.auth.models import User
from events.models import Event

class Favorite(models.Model):
    """
    Favorite model to allow users to save events.
    A user can favorite an event only once.
    """
    owner = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE
    )
    event = models.ForeignKey(
        Event,
        related_name='favorited_by',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'event']

    def __str__(self):
        return f'{self.owner} favorited {self.event}'