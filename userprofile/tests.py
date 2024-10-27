from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from userprofile.models import Profile, Status
from django.test.client import Client

class UserProfileTestCase(TestCase):

    def setUp(self):
        # Create a test user and associated profile
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.profile = Profile.objects.create(user=self.user, bio="Test bio", location="Test Location")
        self.client = Client()

    def test_profile_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Access the profile view for the test user
        url = reverse('userprofile:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)

        # Check that the profile view returns a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check if the response contains the user's bio and location
        self.assertContains(response, self.profile.bio)
        self.assertContains(response, self.profile.location)

    def test_update_profile_ajax(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Send a POST request to update the profile using AJAX
        url = reverse('userprofile:update_profile_ajax', kwargs={'username': self.user.username})
        response = self.client.post(url, {
            'bio': 'Updated Bio',
            'location': 'Updated Location',
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # Check if the update was successful
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"message": "UPDATED"')

        # Refresh the profile instance and verify the changes
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.bio, 'Updated Bio')
        self.assertEqual(self.profile.location, 'Updated Location')

    def test_status_json_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a status for the user
        Status.objects.create(user=self.user, title="Test Status", description="This is a test status")

        # Access the status_json view for the test user
        url = reverse('userprofile:status_json', kwargs={'username': self.user.username})
        response = self.client.get(url)

        # Check if the response is JSON and contains the created status
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Status')
        self.assertContains(response, 'This is a test status')

    def test_private_profile(self):
        # Set the user's profile to private
        self.profile.private = True
        self.profile.save()

        # Log in as another user and attempt to access the private profile
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.login(username='otheruser', password='otherpassword')

        url = reverse('userprofile:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)

        # Check that the user is informed the profile is private
        self.assertContains(response, "This user's profile is private.")
        self.assertNotContains(response, self.profile.bio)  # Ensure the bio is not shown
