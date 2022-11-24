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
    

  ] 