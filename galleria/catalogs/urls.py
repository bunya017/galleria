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
	path('catalogs/<str:catalog__slug>/categories/<str:slug>/',
		views.CategoryDetail.as_view(), name='category-detail',
	),
	path('catalogs/<str:category__catalog__slug>/products/',
		views.ProductEntryList.as_view(), name='productentry-list',
	),
	path('catalogs/<str:category__catalog__slug>/products/<str:slug>/<str:reference_id>/',
		views.ProductEntryDetail.as_view(), name='productentry-detail',
	),
	path('catalogs/<str:product__category__catalog__slug>/p/<str:product__slug>/<str:reference_id>/photos/',
		views.ProductImageList.as_view(), name='productimage-list',
	),
	path('catalogs/<str:catalog__slug>/collections/', 
		views.CollectionList.as_view(), name='collection-list',
	),
	path('catalogs/<str:catalog__slug>/collections/<str:slug>/',
		views.CollectionDetail.as_view(), name='collection-detail',
	),
	path('catalogs/<str:collection__catalog__slug>/collections/<str:collection__slug>/products',
		views.CollectionProductList.as_view(), name='collectionproduct-list',
	),
]