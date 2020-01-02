from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, permissions, serializers
from rest_framework.exceptions import NotAuthenticated, NotFound
from url_filter.integrations.drf import DjangoFilterBackend
from .mixins import MultipleFieldLookupMixin
from .models import (
	Catalog, Category, ProductEntry, ProductImage,
	Collection, CollectionProduct,
)
from .serializers import (
	CatalogSerializer, CategorySerializer,
	ProductEntrySerializer, ProductImageSerializer,
	GetProductEntrySerializer, CollectionSerializer,
	CollectionProductSerializer, AddCollectionProductSerializer,
	GetCollectionSerializer, GetCategorySerializer
)
from . import permissions as my_permissions



class CatalogList(generics.ListCreateAPIView):
	serializer_class = CatalogSerializer

	def get_queryset(self):
		try:
			queryset = Catalog.objects.all().filter(owner=self.request.user)
		except TypeError:
			raise NotAuthenticated
		return queryset

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class CatalogDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	Catalog Detail endpoint to be viewed by visitors.
	"""
	serializer_class = CatalogSerializer
	permission_classes = (
		my_permissions.IsCatalogOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	queryset = Catalog.objects.all()
	lookup_field = 'slug'

	def perform_update(self, serializer):
		validated_data = serializer.validated_data
		slug = self.kwargs['slug']
		instance = Catalog.objects.get(slug=slug)
		if 'background_image' in validated_data:
			instance.background_image.delete_all_created_images()
			instance.background_image.delete(save=False)
		if 'logo_image' in validated_data:
			instance.logo_image.delete_all_created_images()
			instance.logo_image.delete(save=False)
		serializer.save(owner=self.request.user)


class CategoryList(generics.ListCreateAPIView):
	serializer_class = CategorySerializer
	permission_classes = (
		my_permissions.IsCategoryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)

	def get_queryset(self):
		slug = self.kwargs['catalog__slug']
		try:
			catalog = Catalog.objects.get(slug=slug)
		except ObjectDoesNotExist:
			raise NotFound
		queryset = Category.objects.filter(catalog__slug=slug)
		return queryset

	def perform_create(self, serializer):
		name = serializer.validated_data['name']
		error_message = 'A category named \'{0}\' already exists in this catalogue.'.format(
			name.title()
		)
		try:
			serializer.save()
		except IntegrityError:
			raise serializers.ValidationError(error_message)


class CategoryDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (
		my_permissions.IsCategoryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	queryset = Category.objects.all()
	lookup_fields = ('catalog__slug', 'slug')

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return GetCategorySerializer
		return CategorySerializer

	def perform_update(self, serializer):
		validated_data = serializer.validated_data
		catalog_slug = self.kwargs['catalog__slug']
		slug = self.kwargs['slug']
		instance = Category.objects.get(catalog__slug=catalog_slug, slug=slug)
		if 'background_image' in validated_data:
			instance.background_image.delete_all_created_images()
			instance.background_image.delete(save=False)
		serializer.save(owner=self.request.user)


class ProductEntryList(generics.ListCreateAPIView):
	permission_classes = (
		my_permissions.IsProductEntryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	filter_backends = [DjangoFilterBackend]
	filter_fields = ['name', 'price', 'category']

	def get_queryset(self):
		slug = self.kwargs['category__catalog__slug']
		try:
			catalog = Catalog.objects.get(slug=slug)
		except ObjectDoesNotExist:
			raise NotFound
		queryset = ProductEntry.objects.filter(category__catalog__slug=slug)
		return queryset

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return GetProductEntrySerializer
		return ProductEntrySerializer


class ProductEntryDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (
		my_permissions.IsProductEntryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	queryset = ProductEntry.objects.all()
	lookup_fields = ('category__catalog__slug', 'slug', 'reference_id')

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return GetProductEntrySerializer
		return ProductEntrySerializer


class ProductImageList(MultipleFieldLookupMixin, generics.ListCreateAPIView):
	serializer_class = ProductImageSerializer
	permission_classes = (
		my_permissions.IsProductImageOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	queryset = ProductImage.objects.all()
	lookup_fields = (
		'product__category__catalog__slug',
		'product__slug',
		'product__reference_id',
	)


class ProductImageDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ProductImageSerializer
	permission_classes = (
		my_permissions.IsProductImageOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	queryset = ProductImage.objects.all()
	lookup_fields = (
		'product__category__catalog__slug',
		'product__slug',
		'product__reference_id',
		'id'
	)

	def perform_update(self, serializer):
		validated_data = serializer.validated_data
		catalog_slug = self.kwargs['product__category__catalog__slug']
		product_slug = self.kwargs['product__slug']
		product_reference_id = self.kwargs['product__reference_id']
		image_id = self.kwargs['id']
		instance = ProductImage.objects.get(
			product__category__catalog__slug=catalog_slug, product__slug=product_slug,
			product__reference_id=product_reference_id, id=image_id
		)
		if validated_data['photo']:
			instance.photo.delete_all_created_images()
			instance.photo.delete(save=False)
		serializer.save()

	def perform_destroy(self, instance):
		instance.photo.delete_all_created_images()
		instance.photo.delete(save=False)
		instance.delete()


class CollectionList(generics.ListCreateAPIView):
	
	def get_serializer_class(self):
		if self.request.method == 'GET':
			return GetCollectionSerializer
		return CollectionSerializer

	def get_queryset(self):
		slug = self.kwargs['catalog__slug']
		try:
			catalog = Catalog.objects.get(slug=slug)
		except ObjectDoesNotExist:
			raise NotFound
		queryset = Collection.objects.filter(catalog__slug=slug)
		return queryset

	def perform_create(self, serializer):
		name = serializer.validated_data['name']
		error_message = {
			'name': ['A collection named \'{0}\' already exists in this catalogue.'.format(name.title())]
		}
		try:
			serializer.save()
		except IntegrityError:
			raise serializers.ValidationError(error_message)


class CollectionDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CollectionSerializer
	queryset = Collection.objects.all()
	lookup_fields = ('catalog__slug', 'slug')

	def perform_update(self, serializer):
		validated_data = serializer.validated_data
		catalog_slug = self.kwargs['catalog__slug']
		slug = self.kwargs['slug']
		instance = Collection.objects.get(catalog__slug=catalog_slug, slug=slug)
		if 'background_image' in validated_data:
			instance.background_image.delete_all_created_images()
			instance.background_image.delete(save=False)
		serializer.save(owner=self.request.user)


class CollectionProductList(MultipleFieldLookupMixin, generics.ListCreateAPIView):
	queryset = CollectionProduct.objects.all()
	lookup_fields = (
		'collection__catalog__slug',
		'collection__slug'
	)

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return CollectionProductSerializer
		return AddCollectionProductSerializer


class CollectionProductDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = AddCollectionProductSerializer
	queryset = CollectionProduct.objects.all()
	lookup_fields = (
		'collection__catalog__slug',
		'collection__slug',
		'product__slug'
	)