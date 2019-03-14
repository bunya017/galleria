from django.contrib.auth.models import User
from rest_framework import generics, permissions, serializers, status
from .serializers import UserSerializer



class UserRegistration(generics.CreateAPIView):
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)

	def perform_create(self, serializer):
		data = serializer.validated_data
		email = data['email']
		if email == '':
			raise serializers.ValidationError({'email': 'This field may not be blank.'})
		elif User.objects.filter(email=email).exists():
			raise serializers.ValidationError({'email': 'A user with that email already exists.'})
		serializer.save()
