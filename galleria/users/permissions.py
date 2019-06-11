from rest_framework import permissions
from .models import UserProfile



class IsProfileOwner(permissions.BasePermission):
	"""
	Allows access only to profile owners.
	"""

	def has_permission(self, request, view):
		profile_user = UserProfile.objects.get(
			user__username=view.kwargs['user__username']
		)
		return profile_user.user == request.user

	def has_object_permission(self, request, view, obj):
		return obj.user == request.user