from django.shortcuts import render,redirect
from carts.models import CartItem
from .forms import OrderForm
from .models import Order,Payment,OrderProduct
import razorpay
from django.conf import settings
from store.models import Variation,Product
from django.http import JsonResponse

import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def payments(request):
    
    payment = Payment()
    payment.user = request.user
    if request.POST.get('payment_id'):
        payment.payment_id = request.POST.get('payment_id') 
    payment.payment_method = request.POST.get('payment_mode')
    payment.amount_paid = request.POST.get('amount_paid') 
    print('asfsadfasdfdsfadsfasdf', payment.amount_paid)
    payment.status=True
    payment.save()

        
    # payment_id = request.POST.get('payment_id')
    # amount_paid = 100
    # if request.POST.get('payment_id'):
    #     razorpay_client.payment.capture(payment_id, amount_paid)
    order_number = request.POST.get('order_number')
    print('asfsadfasdfdsfadsfasdf',order_number )
    
    order = Order.objects.get(user=request.user, order_number=order_number)
    order.payment = payment
    order.is_ordered = True
    order.status ='Accepted' 
    order.save()
    print(order.order_number)
    
    # item = CartItem.objects.get(id=cart_item.id)
    # product_variation = item.variations.all()

    cart_items = CartItem.objects.filter(user=request.user)
    for cart_item in cart_items:    
        # OrderProduct.objects.create(
        #     order=order,
        #     payment=payment,
        #     user=request.user,
        #     product=cart_item.product,
        #     quantity=cart_item.quantity,
        #     product_price=cart_item.product.price,
        #     ordered = True,
        #     variation= cart_item.variations
        # )
        order_product = OrderProduct()
        order_product.order = order
        order_product.payment = payment
        order_product.user = request.user
        order_product.product = cart_item.product
        order_product.quantity = cart_item.quantity
        order_product.product_price = cart_item.product.price
        order_product.ordered = True
        order_product.save()

        item = CartItem.objects.get(id=cart_item.id)
        product_variation = item.variations.all()
        print(product_variation)
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variation.set(product_variation)
        order_product.save()    
        
        #reducing the quantity
        
        product = Product.objects.get(id=cart_item.product.id)
        product_variation= Variation.objects.get(product=product)
        product_variation.stock -= cart_item.quantity
        product_variation.save()
    
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()
    print("cart item deleted")
    # order confirmed email
    # mail_subject = 'Thank You for your order!'
    # messaage = render_to_string('orders/order_recieved_email.html',{
    #     'user': request.user,
    #     'order':order,

    # })
    # to_mail = request.user.email
    # send_male = EmailMessage(mail_subject, messaage, to=[to_mail])
    # send_male.send()
    
    return JsonResponse({'status':"Your order has been placed successfully "})




def order_complete(request):
    order_number = request.GET.get('order_number')
    order = Order.objects.get(user=request.user, order_number=order_number)
    ordered_products = OrderProduct.objects.filter(order=order)
    total_amount = 0
    
    context = {
        'order':order,
        'ordered_products':ordered_products,

        'total_amount':total_amount,
    }
    return render(request, 'orders/payment_complete.html', context)




# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user
    
    #if the cart count is less than zero ,then redirect to shop
    
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect ('store')
    
    total=0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    
    if request.method == 'POST':
        form = OrderForm(request.POST)  
        if form.is_valid():
            
            #store all the billing information in the table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.adress_line_1 = form.cleaned_data['adress_line_1']
            data.adress_line_2 = form.cleaned_data['adress_line_2']
            data.pin_code = form.cleaned_data['pin_code']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            
            data.save()
            
            
            #generate order number
            
            yr = int(datetime.date.today().strftime('%y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%y%m%d")
            
            order_number = current_date + str(data.id)
            
            data.order_number = order_number
            
            data.save()
            
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            
            payment_mode = request.POST['payment_method']
            
            context = {
                'order': order,
                'cart_items': cart_items,
                'total' : total,
                'payment_mode':payment_mode,
            }
            return render(request,'orders/payments.html',context)
    
    else:
        return redirect('checkout')
        