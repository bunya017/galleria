from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated
from .mixins import MultipleFieldLookupMixin
from .models import (
	Catalog, Category, ProductEntry, ProductImage,
	Collection, CollectionProduct,
)
from .serializers import (
	CatalogSerializer, CategorySerializer,
	ProductEntrySerializer, ProductImageSerializer,
	GetProductEntrySerializer, CollectionSerializer,
	CollectionProductSerializer, AddCollectionProductSerializer
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


class CategoryList(generics.ListCreateAPIView):
	serializer_class = CategorySerializer
	permission_classes = (
		my_permissions.IsCategoryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)

	def get_queryset(self):
		slug = self.kwargs['catalog__slug']
		queryset = Category.objects.filter(catalog__slug=slug)
		return queryset


class CategoryDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CategorySerializer
	permission_classes = (
		my_permissions.IsCategoryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)
	queryset = Category.objects.all()
	lookup_fields = ('catalog__slug', 'slug')


class ProductEntryList(generics.ListCreateAPIView):
	permission_classes = (
		my_permissions.IsProductEntryOwnerOrReadOnly,
		permissions.IsAuthenticatedOrReadOnly,
	)

	def get_queryset(self):
		slug = self.kwargs['category__catalog__slug']
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
	lookup_fields = ('category__catalog__slug', 'slug')

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


class CollectionList(generics.ListCreateAPIView):
	serializer_class = CollectionSerializer

	def get_queryset(self):
		slug = self.kwargs['catalog__slug']
		queryset = Collection.objects.filter(catalog__slug=slug)
		return queryset


class CollectionDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CollectionSerializer
	queryset = Collection.objects.all()
	lookup_fields = ('catalog__slug', 'slug')


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