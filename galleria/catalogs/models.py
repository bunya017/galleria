from django.contrib.auth.models import User
from django.db import models



'''
# Not sure whether to keep this here or in the users app
FREE_TRIAL = 'FR'
BASIC_PLAN = 'BP'
PRO_PLAN = 'PP'
SUBSCRIPTION_PLAN_CHOICES = (
	(FREE_TRIAL, 'Free Trial'),
	(BASIC_PLAN, 'Basic'),
	(PRO_PLAN, 'Pro'),
)
subscription_plan = models.CharField(
		max_length=2,
		choices=
	)
'''

class Catalog(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)
	created_on = models.DateTimeField(auto_now_add=True)
	description = models.CharField(max_length=255)
	contact_address = models.CharField(max_length=255)
	contact_email = models.CharField(max_length=100)
	contact_phone = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class ProductEntry(models.Model):
	name = models.CharField(max_length=75)
	description = models.CharField(max_length=355)
	price = models.DecimalField(max_digits=12, decimal_places=2)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
	last_modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name