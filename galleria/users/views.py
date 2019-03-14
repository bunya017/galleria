from rest_framework import generics, permissions, serializers, status
from .serializers import UserSerializer



class UserRegistration(generics.CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)