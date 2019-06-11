from django.urls import path
from . import views



urlpatterns = [
	path('signup/', views.UserRegistration.as_view(), name='user-registration'),
	path('token-auth/', views.ObtainAuthToken.as_view(), name='token-auth'),
	path('profile/<str:user__username>', views.UserProfileDetail.as_view(), name='user-profile-detail'),
]