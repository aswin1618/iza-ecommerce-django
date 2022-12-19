from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product, Variation
from .models import Wishlist
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

# Create your views here.
def wishlist(request, quantity=0, wishlist_items=None):

        
        if request.user.is_authenticated:
            print(request.user)
            wishlist_items = Wishlist.objects.filter(user=request.user, is_active=True)
        
            context = {
                'wishlist_items' : wishlist_items
            }

            return render(request,'wishlist.html',context)
            
        else:
            messages.error(request,'you need to sign in first')
            return redirect('signin')
                
def add_wish(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)  #get the product
    
    is_wishlist_item_exists = Wishlist.objects.filter(product=product,user=current_user).exists()
    if is_wishlist_item_exists:
        messages.error(request,'item already in wishlist')
        return redirect('wishlist')
        
    else:
        wishlist_item = Wishlist.objects.create(
                            product = product,
                            user = current_user,
                    )
        wishlist_item.save()
        messages.success(request,'item added to wishlist')
        return redirect('wishlist')


    
def remove_wish_item(request, product_id, wishlist_item_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item = Wishlist.objects.get(product=product, id= wishlist_item_id)

    wishlist_item.delete()
    return redirect('wishlist')