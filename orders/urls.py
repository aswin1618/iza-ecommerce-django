from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order, name='place_order'),
    path('payments/',views.payments, name='payments'),
    path('order_complete', views.order_complete, name='order_complete'),
    
    
    path('pdf_download/<int:order_id>', views.DownloadPDF.as_view(), name="pdf_download"),
  ]  