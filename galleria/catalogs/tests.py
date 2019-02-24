import os
import shutil
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Catalog, Category, ProductEntry, ProductImage
from .utils import generate_photo



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
		self.user1 = User.objects.create_user('testUser1', 'testEmail1@mail.com', 'testPassword1')
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

	def test_non_owner_can_update_catalog(self):
		payload = {
			'name': 'Test1 Catalogs Inc',
			'description': 'Catalog description as edited by user1',
			'contact_address': '126 Test Avenue',
			'contact_email': 'testEmail1@mail.com',
			'contact_phone': '08011223311',
		}
		self.client.login(username='testUser1', password='testPassword1')
		response = self.client.put(self.url, payload)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(Catalog.objects.filter(name=self.catalog.name).count(), 1)
		self.assertEqual(Catalog.objects.filter(name=payload['name']).count(), 0)


class CategoryListTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.user1 = User.objects.create_user('testUser1', 'testEmail1@mail.com', 'testPassword1')
		self.catalog = Catalog.objects.create(
			owner=self.user,
			name='Test Catalogs Inc.',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		slug = self.catalog.slug
		self.url = reverse('category-list', kwargs={'catalog__slug': slug})
		self.data = {
			'name': 'Kids Clothing',
			'catalog': self.catalog.id,
			'description': 'Clothes for kids.',
		}

	def test_autenticated_user_can_create_category(self):
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Category.objects.all().count(), 1)

	def test_unautenticated_user_can_create_category(self):
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(Category.objects.all().count(), 0)

	def test_non_catalog_owner_can_create_category(self):
		self.client.login(username='testUser1', password='testPassword1')
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(Category.objects.all().count(), 0)


class CategoryDetailTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.user1 = User.objects.create_user('testUser1', 'testEmail1@mail.com', 'testPassword1')
		self.catalog = Catalog.objects.create(
			owner=self.user,
			name='Test Catalogs Inc.',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		self.category = Category.objects.create(
			name='Kids Clothing',
			catalog=self.catalog,
			description='Clothes for kids.',
		)
		self.url = reverse('category-detail',
			kwargs={
				'catalog__slug': self.catalog.slug,
				'slug': self.category.slug,
			}
		)

	def test_autenticated_user_can_get_category_details(self):
		self.client.login(username='testUser', password='testPassword')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], self.category.name)

	def test_unautenticated_user_can_get_category_details(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['name'], self.category.name)

	def test_non_catalog_owner_can_update_category(self):
		payload = {
			'name': 'Kids Clothing by user1',
			'catalog': self.catalog,
			'description': 'Clothes for kids by user1.',
		}
		self.client.login(username='testUser1', password='testPassword1')
		response = self.client.put(self.url, payload)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(Category.objects.filter(
			name=self.category.name, catalog=self.catalog).count(), 1)
		self.assertEqual(Category.objects.filter(
			name=payload['name'], catalog=self.catalog).count(), 0)


class ProductEntryListTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.user1 = User.objects.create_user('testUser1', 'testEmail1@mail.com', 'testPassword1')
		self.catalog = Catalog.objects.create(
			owner=self.user,
			name='Test Catalogs Inc.',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		self.category = Category.objects.create(
			name='Kids Clothing',
			catalog=self.catalog,
			description='Clothes for kids.',
		)
		self.url = reverse('productentry-list',
			kwargs={
				'category__catalog__slug': self.catalog.slug,
			}
		)
		self.data = {
			'name': 'Tee Shirt',
			'category': self.category.id,
			'description': 'Blue tee-shirt for kids.',
			'price': 3000,
		}

	def test_autenticated_user_can_create_productEntry(self):
		self.client.login(username='testUser', password='testPassword')
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(ProductEntry.objects.all().count(), 1)

	def test_unautenticated_user_can_create_productEntry(self):
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		self.assertEqual(ProductEntry.objects.all().count(), 0)

	def test_autenticated_user_can_get_productEntry_list(self):
		self.client.login(username='testUser', password='testPassword')
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_unautenticated_user_can_get_productEntry_list(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_non_owner_can_create_productEntry(self):
		self.client.login(username='testUser1', password='testPassword1')
		response = self.client.post(self.url, self.data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		self.assertEqual(ProductEntry.objects.all().count(), 0)


class ProductEntryDetailTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.catalog = Catalog.objects.create(
			owner=self.user,
			name='Test Catalogs Inc.',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		self.category = Category.objects.create(
			name='Kids Clothing',
			catalog=self.catalog,
			description='Clothes for kids.',
		)
		self.product = ProductEntry.objects.create(
			name='Tee Shirt',
			category=self.category,
			description='Blue tee-shirt for kids.',
			price=3000,
			created_by=self.user,
		)
		self.url = reverse('productentry-detail',
			kwargs={
				'category__catalog__slug': self.catalog.slug,
				'slug': self.product.slug,
				'reference_id': self.product.reference_id,
			}
		)

	def test_get_product_entry_detail(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProductImageListTest(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user('testUser', 'testEmail@mail.com', 'testPassword')
		self.catalog = Catalog.objects.create(
			owner=self.user,
			name='Test Catalogs Inc.',
			description='Catalog description',
			contact_address='125 Test Avenue',
			contact_email='testEmail@mail.com',
			contact_phone='08011223344',
		)
		self.category = Category.objects.create(
			name='Kids Clothing',
			catalog=self.catalog,
			description='Clothes for kids.',
		)
		self.product = ProductEntry.objects.create(
			name='Tee Shirt',
			category=self.category,
			description='Blue tee-shirt for kids.',
			price=3000,
			created_by=self.user,
		)
		self.url = reverse('productimage-list',
			kwargs={
				'product__category__catalog__slug': self.product.category.catalog.slug,
				'product__slug': self.product.slug,
				'reference_id': self.product.reference_id,
			}
		)

	def _cleanup(self, path):
		if os.path.isdir(path):
			shutil.rmtree(path)

	def tearDown(self):
		self._cleanup(os.path.join(settings.MEDIA_ROOT, self.catalog.slug))

	def test_add_product_image(self):
		self.client.login(username='testUser', password='testPassword')
		photo_file = generate_photo('test_image')
		data = {
			'product': self.product.id,
			'title': 'tee-shirt-blue-001',
			'photo': photo_file,
		}
		response = self.client.post(self.url, data, format='multipart')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(ProductImage.objects.all().count(), 1)

	def test_get_product_image_list(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(ProductImage.objects.all().count(), 0)
