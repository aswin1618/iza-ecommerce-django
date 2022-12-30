from django.db import models
from category.models import SubCategory,Category
from user.models import Account
from django.urls import reverse
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator


PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
RATING_VALIDATOR = [MinValueValidator(0), MaxValueValidator(5)]

# Create your models here.
class Brand(models.Model):
    brand_name = models.CharField(max_length = 20, unique = True)
    def __str__(self):
        return self.brand_name
class SubcategoryOffer(models.Model):
    subcategory = models.OneToOneField(SubCategory,on_delete=models.CASCADE)
    sub_category_offer = models.IntegerField(validators=PERCENTAGE_VALIDATOR,blank=True,null=True,default=0)
    is_expired = models.BooleanField(default=False)
    
    
class BrandOffer(models.Model):
    brand = models.OneToOneField(Brand,on_delete=models.CASCADE)
    brand_offer = models.IntegerField(validators=PERCENTAGE_VALIDATOR,blank=True,null=True,default=0)
    is_expired = models.BooleanField(default=False)

    
class Product(models.Model):
    product_name = models.CharField(max_length = 200, unique = True)
    slug         = models.SlugField(max_length = 200,)
    brand        = models.ForeignKey(Brand,on_delete=models.CASCADE)
    description  = models.TextField(max_length = 500 ,blank = True)
    stock_price  = models.PositiveIntegerField()
    stock        = models.PositiveIntegerField(default=0)
    images       = models.ImageField(upload_to ='photos/products')
    is_available = models.BooleanField(default = True)
    category     = models.ForeignKey(Category,on_delete=models.CASCADE)
    SubCategory  = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add = True)
    modified_date= models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default = False)
    sub_category_offer = models.ForeignKey(SubcategoryOffer,on_delete=models.SET_NULL,null=True,blank=True)
    brand_offer = models.ForeignKey(BrandOffer,on_delete=models.SET_NULL,null=True,blank=True)

    def get_url(self):
        print(self.slug)
        return reverse('product_detail', args=[self.category.slug,self.SubCategory.slug,self.slug])
    
    def offer (self):
        if self.sub_category_offer or self.brand_offer:
            if self.sub_category_offer is None:
                return self.brand_offer.brand_offer
            elif self.brand_offer is None:
                return self.sub_category_offer.sub_category_offer
            else:
                if self.sub_category_offer.sub_category_offer > self.brand_offer.brand_offer:
                    return self.sub_category_offer.sub_category_offer
                else:
                    return self.brand_offer.brand_offer
        else:
            return 0
        
    def price(self):
        if self.sub_category_offer or self.brand_offer:
            if self.sub_category_offer is None:
                return int(self.stock_price * (1-(self.brand_offer.brand_offer/100)))
            elif self.brand_offer is None:
                return int(self.stock_price * (1-(self.sub_category_offer.sub_category_offer/100)))
            else:
                if self.sub_category_offer.sub_category_offer > self.brand_offer.brand_offer:
                    return int(self.stock_price * (1-(self.sub_category_offer.sub_category_offer/100)))
                else:
                    return int(self.stock_price * (1-(self.brand_offer.brand_offer/100)))
        else:
            return self.stock_price
            
    def __str__(self):
        return self.product_name

    def avg_rating(self):
        reviews = ReviewRatings.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
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
    ('black','black'),
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
    stock = models.PositiveIntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product) + " " + self.color+ " " + self.size

class Banner(models.Model):
    img = models.ImageField(upload_to='photos/banners', blank=True)
    text = models.TextField(blank=True,null=True)
    
    
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=15)
    is_expired = models.BooleanField(default=False)
    discount_price = models.PositiveIntegerField()
    minimum_amount = models.PositiveIntegerField()
    
    
class ReviewRatings(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    review = models.CharField(max_length=500,blank=True)
    rating = models.FloatField(validators=RATING_VALIDATOR)
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.subject


fabric_choice=(
    ('Cotton','Cotton'),
    ('Spandex','Spandex'),
    ('Polyester','Polyester'),
)
wash_care_choice=(
    ('Machine wash','Machine wash'),
    ('Handwash','Handwash'),
    ('Any wash','Any wash'),
)
fit_choice=(
    ('Regular','Regular'),
    ('Slimfit','Slimfit'),
    ('Baggy fit','Baggy fit'),
)
occasion_choice=(
    ('Athletic','Athletic'),
    ('Football','Football'),
    ('Gym-wear','Gym-wear'),
    ('Cricket','Cricket'),
    ('Other','Other'),
)


class ProductAttributes(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)
    fabric = models.CharField(max_length=25, choices=fabric_choice)
    wash_care = models.CharField(max_length=25, choices=wash_care_choice)
    fit = models.CharField(max_length=25, choices=fit_choice)
    occasion = models.CharField(max_length=25, choices=occasion_choice)