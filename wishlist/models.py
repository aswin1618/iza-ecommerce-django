from django.db import models
from store.models import Product,Variation
from user.models import Account


# Create your models here.

class Wishlist(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete = models.CASCADE,null=True)
    variations = models.ManyToManyField(Variation, blank=True)
    is_active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.product