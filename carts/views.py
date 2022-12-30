from django.shortcuts import render,redirect, get_object_or_404,HttpResponseRedirect
from store.models import Product, Variation,Coupon
from .models import Cart , CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from user.models import UserAdress,UserProfile
from django.contrib import messages
# Create your views here.

def _cart_id(request):
     cart = request.session.session_key
     if not cart:
          cart = request.session.create()
     return cart

def add_cart(request,product_id):
     current_user = request.user
     product = Product.objects.get(id=product_id)  #get the product
     
     
     #if the user is  authenticated
     if current_user.is_authenticated:
          product_variation = []
          
          if request.method == 'POST':
               color = request.POST['color']
               size = request.POST['size']
               try:
                    variation = Variation.objects.get(product=product, color__iexact=color, size__iexact=size)
                    product_variation.append(variation)
               except:
                    pass
                    print(product_variation)

          print(product_variation)
          
          is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
          if is_cart_item_exists:
               cart_item = CartItem.objects.filter(product=product, user=current_user)
               ex_var_list = []
               id = []
               for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

               if product_variation in ex_var_list:
                    #increase cart item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    if item.quantity<10:
                         item.quantity +=1
                    else:
                         messages.error(request,'You can only buy upto 10 products at one time')
                         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                    item.save()
               else:
                    item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                    if len(product_variation) > 0:
                         item.variations.clear()
                         item.variations.add(*product_variation)
                    item.save()
                    
          else:
               cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    user = current_user,
               )
               if len(product_variation) > 0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
               cart_item.save()
          return redirect('cart')
          
  # if the user is not authenticated
               
     else:
          product_variation = []
          if request.method == 'POST':
               color = request.POST['color']
               size = request.POST['size']

               try:
                    variation = Variation.objects.get(product=product,color=color, size=size)
                    product_variation.append(variation)
               except:
                    pass


          try:
               cart = Cart.objects.get(cart_id=_cart_id(request)) #getting the cart using the cart id in the session
          except Cart.DoesNotExist:
               cart = Cart.objects.create(
                    cart_id = _cart_id(request)
               )
          cart.save()

          

          is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
          if is_cart_item_exists:
               cart_item = CartItem.objects.filter(product=product, cart=cart)
               #existing variations -- db
               #current variation -- product_variation
               #item id --db
               ex_var_list = []
               id = []
               for item in cart_item:
                    existing_variation = item.variations.all()
                    ex_var_list.append(list(existing_variation))
                    id.append(item.id)

               if product_variation in ex_var_list:
                    #increase cart item quantity
                    index = ex_var_list.index(product_variation)
                    item_id = id[index]
                    item = CartItem.objects.get(product=product, id=item_id)
                    item.quantity +=1
                    item.save()
               else:
                    item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                    if len(product_variation) > 0:
                         item.variations.clear()
                         item.variations.add(*product_variation)
                    item.save()
                    
          else:
               cart_item = CartItem.objects.create(
                    product = product,
                    quantity = 1,
                    cart = cart,
               )
               if len(product_variation) >0:
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
               cart_item.save()
          return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
     
     product = get_object_or_404(Product, id=product_id)
     try:
          if request.user.is_authenticated:
               cart_item = CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
          else:
               cart = Cart.objects.get(cart_id=_cart_id(request))
               cart_item = CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
          if cart_item.quantity >1:
               cart_item.quantity -= 1
               cart_item.save()
          else:
               cart_item.delete()
     except:
          pass
     return redirect('cart')


def remove_cart_item(request, product_id,cart_item_id):
     
     product = get_object_or_404(Product, id=product_id)
     if request.user.is_authenticated:
          cart_item = CartItem.objects.get(product=product, user=request.user, id= cart_item_id)
     else:
          cart = Cart.objects.get(cart_id= _cart_id(request))
          cart_item = CartItem.objects.get(product=product, cart=cart, id= cart_item_id)

     cart_item.delete()
     return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
     try:
          if request.user.is_authenticated:
               cart_items = CartItem.objects.filter(user=request.user, is_active=True)
          else:
               cart = Cart.objects.get(cart_id= _cart_id(request))
               cart_items = CartItem.objects.filter(cart=cart, is_active=True)
          for cart_item in cart_items:
               total += (cart_item.product.price() * cart_item.quantity)
               quantity += cart_item.quantity
     except ObjectDoesNotExist:
          pass

     try:
          cart = Cart.objects.get(cart_id=_cart_id(request)) #getting the cart using the cart id in the session
     except Cart.DoesNotExist:
          cart = Cart.objects.create(cart_id = _cart_id(request))
     
     cart.total_price = total
     cart.save()   
     
          
     context = {
          'total' : total,
          'quantity' : quantity,
          'cart_items' : cart_items
     }
     return render(request,'cart.html',context)


@login_required(login_url='signin')
def checkout(request, total=0, quantity=0, cart_items=None):
     delivery= 50
     try:
          if request.user.is_authenticated:
               cart_items = CartItem.objects.filter(user=request.user, is_active=True).order_by('id')
          else:
               cart = Cart.objects.get(cart_id= _cart_id(request))
               cart_items = CartItem.objects.filter(cart=cart, is_active=True)
          for cart_item in cart_items:
               quantity += cart_item.quantity
     except ObjectDoesNotExist:
          pass
     
     try:
          cart = Cart.objects.get(cart_id=_cart_id(request)) #getting the cart using the cart id in the session
     except Cart.DoesNotExist:
          cart = Cart.objects.create(cart_id = _cart_id(request))
     
     total = cart.total_price
     
       
     userprofile = get_object_or_404(UserProfile ,user=request.user)
     adress_list = UserAdress.objects.filter(user=userprofile)
     if total < 2000 :
          final_total = total + delivery
     else:
          
          final_total = total
          
     context = {
          'total' : total,
          'final_total' :final_total,
          'quantity' : quantity,
          'cart_items' : cart_items,
          'adress_list': adress_list
     }

     return render (request,'checkout.html',context)


def add_coupon(request,total=0, quantity=0, cart_items=None):
     try:
          if request.user.is_authenticated:
               cart_items = CartItem.objects.filter(user=request.user, is_active=True)
          else:
               cart = Cart.objects.get(cart_id= _cart_id(request))
               cart_items = CartItem.objects.filter(cart=cart, is_active=True)
          for cart_item in cart_items:
               total += (cart_item.product.price() * cart_item.quantity)
               quantity += cart_item.quantity
     except ObjectDoesNotExist:
          pass
     
     try:
          cart = Cart.objects.get(cart_id=_cart_id(request)) #getting the cart using the cart id in the session
     except Cart.DoesNotExist:
          cart = Cart.objects.create(cart_id = _cart_id(request))
     
           
     if request.method =='POST':
          coupon = request.POST.get('coupon')
          coupon_obj = Coupon.objects.filter(coupon_code__icontains = coupon)
          if not coupon_obj.exists():
               messages.warning(request,'coupon does not exist')
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
          if coupon_obj[0].is_expired:
               messages.warning(request,'coupon expired')
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
          if cart.coupon:
               messages.warning(request,'coupon already applied')
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
          
          if total < coupon_obj[0].minimum_amount:
               messages.warning(request,'total exceeds coupon price limit') 
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
          else:
               messages.success(request,'Coupon Applied')
               cart.coupon = coupon_obj[0]
               total = total-(coupon_obj[0].discount_price) 
               cart.total_price = total
               cart.save()
               return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     context = {
          'cart': cart,
          'total' : total,
          'quantity' : quantity,
          'cart_items' : cart_items
     }
     return render(request,'coupon.html',context)
          
def remove_coupon(request, cart_id):
     cart_obj = Cart.objects.get(id= cart_id)
     cart_obj.total_price= cart_obj.total_price + cart_obj.coupon.discount_price
     cart_obj.coupon = None
     cart_obj.save()
     messages.success(request,'coupon removed')
     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))