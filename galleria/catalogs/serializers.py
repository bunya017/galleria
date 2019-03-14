from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Catalog, Category, ProductEntry, ProductImage



class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ('id', 'product', 'title', 'photo')


class ProductEntrySerializer(serializers.ModelSerializer):
	photos = ProductImageSerializer(many=True)

	class Meta:
		model = ProductEntry
		fields = (
			'id', 'name', 'category', 'description', 'price', 'reference_number', 
			'created_by', 'created_on', 'last_modified', 'photos',
		)


class CategorySerializer(serializers.ModelSerializer):
	product_entries = ProductEntrySerializer(many=True)

	class Meta:
		model = Category
		fields = ('id', 'name','catalog','created_on','description', 'product_entries')


class CatalogSerializer(serializers.ModelSerializer):
	categories = CategorySerializer(many=True)

	class Meta:
		model = Catalog
		fields = (
			'name', 'created_on', 'description', 'contact_address', 'contact_email', 
			'contact_phone', 'categories',
		)