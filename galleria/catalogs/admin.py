from django.contrib import admin
from .models import (
	Catalog, Category, ProductEntry, ProductImage
)



admin.site.register(Catalog)
admin.site.register(Category)
admin.site.register(ProductEntry)
admin.site.register(ProductImage)