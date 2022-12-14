from django.contrib import admin
from .models import Category, SubCategory

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcat_name','category_name')
    prepopulated_fields = {'slug':('category_name','subcat_name',)}
    list_filter = ('category_name',)

admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)

