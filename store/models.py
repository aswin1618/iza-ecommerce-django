from django.db import models
from category.models import SubCategory,Category
from django.urls import reverse

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length = 200, unique = True)
    slug         = models.SlugField(max_length = 200, unique =True)
    brand        = models.CharField(max_length=100 ,default=None)
    description  = models.TextField(max_length = 500 ,blank = True)
    price        = models.IntegerField()
    stock        = models.IntegerField(default=0)
    images       = models.ImageField(upload_to ='photos/products')
    is_available = models.BooleanField(default = True)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    SubCategory  = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date= models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default = False)
    

    def get_url(self):
        print(self.slug)
        return reverse('product_detail', args=[self.category.slug,self.SubCategory.slug,self.slug])

    def __str__(self):
        return self.product_name


color_choice=(
    ('red','red'),
    ('orange','orange'),
    ('yellow','yellow'),
    ('green','green'),
    ('cyan','cyan'),
    ('azure','azure'),
    ('blue','blue'),
    ('violet','violet'),
    ('magenta','magenta'),
    ('pink','pink'),
)
size_choice=(
    ('XS','XS'),
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL'),
)
class Variation(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    color = models.CharField(max_length=100, choices=color_choice ,default='null')
    size = models.CharField(max_length=100, choices=size_choice, default='null')
    stock = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product) + " " + self.color+ " " + self.size

