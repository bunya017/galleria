from rest_framework import exceptions, permissions



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