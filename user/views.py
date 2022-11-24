from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.models import Cart,CartItem
from carts.views import _cart_id

#verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string 
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode 
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

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
    return render(request,'accounts/dashboard.html')
    
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