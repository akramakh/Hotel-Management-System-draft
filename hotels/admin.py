from django.contrib import admin
from .models import Hotel, Room, Classification, Reservation
# Register your models here.

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Classification)
admin.site.register(Reservation)
