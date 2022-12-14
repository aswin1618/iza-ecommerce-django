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
    path('edit_profile/',views.edit_profile ,name='edit_profile'),
    path('edit_adress/',views.edit_adress ,name='edit_adress'),
    path('change_password/',views.change_password ,name='change_password'),
    

  ] 