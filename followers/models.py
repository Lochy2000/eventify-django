# followers/models.py
from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model):
    """
    Follower model to track relationships between users.
    'owner' follows 'followed'
    """
    owner = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User,
        related_name='followed',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f'{self.owner} follows {self.followed}'