from django.urls import path
from .views import BookingListView, BookingDetailView, BookingCreateView, BookingUpdateView

urlpatterns = [
    path('', BookingListView.as_view(), name='booking_list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('add/', BookingCreateView.as_view(), name='booking_add'),
    path('<int:pk>/edit/', BookingUpdateView.as_view(), name='booking_edit'),
]
