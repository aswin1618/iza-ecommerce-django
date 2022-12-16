from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required, user_passes_test
from user.models import Account,UserProfile,UserAdress
from store.models import Product,Variation
from orders.models import Order
from category.models import Category,SubCategory
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .forms import ProductForm,CategoryForm,SubCategoryForm,VariationForm

# Create your views here.



@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def manager_dashboard(request):
    if request.user.is_superadmin:

        user_count = Account.objects.filter(is_superadmin=False).count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.filter(is_ordered=True).count()
        category_count = Category.objects.all().count()
        variation_count = Variation.objects.all().count()
        

        context = {
            'user_count': user_count,
            'product_count': product_count,
            'order_count' : order_count,
            'category_count' : category_count,
            'variation_count' : variation_count,
        }

        return render(request,'manager/manager_dashboard.html',context)
    else:
        return redirect('home')

# Manage users
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def user_management(request):
    if request.method == "POST":
      key = request.POST['key']
      users = Account.objects.filter( Q(first_name__icontains=key) | Q(last_name__icontains=key) | Q(username__startswith=key) | Q(email__icontains=key), is_superadmin = False).order_by('id')
    else:
        users = Account.objects.filter(is_superadmin=False).order_by('id')

    paginator = Paginator(users,10)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
        'users' : paged_users
    }
    return render(request, 'manager/user_management.html',context)

@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def user_block(request, user_id):
  user = Account.objects.get(id=user_id)
  user.is_active = False
  user.save()
  return redirect('user_management')



@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='home')
def user_unblock(request, user_id):
  user = Account.objects.get(id=user_id)
  user.is_active= True
  user.save()
  return redirect('user_management')







#Manage product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def product_management(request):
  if request.method == "POST":
    key = request.POST['key']
    products = Product.objects.filter(Q(product_name__icontains=key) | Q(slug__startswith=key) | Q(SubCategory__category__category_name__startswith=key)).order_by('id')
  else:
    products = Product.objects.all().order_by('id')

  paginator = Paginator(products, 10)
  page = request.GET.get('page')
  paged_products = paginator.get_page(page)
  
  context = {
    'products': paged_products
  }
  return render(request, 'manager/product_management.html', context)


# Add Product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_product(request):
  if request.method == 'POST':
    print("hoi")
    form = ProductForm(request.POST, request.FILES)
    print("pooi")
    if form.is_valid():
      print("hai")
      form.save()
      return redirect('product_management')
    else:
      print(form.errors)
  else:
    form = ProductForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_product.html', context)



    
# Edit Product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def edit_product(request, product_id):
  product = Product.objects.get(id=product_id)
  form = ProductForm(instance=product)
  
  if request.method == 'POST':
    try:
      form = ProductForm(request.POST, request.FILES, instance=product)
      if form.is_valid():
        form.save()
        
        return redirect('product_management')
    
    except Exception as e:
      raise e

  context = {
    'product': product,
    'form': form
  }
  return render(request, 'manager/edit_product.html', context)


# Delete Product
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_product(request, product_id):
  product = Product.objects.get(id=product_id)
  product.delete()
  return redirect('product_management')




@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def category_management(request):
    categories = Category.objects.all().order_by('id')

    context = {
        'categories' :categories
    }

    return render(request, 'manager/category_management.html',context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_category(request):
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('category_management')

    else:
      messages.error(request, "Catergory with this same name already exists")
      return redirect('add_category')
  else:
    form = CategoryForm()
    context = {
      'form': form
    }
  return render(request, 'manager/add_category.html', context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_category(request, category_id):
  category = Category.objects.get(id=category_id)
  category.delete()
  return redirect('category_management')


# Update Category
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_category(request, category_id):
  category = Category.objects.get(id=category_id)
  form = CategoryForm(instance=category)
  
  if request.method == 'POST':
    try:
      form = CategoryForm(request.POST, instance=category)
      if form.is_valid():
        form.save()
        return redirect('category_management')
    
    except Exception as e:
      raise e

  context = {
    'category': category,
    'form': form
  }
  return render(request, 'manager/update_category.html', context)

# Sub category management
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def sub_category_management(request):
    sub_categories = SubCategory.objects.all().order_by('id')

    context = {
        'sub_categories' :sub_categories
    }

    return render(request, 'manager/sub_category_management.html',context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_sub_category(request):
  if request.method == 'POST':
    form = SubCategoryForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('sub_category_management')
  else:
    form = SubCategoryForm()
    context = {
      'form': form
    }
    return render(request, 'manager/add_sub_category.html', context)


@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_sub_category(request, sub_cat_id):
  sub_category = SubCategory.objects.get(id = sub_cat_id)
  form = SubCategoryForm(instance = sub_category)
  if request.method == 'POST':
    form = SubCategoryForm(request.POST, instance = sub_category)
    form.save()

    return redirect('sub_category_management')

  context = {
    'form' : form
  }
  return render(request, 'manager/update_sub_category.html', context)



@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_sub_category(request, sub_cat_id):
  sub_category = SubCategory.objects.get(id=sub_cat_id)
  sub_category.delete()
  return redirect('sub_category_management')




# Manage Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def order_management(request):
  if request.method =="POST":
    key = request.POST['key']
    orders = Order.objects.filter(Q(is_ordered=True), Q(order_number__icontains=key) | Q(user__email__icontains=key) | Q(first_name__startswith=key)).order_by('-id')
  else:
    orders = Order.objects.filter(is_ordered=True).order_by('-id')
    

  context = {
    'orders': orders
  }
  return render(request, 'manager/order_management.html', context)


# Accept Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def accept_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Shipped'
  order.save()
  
  return redirect('order_management')




# Complete Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def complete_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Delivered'
  order.save()
  
  return redirect('order_management')



# Cancel Order
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def manager_cancel_order(request, order_number):
  order = Order.objects.get(order_number=order_number)
  order.status = 'Cancelled'
  order.save()

  if request.user.is_admin:
    return redirect('admin_orders')

  else:
    return redirect('order_management')
  
  
# Manage Variation
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def variation_management(request):
  if request.method == 'POST':
    keyword = request.POST['keyword']
    variations = Variation.objects.filter(Q(product__product_name__icontains=keyword) | Q(product__sub_category__category__category_name__startswith=keyword) | Q(color__color_name__startswith=keyword | Q(size__size__startswith=keyword)).order_by('-id'))
  
  else:
    variations = Variation.objects.all().order_by('product')
  
  paginator = Paginator(variations, 10)
  page = request.GET.get('page')
  paged_variations = paginator.get_page(page)
  
  context = {
    'variations': paged_variations
  }
  return render(request, 'manager/variation_management.html', context)


# Add Variation
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def add_variation(request):
  
  if request.method == 'POST':
    form = VariationForm(request.POST)
    if form.is_valid():
      variation_stock = form.cleaned_data['stock']
      variation_product = form.cleaned_data['product']
      form.save()
      #adding the stock
      product = Product.objects.get(product_name=variation_product)
      product.stock = product.stock +variation_stock
      product.save()
      return redirect('variation_management')
  
  else:
    form = VariationForm()
    
  
  
  context = {
    'form': form
  }
  return render(request, 'manager/add_variation.html', context)



# update variation 
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def update_variation(request, variation_id):
  variation = Variation.objects.get(id = variation_id)
  initial_var_stock = variation.stock
  if request.method == 'POST':
    form = VariationForm(request.POST, instance = variation)
    if form.is_valid():
      updated_var_stock = form.cleaned_data['stock']
      variation_product = form.cleaned_data['product']
      form.save()
      
      product = Product.objects.get(product_name=variation_product)
      product.stock = product.stock-initial_var_stock
      product.stock = product.stock+updated_var_stock
      product.save()
      return redirect('variation_management')
  else:
    form = VariationForm(instance = variation)

  context = {
    'form':form,
    'variation':variation
  }

  return render(request, 'manager/update_variation.html', context)


# delete variation 
@never_cache
@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_admin, login_url='index')
def delete_variation(request, variation_id):
  variation = Variation.objects.get(id = variation_id)
  variation_stock = variation.stock
  variation_product = variation.product
  variation.delete()
  product = Product.objects.get(product_name=variation_product)
  product.stock = product.stock - variation_stock
  product.save()
  return redirect('variation_management')
