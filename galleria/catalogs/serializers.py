from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Catalog, Category, ProductEntry, ProductImage
from . import relations



class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ('id', 'product', 'photo')


class ProductEntrySerializer(serializers.ModelSerializer):
	photos = ProductImageSerializer(many=True, read_only=True)
	url = relations.ParameterisedHyperlinkedIdentityField(
		view_name='productentry-detail',
		lookup_fields=(
			('category.catalog.slug', 'category__catalog__slug'),
			('reference_id', 'reference_id'),
			('slug', 'slug'),
		)
	)

	class Meta:
		model = ProductEntry
		fields = (
			'id', 'url', 'name', 'category', 'description', 'price', 
			'created_on', 'last_modified', 'photos',
		)

	def create(self, validated_data):
		request = self.context.get('request')
		photos_data = request.FILES.getlist('photos')
		if not photos_data:
			error = {
				'photos': 'This field is required.'
			}
			raise serializers.ValidationError(error)
		else:
			product_entry = ProductEntry.objects.create(created_by=request.user, **validated_data)
			for photo in photos_data:
				ProductImage.objects.create(product=product_entry, photo=photo)
			return product_entry


class CategorySerializer(serializers.ModelSerializer):
	product_entries = ProductEntrySerializer(many=True, read_only=True)
	url = relations.ParameterisedHyperlinkedIdentityField(
		view_name='category-detail',
		read_only=True,
		lookup_fields=(
			('catalog.slug', 'catalog__slug'),
			('slug', 'slug'),
		)
	)

	class Meta:
		model = Category
		fields = ('id', 'url', 'slug', 'name','catalog','created_on','description',
			'product_entries',
		)
		extra_kwargs = {'slug': {'read_only': True}}


class CatalogSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	categories = CategorySerializer(many=True, read_only=True)
	url = serializers.HyperlinkedIdentityField(
		view_name='catalog-detail', lookup_field='slug')
	lookup_field = 'slug'

	class Meta:
		model = Catalog
		fields = (
			'id', 'owner', 'url', 'name', 'slug', 'created_on', 'description', 'contact_address', 
			'contact_email', 'contact_phone', 'categories',
		)
		extra_kwargs = {'slug': {'read_only': True}}