from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify

from versatileimagefield.fields import VersatileImageField
from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from .utils import generate_hash_id



'''
# Not sure whether to keep this here or in the users app
FREE_TRIAL = 'FR'
BASIC_PLAN = 'BP'
PRO_PLAN = 'PP'
SUBSCRIPTION_PLAN_CHOICES = (
	(FREE_TRIAL, 'Free Trial'),
	(BASIC_PLAN, 'Basic'),
	(PRO_PLAN, 'Pro'),
)
subscription_plan = models.CharField(
		max_length=2,
		choices=
	)
'''


@receiver(models.signals.post_save, sender='catalogs.ProductImage')
def warm_product_images(sender, instance, ** kwargs):
	"""Ensures different Product image sizes are created post-save"""
	product_img_warmer = VersatileImageFieldWarmer(
	instance_or_queryset=instance,
	rendition_key_set='product_image',
	image_attr='photo'
	)
	num_created, failed_to_create = product_img_warmer.warm()


@receiver(models.signals.post_save, sender='catalogs.Catalog')
@receiver(models.signals.post_save, sender='catalogs.Category')
@receiver(models.signals.post_save, sender='catalogs.Collection')
def warm_bg_images(sender, instance, ** kwargs):
	"""Ensures different background image sizes are created post-save"""
	bg_img_warmer = VersatileImageFieldWarmer(
	instance_or_queryset=instance,
	rendition_key_set='bg_image',
	image_attr='background_image'
	)
	num_created, failed_to_create = bg_img_warmer.warm()


def product_photo_upload_path(instance, filename):
	return '{0}/product-images/{1}-{2}/{3}'.format(
		instance.product.category.catalog.slug,
		instance.product.slug,
		instance.product.reference_id,
		filename,
	)

def category_bg_photo_upload_path(instance, filename):
	return '{0}/background-images/categories/{1}/{2}'.format(
		instance.catalog.slug,
		instance.slug,
		filename,
	)

def collection_bg_photo_upload_path(instance, filename):
	return '{0}/background-images/collections/{1}/{2}'.format(
		instance.catalog.slug,
		instance.slug,
		filename,
	)

def catalog_bg_photo_upload_path(instance, filename):
	return '{0}/background-images/catalog/{1}'.format(
		instance.slug,
		filename,
	)


class Catalog(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=150, unique=True)
	slug = models.SlugField()
	created_on = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255)
	contact_address = models.CharField(max_length=255)
	contact_email = models.CharField(max_length=100)
	contact_phone = models.CharField(max_length=50)
	background_image = VersatileImageField(
		upload_to=catalog_bg_photo_upload_path,
		blank=True
	)

	class Meta:
		verbose_name = 'Catalog'
		verbose_name_plural = 'Catalogs'

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		self.slug = slugify(self.name)
		super(Catalog, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=150)
	catalog = models.ForeignKey(
		Catalog, related_name='categories', on_delete=models.CASCADE
	)
	slug = models.SlugField()
	created_on = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255, blank=True)
	background_image = VersatileImageField(
		upload_to=category_bg_photo_upload_path,
		blank=True
	)

	class Meta:
		verbose_name_plural = 'Categories'
		unique_together = ('name', 'catalog')

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class ProductEntry(models.Model):
	name = models.CharField(max_length=150)
	category = models.ForeignKey(
		Category, related_name='product_entries', on_delete=models.CASCADE
	)
	slug = models.SlugField()
	description = models.CharField(max_length=355)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	sku = models.CharField(max_length=32, blank=True)
	reference_id = models.CharField(max_length=16, blank=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = 'Products'

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		self.slug = slugify(self.name)
		products_count = ProductEntry.objects.all().count()
		self.reference_id = generate_hash_id(id=products_count+1, salt=self.name, len=16)
		super(ProductEntry, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class ProductImage(models.Model):
	product = models.ForeignKey(
		ProductEntry, related_name='photos', on_delete=models.CASCADE
	)
	title = models.CharField(max_length=150)
	photo = VersatileImageField(upload_to=product_photo_upload_path, blank=True)

	class Meta:
		verbose_name = 'Product Image'
		verbose_name_plural = 'Product Images'

	def __str__(self):
		return self.product.name + ' - photo'


class Collection(models.Model):
	name = models.CharField(max_length=100)
	catalog = models.ForeignKey(
		Catalog, related_name='collections', on_delete=models.CASCADE
	)
	slug = models.SlugField(max_length=120)
	description = models.TextField(blank=True)
	products = models.ManyToManyField(
		ProductEntry, blank=True, related_name='collection_products',
		through='CollectionProduct'
	)
	background_image = VersatileImageField(
		upload_to=collection_bg_photo_upload_path,
		blank=True
	)

	class Meta:
		unique_together = ('name', 'catalog')
		verbose_name = 'Collection'
		verbose_name_plural = 'Collections'

	def save(self, *args, **kwargs):
		self.name = self.name.title()
		self.slug = slugify(self.name)
		super(Collection, self).save(*args, **kwargs)

	def __str__(self):
		return self.name + ' - ' + self.catalog.name


class CollectionProduct(models.Model):
	product = models.ForeignKey(ProductEntry, on_delete=models.CASCADE)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('product', 'collection')
		verbose_name = 'Collction Product'
		verbose_name_plural = 'collection Products'

	def __str__(self):
		return self.product.name + ' - ' + self.collection.name