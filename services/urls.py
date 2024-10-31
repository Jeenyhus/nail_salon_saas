from django.urls import path
from .views import ServiceListView, ServiceDetailView, ServiceCreateView, ServiceUpdateView

urlpatterns = [
    path('', ServiceListView.as_view(), name='service_list'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('add/', ServiceCreateView.as_view(), name='service_add'),
    path('<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_edit'),
]
