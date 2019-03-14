from django.contrib.auth.models import User
from rest_framework import generics, permissions, serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
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

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		headers = self.get_success_headers(serializer.data)
		token, created = Token.objects.get_or_create(user=serializer.instance)
		serialized_user = UserSerializer(token.user, context={'request': request})
		return Response({'token': token.key}, status=status.HTTP_201_CREATED, headers=headers)