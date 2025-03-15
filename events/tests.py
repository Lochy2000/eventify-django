#events/testing.py

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Event
from likes.models import Like
from comments.models import Comment
from datetime import datetime, timedelta
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import cloudinary.uploader
from PIL import Image

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


class CloudinaryUploadTest(APITestCase):
    """Test Cloudinary image upload functionality"""
    
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create a small test image file
        self.image_file = self._create_test_image()
    
    def _create_test_image(self):
        # Create a temporary image file for testing
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            # Create a small test image using PIL
            image = Image.new('RGB', (100, 100), color='red')
            image.save(temp_file, format='JPEG')
            temp_file.flush()
            return temp_file.name
    
    def tearDown(self):
        # Clean up the temporary file
        if hasattr(self, 'image_file') and os.path.exists(self.image_file):
            os.unlink(self.image_file)
    
    def test_event_with_image(self):
        """Test creating an event with an image"""
        # Skip test if Cloudinary credentials are not set
        if not all([os.environ.get('CLOUDINARY_CLOUD_NAME'),
                  os.environ.get('CLOUDINARY_API_KEY'),
                  os.environ.get('CLOUDINARY_API_SECRET')]):
            self.skipTest("Cloudinary credentials not found in environment")
            return
            
        self.client.force_authenticate(user=self.user)
        url = reverse('event-list')
        
        # Create event data with image
        with open(self.image_file, 'rb') as img:
            image_data = img.read()
        
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_data,
            content_type='image/jpeg'
        )
        
        # Prepare event data
        data = {
            'title': 'Event With Image',
            'description': 'Test Description',
            'date': (timezone.now() + timedelta(days=7)).isoformat(),
            'location': 'Test Location',
            'category': 'tech',
            'price': 15.00,
            'cover': image
        }
        
        # Make API request
        response = self.client.post(url, data=data, format='multipart')
        
        # Verify the event was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verify the image was uploaded to Cloudinary
        event_id = response.data['id']
        event = Event.objects.get(id=event_id)
        
        # Check if the cover field has a value
        self.assertIsNotNone(event.cover, "The cover field should not be None after upload")