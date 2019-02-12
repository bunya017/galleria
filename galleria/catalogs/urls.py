from django.urls import path
from . import views



urlpatterns = [
	path('catalogs/', views.CatalogList.as_view(), name='catalogs-list'),
	path('catalogs/<str:name>/', views.CatalogDetail.as_view(), name='catalogs-detail'),
]