from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated
from .mixins import MultipleFieldLookupMixin
from .models import Catalog, Category, ProductEntry, ProductImage
from .serializers import (
	CatalogSerializer, CategorySerializer,
	ProductEntrySerializer, ProductImageSerializer,
)
from .import permissions as my_permissions



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

	def get_queryset(self):
		slug = self.kwargs['catalog__slug']
		queryset = Category.objects.filter(catalog__slug=slug)
		return queryset


class CategoryDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = CategorySerializer
	queryset = Category.objects.all()
	lookup_fields = ('catalog__slug', 'slug')


class ProductEntryList(generics.ListCreateAPIView):
	serializer_class = ProductEntrySerializer

	def get_queryset(self):
		slug = self.kwargs['category__catalog__slug']
		queryset = ProductEntry.objects.filter(category__catalog__slug=slug)
		return queryset

	def perform_create(self, serializer):
		data = serializer.validated_data
		serializer.save(created_by=self.request.user)


class ProductEntryDetail(MultipleFieldLookupMixin, generics.RetrieveUpdateDestroyAPIView):
	serializer_class = ProductEntrySerializer
	queryset = ProductEntry.objects.all()
	lookup_fields = ('category__catalog__slug', 'slug')


class ProductImageList(MultipleFieldLookupMixin, generics.ListCreateAPIView):
	serializer_class = ProductImageSerializer
	queryset = ProductImage.objects.all()
	lookup_fields = (
		'product__category__catalog__slug',
		'product__slug',
		'product__reference_id',
	)