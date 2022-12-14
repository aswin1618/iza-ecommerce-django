from django.urls import path
from . import views

urlpatterns = [
    path('',views.wishlist, name='wishlist'),
    path('add_wish/<int:product_id>/',views.add_wish, name='add_wish'),
    path('remove_wish_item/<int:product_id>/<int:wishlist_item_id>/',views.remove_wish_item, name='remove_wish_item'),
    
    
]