from rest_framework import exceptions, permissions
from .models import Catalog



class IsCatalogOwnerOrReadOnly(permissions.BasePermission):
	"""
	Object-level permission to only allow owners of a catalog to edit it.
	Assumes the model instance has an `owner` attribute.
	"""

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.owner == request.user


class IsCategoryOwnerOrReadOnly(permissions.BasePermission):
	"""
	Object-level permission to only allow owners of a category.catalog to edit it.
	Assumes the model instance has an `owner` attribute.
	"""

	def has_permission(self, request, view):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		obj = Catalog.objects.get(slug=view.kwargs['catalog__slug'])
		return obj.owner == request.user

	def has_object_permission(self, request, view, obj):
		# Read permissions are allowed to any request,
		# so we'll always allow GET, HEAD or OPTIONS requests.
		if request.method in permissions.SAFE_METHODS:
			return True

		return obj.catalog.owner == request.user