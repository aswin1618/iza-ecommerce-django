from django.contrib import admin
from .models import Product,Variation

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','category','brand','SubCategory','modified_date','is_available')
    prepopulated_fields ={'slug':('brand','product_name',)}
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','color','size','is_active','stock')
    list_editable = ('is_active',)
    list_filter = ('product__category','product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)