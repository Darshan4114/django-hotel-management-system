from django.urls import path
from .views import RoomListView, BookingListView, RoomDetailView, CancelBookingView, checkout_view, success_view, cancel_view

app_name = 'hotel'

urlpatterns = [
    path('', RoomListView, name='RoomListView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(),
         name='CancelBookingView'),
    path('checkout/', checkout_view, name='checkout_view'),
    path('success/', success_view, name='success_view'),
    path('cancel/', cancel_view, name='cancel_view'),

]
