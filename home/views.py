from django.shortcuts import render ,get_object_or_404 ,redirect
from category.models import Category , SubCategory
from store.models import Product,Variation, Banner,ProductAttributes,ReviewRatings
from orders.models import OrderProduct
from carts.views import _cart_id
from django.db.models import Q
from carts.models import CartItem
from django.core.paginator import Paginator
from store.forms import ReviewForm
from django.contrib import messages

# Create your views here.
def home(request):


    banners = Banner.objects.all()
    categories = Category.objects.all()
    products = Product.objects.all().filter(is_available = True).order_by('-created_date')
    featured_products = Product.objects.all().filter(is_available = True,is_featured=True).order_by('id')
    context = {
        'products' : products,
        'categories' : categories,
        'banners' :banners,
        'featured_products' :featured_products
    }

    return render(request,'home.html',context)


def store(request,category_slug = None,SubCategory_slug = None):
    categories = None
    subcategories = None
    products = None

    if category_slug != None and SubCategory_slug!= None :
        categories = get_object_or_404( Category, slug = category_slug)
        subcategories = get_object_or_404(SubCategory, slug= SubCategory_slug)
        products   = Product.objects.filter(category = categories,SubCategory=subcategories).order_by('id')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        
    elif category_slug != None:
        categories = get_object_or_404( Category, slug = category_slug)
        products   = Product.objects.filter(category = categories).order_by('id')
        subcategories = SubCategory.objects.filter(category_name=categories).values('subcat_name')
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    else:
        return redirect('home')

    sub_categories = SubCategory.objects.all().filter(category_name = categories)
    
    #brands =  Product.objects.filter(category=categories).values('brand').distinct()
    
    context = {
        'products' : paged_products,
        'sub_categories' :sub_categories,
    }

    return render(request, 'shop.html',context)

def product_detail(request,category_slug,SubCategory_slug, product_slug):
    try:
        
        single_product = Product.objects.get(category__slug =category_slug, SubCategory__slug= SubCategory_slug,slug = product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request),product = single_product).exists()
        colors = Variation.objects.filter(product=single_product).values('color').distinct()
        sizes = Variation.objects.filter(product=single_product).values('size').distinct()
        product_attributes = ProductAttributes.objects.get(product=single_product)
    except Exception as e:
        raise e
    
    
    if request.user.is_authenticated:
        try:
            order_product = OrderProduct.objects.filter(user=request.user, product_id= single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product=None
    else:    
        order_product=None    
    # get the reviews
    reviews = ReviewRatings.objects.filter(product_id = single_product.id, status=True)
    context={
        'product_attributes':product_attributes,
        'single_product' : single_product,
        'in_cart' : in_cart,
        'colors' : colors,
        'sizes' : sizes,
        'order_product': order_product,
        'reviews':reviews
    }
    return render(request,'product_detail.html',context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            context = {
                'products' : products
            }

            return render(request, 'shop.html', context)
        else:
            return render(request, 'shop.html')


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRatings.objects.get(user__id=request.user.id, product__id= product_id)
            form = ReviewForm(request.POST,instance =reviews)
            form.save()
            messages.success(request,'Thankyou, Your Review Has been updated')
            return redirect(url)
        except ReviewRatings.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject'] 
                rating = form.cleaned_data['rating'] 
                review = form.cleaned_data['review']     
            data= ReviewRatings()
            data.subject = subject 
            data.rating = rating 
            data.review = review
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id = product_id
            data.user_id = request.user.id
            data.save()
            messages.success(request,'Thankyou, Your Review Has been submitted')
            return redirect(url)
            
    