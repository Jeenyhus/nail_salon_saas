from django.urls import path
from .views import CustomerListView, CustomerDetailView, CustomerCreateView, CustomerUpdateView

urlpatterns = [
    path('', CustomerListView.as_view(), name='customer_list'),
    path('<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('add/', CustomerCreateView.as_view(), name='customer_add'),
    path('<int:pk>/edit/', CustomerUpdateView.as_view(), name='customer_edit'),
]
