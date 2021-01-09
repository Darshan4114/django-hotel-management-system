from django.contrib import admin
from .models import Room, Booking, RoomCategory, Person

# Register your models here.
admin.site.register(RoomCategory)
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Person)
