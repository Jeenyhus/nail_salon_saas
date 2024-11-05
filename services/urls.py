from django.urls import path, include
from . import views


urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('book/<int:service_id>/', views.book_appointment, name='book_appointment'),
    path('confirm/<int:appointment_id>/', views.confirm_booking, name='confirm_booking'),
    path('pay/<int:appointment_id>/', views.complete_payment, name='complete_payment'),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('accounts/signup/', views.signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    

]
