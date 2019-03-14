from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify



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

class Catalog(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	slug = models.SlugField(unique=True)
	created_on = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255)
	contact_address = models.CharField(max_length=255)
	contact_email = models.CharField(max_length=100)
	contact_phone = models.CharField(max_length=50)

	class Meta:
		verbose_name = 'Catalog'
		verbose_name_plural = 'Catalogs'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Catalog, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=150)
	catalog = models.ForeignKey(Catalog, related_name='categories', on_delete=models.CASCADE)
	slug = models.SlugField(unique=True)
	created_on = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255, blank=True)

	class Meta:
		verbose_name_plural = 'Categories'

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class ProductEntry(models.Model):
	name = models.CharField(max_length=150)
	category = models.ForeignKey(Category, related_name='product_entries', on_delete=models.CASCADE)
	description = models.CharField(max_length=355)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	reference_number = models.CharField(max_length=15)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = 'Products'

	def __str__(self):
		return self.name


class ProductImage(models.Model):
	product = models.ForeignKey(ProductEntry, related_name='photos', on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	photo = models.ImageField(upload_to='uploads/', blank=True)

	class Meta:
		verbose_name = 'Product Image'
		verbose_name_plural = 'Product Images'