from django.urls import path
from . import views

urlpatterns = [
    path('manager_dashboard/',views.manager_dashboard,name='manager_dashboard'),
    
    path('user_management/',views.user_management,name='user_management'),
    path('user_block/<int:user_id>/',views.user_block,name='user_block'),
    path('user_unblock/<int:user_id>/',views.user_unblock,name='user_unblock'),
    
    
    path('product_management/',views.product_management,name='product_management'),
    path('add_product/',views.add_product,name='add_product'),
    path('delete_product/<int:product_id>/',views.delete_product,name='delete_product'),
    path('edit_product/<int:product_id>/',views.edit_product,name='edit_product'),
    
    path('category_management/',views.category_management,name='category_management'),
    path('add_category',views.add_category,name='add_category'),
    path('delete_category/<int:category_id>/',views.delete_category,name='delete_category'),
    path('update_category/<int:category_id>/', views.update_category, name="update_category"),
    
    path('sub_category_management/',views.sub_category_management,name='sub_category_management'),
    path('add_sub_category',views.add_sub_category,name='add_sub_category'),
    path('update_sub_category/<int:sub_cat_id>/',views.update_sub_category,name='update_sub_category'),
    path('delete_sub_category/<int:sub_cat_id>/',views.delete_sub_category,name='delete_sub_category'),
    
    path('order_management/',views.order_management,name='order_management'),
    path('manager_cancel_order/<int:order_number>/', views.manager_cancel_order, name='manager_cancel_order'),
    path('accept_order/<int:order_number>/', views.accept_order, name='accept_order'),
    path('complete_order/<int:order_number>/', views.complete_order, name='complete_order'),
    
    path('variation_management/',views.variation_management,name='variation_management'),
    path('add_variation/', views.add_variation, name='add_variation'),
    path('update_variation/<int:variation_id>/',views.update_variation,name='update_variation'),
    path('delete_variation/<int:variation_id>/', views.delete_variation, name='delete_variation'),
    
    path('offer_management/',views.offer_management,name='offer_management'),
    path('subcategory_offer/',views.subcategory_offer,name='subcategory_offer'),
    path('remove_sub_offer/<int:offer_id>/',views.remove_sub_offer,name='remove_sub_offer'),
    # path('edit_sub_offer/',views.edit_sub_offer,name='edit_sub_offer'),
    path('brand_offer/',views.brand_offer,name='brand_offer'),
    path('remove_brand_offer/<int:offer_id>/',views.remove_brand_offer,name='remove_brand_offer'),
    # path('edit_brand_offer/',views.edit_brand_offer,name='edit_brand_offer'),
    
    path('add_sub_offer/',views.add_sub_offer,name='add_sub_offer'),
    path('add_brand_offer/',views.add_brand_offer,name='add_brand_offer'),
    
    
    path('sales_dashboard/',views.sales_dashboard,name='sales_dashboard'),
    
    
]