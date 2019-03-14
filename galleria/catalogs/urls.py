from django.urls import path
from . import views



urlpatterns = [
	path('catalogs/', views.CatalogList.as_view(), name='catalog-list'),
	path('catalogs/<str:slug>/', views.CatalogDetail.as_view(), 
		name='catalog-detail',
	),
	path('catalogs/<str:catalog__slug>/categories/', 
		views.CategoryList.as_view(), name='category-list',
	),
]