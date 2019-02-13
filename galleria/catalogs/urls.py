from django.urls import path
from . import views



urlpatterns = [
	path('catalogs/', views.CatalogList.as_view(), name='catalog-list'),
	path('catalogs/<str:slug>/', views.CatalogDetail.as_view(), name='catalog-detail'),
]