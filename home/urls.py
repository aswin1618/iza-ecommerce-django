from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('store',views.store,name='store'),
    path('store/<slug:category_slug>/',views.store, name='products_by_category'),
    path('store/<slug:category_slug>/<slug:SubCategory_slug>/',views.store, name='products_by_subcategory'),
    path('store/<slug:category_slug>/<slug:SubCategory_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>',views.submit_review,name='submit_review'),

  ]  