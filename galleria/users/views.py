from django.contrib.auth.models import User
from rest_framework import generics, permissions, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as DRFObtainAuthToken
from rest_framework.response import Response
from .models import UserProfile
from .serializers import (
	UserSerializer, UserProfileSerializer,
	GetUserProfileSerializer
)
from . import permissions as my_user_permissions



class UserRegistration(generics.CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)
	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		token, created = Token.objects.get_or_create(user=serializer.instance)
		serialized_user = UserSerializer(token.user, context={'request': request})
		return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)


class ObtainAuthToken(DRFObtainAuthToken):
	
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({'token': token.key})


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (my_user_permissions.IsProfileOwner, )
	queryset = UserProfile.objects.all()
	lookup_field = 'user__username'

	def get_serializer_class(self):
		if self.request.method == 'GET':
			return GetUserProfileSerializer
		return UserProfileSerializer