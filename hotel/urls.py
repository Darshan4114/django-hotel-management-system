from django.urls import path
from .views import RoomListView, BookingList, BookingView, RoomDetailView

app_name = 'hotel'

urlpatterns = [
    path('room_list/', RoomListView, name='RoomList'),
    path('booking_list/', BookingList.as_view(), name='BookingList'),
    path('book/', BookingView.as_view(), name='BookingView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),


]
