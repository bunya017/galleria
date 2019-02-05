from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationTest(APITestCase):
	def setUp(self):
		User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
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

	