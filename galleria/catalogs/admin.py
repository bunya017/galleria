from django.contrib import admin
from .models import Catalog, Category, ProductEntry



admin.site.register(Catalog)
admin.site.register(Category)
admin.site.register(ProductEntry)