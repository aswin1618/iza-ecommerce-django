from django.contrib import admin
from .models import Category, SubCategory

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('subcat_name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(SubCategory,SubCategoryAdmin)

