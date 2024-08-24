from django.urls import path
from .import views

urlpatterns = [
    path('', views.home,name='home'),
    path('register', views.register,name='register'),
    path('log_in', views.log_in,name='log_in'),
    path('log_out', views.log_out,name='log_out'),
    path('verify_otp', views.verify_otp, name='verify_otp'),
    path('create_service', views.create_service, name='create_service'),
    path('list_service', views.list_service, name='list_service'),
    path('update_service/<int:pk>/', views.update_service, name='update_service'),
    path('delete_service/<int:pk>/', views.delete_service, name='delete_service'),
    path('services/<int:service_id>/subscribe/', views.subscribe, name='subscribe'),
    path('services/<int:service_id>/buy/<int:subscription_id>/', views.buy_service, name='buy_service'),
    path('razorpay/callback/', views.razorpay_callback, name='razorpay_callback'),
]