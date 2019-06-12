from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
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
def product_photo_upload_path(instance, filename):
	return '{0}/product-images/{1}-{2}/{3}'.format(
		instance.product.category.catalog.slug,
		instance.product.slug,
		instance.product.reference_id,
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
	slug = models.SlugField()
	created_on = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255, blank=True)

	class Meta:
		verbose_name_plural = 'Categories'
		unique_together = ('name', 'catalog')

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class ProductEntry(models.Model):
	name = models.CharField(max_length=150)
	category = models.ForeignKey(Category, related_name='product_entries', on_delete=models.CASCADE)
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
		self.slug = slugify(self.name)
		products_count = ProductEntry.objects.all().count()
		self.reference_id = generate_hash_id(id=products_count+1, salt=self.name, len=16)
		super(ProductEntry, self).save(*args, **kwargs)

	def __str__(self):
		return self.name


class ProductImage(models.Model):
	product = models.ForeignKey(ProductEntry, related_name='photos', on_delete=models.CASCADE)
	title = models.CharField(max_length=150)
	photo = models.ImageField(upload_to=product_photo_upload_path, blank=True)

	class Meta:
		verbose_name = 'Product Image'
		verbose_name_plural = 'Product Images'

	def __str__(self):
		return self.product.name + ' - photo'


class CollectionProduct(models.Model):
	collection = models.ForeignKey(
		'Collection', related_name='collection_product', on_delete=models.CASCADE
	)
	product = models.ForeignKey(
		ProductEntry, related_name='collection_product', on_delete=models.CASCADE
	)


class Collection(models.Model):
	name = models.CharField(max_length=150)
	catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
	slug = models.SlugField(max_length=150)
	description = models.TextField(blank=True)
	products = models.ManyToManyField(
		ProductEntry,
		blank=True,
		related_name='collections',
		through=CollectionProduct,
		through_fields=['collection', 'product']
	)

	class Meta:
		unique_together = ('name', 'catalog')
		verbose_name = 'Collection'
		verbose_name_plural = 'Collections'

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Collection, self).save(*args, **kwargs)
