from django.contrib.auth.models import User
from .models import Profile
from .views import ProfileList
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class ProfileTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password = 'testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password = 'testpass123')

    def test_profile_created_on_user_creation(self):
        """Test that a profile is created when a user is created"""
        self.assertTrue(Profile.objects.filter(owner=self.user).exists())

    def test_list_profiles(self):
        """Test retrieving a list of profiles"""
        url = reverse('profile-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_profile(self):
        """Test retrieving a specific profile"""
        url = reverse('profile-details', kwargs={'pk': self.user.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')

    def test_update_own_profile(self):
        """Test updating own profile"""
        self.client.force_authenticate(user=self.user)
        url = reverse('profile-details', kwargs={'pk': self.user.profile.pk})
        data = {'name': 'Updated Name', 'bio': 'Updated bio'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Name')

    def test_cannot_update_other_profile(self):
        """Test user cannot update another user's profile"""
        self.client.force_authenticate(user=self.user)
        url = reverse('profile-details', kwargs={'pk': self.user2.profile.pk})
        data = {'name': 'Updated Name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)