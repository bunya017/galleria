from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
	if created:
		Token.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance=None, created=False, **kwargs):
	if created:
		UserProfile.objects.create(user=instance)



class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	address = models.CharField(max_length=250)
	phone = models.CharField(max_length=25)

	class Meta:
		verbose_name = 'User Profile'
		verbose_name_plural = 'User Profiles'

	def __str__(self):
		if self.user.get_full_name():
			return self.user.username + ' (' + self.user.get_full_name() + ')'
		return self.user.username