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
	path('catalogs/<str:catalog__slug>/<str:slug>/',
		views.CategoryDetail.as_view(), name='category-detail',
	),
	path('catalogs/<str:category__catalog__slug>/p/products/',
		views.ProductEntryList.as_view(), name='productentry-list',
	)
]