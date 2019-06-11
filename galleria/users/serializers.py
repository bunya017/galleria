from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import UserProfile



class UserSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(
		validators=[
			UniqueValidator(
				queryset=User.objects.all(),
				message='A user with that email already exists.'
			)
		]
	)

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'password')
		extra_kwargs = {
			'password': {'write_only': True},
			'email': {'required': True}
		}

	def create(self, validated_data):
		user = User(
			email=validated_data['email'],
			username=validated_data['username'],
		)
		user.set_password(validated_data['password'])
		user.save()
		return user


class UserProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer(read_only=True)

	class Meta:
		model = UserProfile
		fields = ('id', 'address', 'phone', 'user')