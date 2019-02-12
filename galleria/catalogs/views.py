from rest_framework import generics, permissions
from rest_framework.exceptions import NotAuthenticated
from .models import Catalog
from .serializers import CatalogSerializer



class CatalogList(generics.ListCreateAPIView):
	serializer_class = CatalogSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
	lookup_field= 'name'