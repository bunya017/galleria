from django.urls import path
from . import views



urlpatterns = [
	path('catalogs/', views.CatalogList.as_view(), name='catalogs-list'),
]