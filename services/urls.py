from django.urls import path
from .views import (
    home, login_view, logout_view, client_dashboard,
    ServiceListView, ServiceCreateView, ServiceUpdateView,
    appointment_create, payment_create
)

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', client_dashboard, name='client_dashboard'),
    
    # Admin routes
    path('services/', ServiceListView.as_view(), name='service_list'),
    path('services/new/', ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_update'),
    
    # Client routes
    path('services/<int:service_id>/book/', appointment_create, name='appointment_create'),
    path('appointments/<int:appointment_id>/pay/', payment_create, name='payment_create'),
]
