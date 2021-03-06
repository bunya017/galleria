from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import UserProfile


class UserRegistrationTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.url = reverse('user-registration')

	def test_user_registration(self):
		"""
		Test user can register.
		"""
		data = {
			'username': 'testUser1',
			'email': 'testEmail.One@mail.com',
			'password': 'testPassword'
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(User.objects.all().count(), 2)
		# Make sure auth token is returned as response.
		self.assertNotEqual(response.data['token'], '')
		# Make sure user profile is created upon registration.
		self.assertTrue(
			UserProfile.objects.filter(user__username=data['username']).exists()
		)

	def test_unique_username(self):
		"""
		Test if an existing username can be used.
		"""
		data = {
			'username': 'testUser',
			'email': 'testEmail.One@mail.com',
			'password': 'testPassword'
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_unique_email(self):
		"""
		Test if an existing email can be used.
		"""
		data = {
			'username': 'testUser1',
			'email': 'testEmail@mail.com',
			'password': 'testPassword'
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_blank_username(self):
		"""
		Test if username field can be submitted blank.
		"""
		data = {
			'username': '',
			'email': 'testEmail.One@mail.com',
			'password': 'testPassword'
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_blank_email(self):
		"""
		Test if email field can be submitted blank.
		"""
		data = {
			'username': 'testUser1',
			'email': '',
			'password': 'testPassword'
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_blank_password(self):
		"""
		Test if password field can be submitted blank.
		"""
		data = {
			'username': 'testUser1',
			'email': 'testEmail.One@mail.com',
			'password': ''
		}
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.url = reverse('token-auth')
		self.data = {
			'username': 'testUser',
			'password': 'testPassword'
		}

	def test_fetch_auth_token(self):
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertNotEqual(response.data['token'], '')