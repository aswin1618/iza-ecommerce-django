from django.contrib import admin
from .models import Product,Variation ,Banner,Coupon, Brand,BrandOffer,SubcategoryOffer, ReviewRatings,ProductAttributes

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','stock_price','category','brand','SubCategory','modified_date','is_available','offer','price')
    prepopulated_fields ={'slug':('brand','product_name',)}
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','color','size','is_active','stock')
    list_editable = ('is_active',)
    list_filter = ('product__category','product')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Banner)
admin.site.register(Coupon)
admin.site.register(Brand)
admin.site.register(BrandOffer)
admin.site.register(SubcategoryOffer)
admin.site.register(ReviewRatings)
admin.site.register(ProductAttributes)
