from django.contrib.auth.models import User
from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer
from .models import (
	Catalog, Category, ProductEntry, ProductImage,
	Collection, CollectionProduct
)
from . import relations



class ProductImageSerializer(serializers.ModelSerializer):
	photo = VersatileImageFieldSerializer(
		sizes='product_image'
	)

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
			'reference_id', 'created_on', 'last_modified', 'slug',
			'photos',
		)
		extra_kwargs = {
			'slug': {
				'read_only': True
			},
			'reference_id': {
				'read_only': True
			}
		}

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


class GetProductEntrySerializer(ProductEntrySerializer):
	class Meta:
		model = ProductEntry
		depth = 2
		fields = (
			'id', 'url', 'name', 'category', 'description', 'price',
			'reference_id', 'created_on', 'last_modified', 'slug',
			'photos',
		)

		
class CollectionProductSerializer(serializers.ModelSerializer):
	id = serializers.ReadOnlyField(source='product.id')
	url = relations.ParameterisedHyperlinkedIdentityField(
		view_name='collectionproduct-detail',
		read_only=True,
		lookup_fields=(
			('collection.catalog.slug', 'collection__catalog__slug'),
			('collection.slug', 'collection__slug'),
			('product.slug', 'product__slug')
		)
	)
	name = serializers.ReadOnlyField(source='product.name')
	product = ProductEntrySerializer(read_only=True)

	class Meta:
		model = CollectionProduct
		fields = ('id', 'url', 'name', 'collection', 'product')


class AddCollectionProductSerializer(serializers.ModelSerializer):

	class Meta:
		model = CollectionProduct
		fields = ('product', 'collection')


class CollectionSerializer(serializers.ModelSerializer):
	collection_products = CollectionProductSerializer(
		source='collectionproduct_set', many=True, read_only=True
	)
	url = relations.ParameterisedHyperlinkedIdentityField(
		view_name='collection-detail',
		read_only=True,
		lookup_fields=(
			('catalog.slug', 'catalog__slug'),
			('slug', 'slug')
		)
	)
	background_image = VersatileImageFieldSerializer(
		required=False,
		sizes='bg_image'
	)

	class Meta:
		model = Collection
		fields = (
			'id', 'url', 'name', 'slug', 'description', 'catalog',
			'background_image', 'collection_products'
		)
		extra_kwargs = {'slug': {'read_only': True}}


class GetCollectionSerializer(CollectionSerializer):
	class Meta:
		model = Collection
		fields = (
			'id', 'url', 'name', 'slug', 'description', 'catalog',
			'background_image', 'collection_products'
		)
		depth = 1


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
	background_image = VersatileImageFieldSerializer(
		required=False,
		sizes='bg_image'
	)

	class Meta:
		model = Category
		fields = ('id', 'url', 'slug', 'name','catalog','created_on','description',
			'background_image', 'product_entries'
		)
		extra_kwargs = {'slug': {'read_only': True}}


class GetCategorySerializer(CategorySerializer):
	class Meta:
		model = Category
		depth = 1
		fields = ('id', 'url', 'slug', 'name','catalog','created_on','description',
			'background_image', 'product_entries'
		)


class CatalogSerializer(serializers.ModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	categories = CategorySerializer(many=True, read_only=True)
	collections = CollectionSerializer(many=True, read_only=True)
	url = serializers.HyperlinkedIdentityField(
		view_name='catalog-detail', lookup_field='slug')
	lookup_field = 'slug'

	class Meta:
		model = Catalog
		fields = (
			'id', 'owner', 'url', 'name', 'slug', 'created_on', 'description', 'contact_address', 
			'contact_email', 'contact_phone', 'categories', 'collections'
		)
		extra_kwargs = {'slug': {'read_only': True}}