from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Catalog, Category, ProductEntry, ProductImage
from . import relations



class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ('id', 'product', 'title', 'photo')


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


class CategorySerializer(serializers.ModelSerializer):
	product_entries = ProductEntrySerializer(many=True, read_only=True)
	url = relations.ParameterisedHyperlinkedRelatedField(
		view_name='category-detail',
		read_only=True,
		lookup_fields=(
			('catalog.slug', 'catalog__slug'),
			('slug', 'slug'),
		)
	)

	class Meta:
		model = Category
		fields = ('id', 'url', 'name','catalog','created_on','description',
			'product_entries',
		)


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