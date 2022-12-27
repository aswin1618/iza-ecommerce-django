from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm ,UserForm,UserProfileForm,AdressForm
from .models import Account,UserProfile,UserAdress
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from carts.models import Cart,CartItem
from carts.views import _cart_id

#verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


from orders.models import Order,OrderProduct
# Create your views here.




def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            #USER ACTIVATION
            
            current_site = get_current_site(request)
            mail_subject = 'please activate your IZA account'
            message =render_to_string('accounts/account_verification_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_email =email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            #messages.success(request,'Thank you for registering with us. We have sent a verification email, please verify to continue shopping with us')
            
            
            
            #creating userprofile and useradress
            userprofile = UserProfile()
            userprofile.user = user
            userprofile.save()
            
            return redirect('/profile/signin/?command=verification&email='+email)
    else:
        form = RegistrationForm()
        
    # context = {
    #     'form': form
    # }
    return render(request,'accounts/signup.html',{"form": form})


#signin
def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        
        user = auth.authenticate(email=email, password=password)
        
        
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    # getting the product variation by cart_id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))
                        
                        
                    #Get the cart items from user to access his product variaton
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                            
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index= ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user =user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)  
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            
            auth.login(request, user)
            
            if user.is_superadmin == True   :
                return redirect('manager_dashboard')
            else:
                messages.success(request,'you are logged in')
                return redirect('home')
        else:
            messages.error(request,'invalid credentials')
            return redirect('signin')            
        
    return render(request,'accounts/login.html')

@login_required(login_url='signin')
def signout(request):   
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('home')

def activate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
    
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'account verification success')
        return redirect('signin')
    else:
        messages.error(request,'invalid activation link')
        return redirect('register')
    
#dashboard
@login_required(login_url='signin')
def dashboard(request):
    userprofile = get_object_or_404(UserProfile ,user=request.user)
    orders =Order.objects.order_by('-created_at').filter(user_id = request.user.id , is_ordered=True)
    orders_count = orders.count()
    context ={
        'userprofile': userprofile,
        'orders_count' : orders_count,
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='signin')    
def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact = email)
            
            #reset passwoed
            current_site = get_current_site(request)
            mail_subject = 'please reset your IZA password'
            message =render_to_string('accounts/reset_password_email.html', {
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            
            to_email =email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request,'please check your email')
            return redirect('signin')
            
        
        else:
            messages.error(request,'account does not exist')
            return redirect('forgotpassword')
            
        
    return render(request, 'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
        
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request,'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'link expired')
        return redirect('home')
    
    
@login_required(login_url='signin')   
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'password reset successful')
            return redirect('signin')
        else:
            messages.error(request,'passwords doesnt match')
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')
    
@login_required(login_url='signin')   
def my_orders(request):
    orders =Order.objects.filter(user = request.user , is_ordered=True).order_by('-created_at')
    context ={
        'orders' : orders,
    }
    return render(request,'accounts/my_order.html',context)

@login_required(login_url='signin')
def cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    if order.status =='Accepted':
        order.status = 'Cancelled'
        order.save()
    else:
        messages.error(request,'you cannot cancel now')
    return redirect('my_orders')


# user order details
@login_required(login_url='signin')
def order_detail(request, order_id):
    print(order_id)
    order = Order.objects.get(order_number=order_id)
    ordered_products = OrderProduct.objects.filter(order=order)
    total_amount = 0
    for item in ordered_products:
        total_amount += (item.product_price * item.quantity)
    context = {
        'order':order,
        'ordered_products':ordered_products,
        'total_amount':total_amount,
    }
    return render(request, 'accounts/order_detail.html', context)

@login_required(login_url='signin')
def edit_profile(request):
    
    userprofile = get_object_or_404(UserProfile ,user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form =UserProfileForm(request.POST, request.FILES, instance= userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your proile has been updated')
            return redirect('edit_profile')
        
        
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance= userprofile)
            
    context = {
        'user_form' :user_form,
        'profile_form' :profile_form,
        'userprofile' :userprofile
    }
    
    return render(request,'accounts/edit_profile.html',context)

@login_required(login_url='signin')
def user_adress(request):
    userprofile = get_object_or_404(UserProfile ,user=request.user)
    adress_list = UserAdress.objects.filter(user=userprofile)
    
    context = {
        'adress_list': adress_list,
    }
    
    return render(request,'accounts/adresses.html',context)


@login_required(login_url='signin')
def add_adress(request):
    userprofile = get_object_or_404(UserProfile ,user=request.user)
    if request.method == 'POST':
        form = AdressForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            adress_line_1 = form.cleaned_data['adress_line_1']
            adress_line_2 = form.cleaned_data['adress_line_2']
            pin_code = form.cleaned_data['pin_code']
            district = form.cleaned_data['district']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
        adress = UserAdress()
        adress.user= userprofile
        adress.phone = phone
        adress.adress_line_1 = adress_line_1
        adress.adress_line_2 = adress_line_2
        adress.pin_code = pin_code
        adress.district = district
        adress.city = city
        adress.state = state
        adress.save()
        return redirect('user_adress')
    else:
        form = AdressForm()
        return render(request,'accounts/add_adress.html',{"form": form})

    
    
@login_required(login_url='signin')
def edit_adress(request, adress_id):
    userprofile = get_object_or_404(UserProfile ,user=request.user)
    adress = UserAdress.objects.get(user= userprofile, id=adress_id)
    
    if request.method == 'POST': 
        adress_form = AdressForm(request.POST, user=request.user, instance=adress)
        if adress_form.is_valid():
            adress_form.save()
            messages.success(request,'your adress has been updated')
            return redirect('edit_adress')
     
    else:
        adress_form = AdressForm(instance= userprofile,id=adress_id)
            
    context = {
        'adress_form' :adress_form,
    }
    
    return render(request,'accounts/edit_adress.html',context)


@login_required(login_url='signin')
def remove_adress(request,adress_id):
    userprofile = get_object_or_404(UserProfile ,user=request.user)
    adress = UserAdress.objects.get(user= userprofile,id=adress_id)
    
    adress.delete()
    messages.warning(request,'adress has been deleted')
    return redirect('user_adress')



@login_required(login_url='signin')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']    
        new_password = request.POST['new_password']    
        confirm_new_password = request.POST['confirm_new_password']  
        
        user = Account.objects.get(username__iexact = request.user.username)
        if new_password == confirm_new_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request,'check your current password')
                return redirect('change_password')
                
        else:
            messages.error(request,'passwords doesnt match')
            return redirect('change_password')
        
    return render(request, 'accounts/change_password.html' )