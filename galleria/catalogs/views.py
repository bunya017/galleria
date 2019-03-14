from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated
from .models import Catalog, Category
from .serializers import CatalogSerializer, CategorySerializer



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


class CatalogDetail(generics.RetrieveAPIView):
	"""
	Catalog Detail endpoint to be viewed by visitors.
	"""
	serializer_class = CatalogSerializer
	permission_classes = (permissions.AllowAny,)
	queryset = Catalog.objects.all()
	lookup_field = 'slug'


class CategoryList(generics.ListCreateAPIView):
	serializer_class = CategorySerializer

	def get_queryset(self):
		slug = self.kwargs['catalog__slug']
		queryset = Category.objects.filter(catalog__slug=slug)
		return queryset