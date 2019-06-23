from django.contrib import admin
from .models import (
	Catalog, Category, ProductEntry, ProductImage, Collection,
	CollectionProduct
)



class CollectionProductInline(admin.TabularInline):
	model = CollectionProduct
	extra = 1


class CollectionAdmin(admin.ModelAdmin):
	inlines = [CollectionProductInline]


admin.site.register(Catalog)
admin.site.register(Category)
admin.site.register(ProductEntry)
admin.site.register(ProductImage)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionProduct)