from django.db import models
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50 , unique=True)
    slug = models.SlugField(max_length=100 , unique=True)
    description = models.CharField(max_length=250 ,blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_ulr(self):
        return reverse('products_by_category', args = [self.slug])

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    subcat_name = models.CharField(max_length=50 )
    slug = models.SlugField(max_length=100 , unique=True, null=True)
    category_name = models.ForeignKey(Category,on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'   
    
    def get_ulr1(self):
        return reverse('products_by_subcategory', args = [self.category_name.slug, self.slug])
    
    def __str__(self):
        return self.subcat_name

