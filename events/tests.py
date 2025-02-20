from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Event, Like, Comment
from datetime import datetime, timedelta

class EventTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        
        # Create a test event
        self.event = Event.objects.create(
            owner=self.user,
            title='Test Event',
            description='Test Description',
            date=timezone.now() + timedelta(days=7),
            location='Test Location',
            category='tech',
            price=10.00
        )

    def test_create_event(self):
        """Test creating a new event"""
        self.client.force_authenticate(user=self.user)
        url = reverse('event-list')
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'date': (timezone.now() + timedelta(days=7)).isoformat(),
            'location': 'New Location',
            'category': 'music',
            'price': 15.00
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 2)
        self.assertEqual(Event.objects.latest('created_at').title, 'New Event')

    def test_list_events(self):
        """Test retrieving a list of events"""
        url = reverse('event-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_event_detail(self):
        """Test retrieving a specific event"""
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Event')

    def test_update_event(self):
        """Test updating an event by owner"""
        self.client.force_authenticate(user=self.user)
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        data = {'title': 'Updated Event Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Event Title')

    def test_cannot_update_other_user_event(self):
        """Test user cannot update another user's event"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('event-detail', kwargs={'pk': self.event.pk})
        data = {'title': 'Updated Event Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            owner=self.user,
            title='Test Event',
            description='Test Description',
            date=timezone.now() + timedelta(days=7),
            location='Test Location',
            category='tech',
            price=10.00
        )
        self.comment = Comment.objects.create(
            owner=self.user,
            event=self.event,
            content='Test comment'
        )

    def test_create_comment(self):
        """Test creating a comment on an event"""
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-list', kwargs={'event_pk': self.event.pk})
        data = {'content': 'New comment', 'event': self.event.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_list_comments(self):
        """Test retrieving comments for an event"""
        url = reverse('comment-list', kwargs={'event_pk': self.event.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class LikeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            owner=self.user,
            title='Test Event',
            description='Test Description',
            date=timezone.now() + timedelta(days=7),
            location='Test Location',
            category='tech',
            price=10.00
        )

    def test_create_like(self):
        """Test creating a like on an event"""
        self.client.force_authenticate(user=self.user)
        url = reverse('like-create', kwargs={'pk': self.event.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_remove_like(self):
        """Test removing a like from an event"""
        like = Like.objects.create(owner=self.user, event=self.event)
        self.client.force_authenticate(user=self.user)
        url = reverse('like-destroy', kwargs={'pk': like.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(), 0)

    def test_duplicate_like(self):
        """Test that a user cannot like an event twice"""
        self.client.force_authenticate(user=self.user)
        url = reverse('like-create', kwargs={'pk': self.event.pk})
        # First like
        self.client.post(url)
        # Try to like again
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)