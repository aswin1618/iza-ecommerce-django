from django.urls import path
from . import views

urlpatterns = [
    path('signin/',views.signin,name='signin'),
    path('register/',views.register,name='register'),
    path('signout/',views.signout,name='signout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    
    
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',views.resetpassword,name='resetpassword'),
    
    path('my_orders/',views.my_orders ,name='my_orders'),
    path('cancel-order/<int:order_number>', views.cancel_order, name='cancel_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    
    path('edit_profile/',views.edit_profile ,name='edit_profile'),
    path('user_adress/',views.user_adress ,name='user_adress'),
    path('add_adress/',views.add_adress ,name='add_adress'),
    path('edit_adress/<int:adress_id>/',views.edit_adress ,name='edit_adress'),
    path('remove_adress/<int:adress_id>/',views.remove_adress ,name='remove_adress'),
    path('change_password/',views.change_password ,name='change_password'),
    

  ] 