from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Catalog



class CatalogListTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.user1 = User.objects.create_user('testUser1', 'testEmail1@mail.com', 'testPassword')
		self.url = reverse('catalog-list')
		Catalog.objects.create(
			owner=self.user1,
			name='Test Catalogs Inc.',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		self.data = {
			'name': 'Test One Catalogs Inc.',
			'description': 'Catalog description',
			'contact_address': '125 Test Avenue',
			'contact_email': 'testEmail@mail.com',
			'contact_phone': '08011223344',
		}

	def test_create_catalog(self):
		"""
		Test if user can create a new catalog.
		"""
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Catalog.objects.all().count(), 2)

	def test_unauthenticated_create(self):
		"""
		Test if unauthenticated user can create a new catalog
		"""
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(Catalog.objects.all().count(), 1)

	def test_all_blank_fields(self):
		"""
		Test if all fields submitted blank is allowed.
		"""
		data = {
			'name': '',
			'description': '',
			'contact_address': '',
			'contact_email': '',
			'contact_phone': '',
		}
		data_keys_list = list(data.keys())
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, data)
		response_keys_list = list(response.data.keys())
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(data_keys_list, response_keys_list)

	def test_catalog_list_owner(self):
		"""
		Test if request.user is the returned catalogs list owner.
		"""
		self.client.login(username='testUser1', password='testPassword')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data[0]['owner'], 'testUser1')

	def test_blank_name(self):
		"""
		Test if name field submitted blank is allowed.
		"""
		data = {
			'name': '',
			'description': 'Catalog description',
			'contact_address': '125 Test Avenue',
			'contact_email': 'testEmail@mail.com',
			'contact_phone': '08011223344',
		}
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('name', response.data.keys())

	def test_blank_description(self):
		"""
		Test if description field submitted blank is allowed.
		"""
		data = {
			'name': 'Test One Catalogs Inc.',
			'description': '',
			'contact_address': '125 Test Avenue',
			'contact_email': 'testEmail@mail.com',
			'contact_phone': '08011223344',
		}
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('description', response.data.keys())

	def test_blank_contact_address(self):
		"""
		Test if contact address field submitted blank is allowed.
		"""
		data = {
			'name': 'Test One Catalogs Inc.',
			'description': 'Catalog description',
			'contact_address': '',
			'contact_email': 'testEmail@mail.com',
			'contact_phone': '08011223344',
		}
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('contact_address', response.data.keys())

	def test_blank_contact_email(self):
		"""
		Test if contact email field submitted blank is allowed.
		"""
		data = {
			'name': 'Test One Catalogs Inc.',
			'description': 'Catalog description',
			'contact_address': '125 Test Avenue',
			'contact_email': '',
			'contact_phone': '08011223344',
		}
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('contact_email', response.data.keys())

	def test_blank_contact_phone(self):
		"""
		Test if contact phone field submitted blank is allowed.
		"""
		data = {
			'name': 'Test One Catalogs Inc.',
			'description': 'Catalog description',
			'contact_address': '125 Test Avenue',
			'contact_email': 'testEmail@mail.com',
			'contact_phone': '',
		}
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn('contact_phone', response.data.keys())


class CatalogDetailTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.catalog = Catalog.objects.create(
			owner=self.user,
			name='Test Catalogs Inc',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		self.data = self.catalog.slug
		self.url = reverse('catalog-detail', args=[self.data])

	def test_authenticated_user_can_retrieve(self):
		"""
		Test if authenticated user can retrieve CatalogDetail.
		"""
		self.client.login(username='testUser', password='testPassword')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn(self.data, response.data['url'])

	def test_unauthenticated_user_can_retrieve(self):
		"""
		Test if unauthenticated user can retrieve CatalogDetail.
		"""
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn(self.data, response.data['url'])