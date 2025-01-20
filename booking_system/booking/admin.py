from django.contrib import admin
from .models import Booking, Room



# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'room', 'check_in_date', 'check_out_date', 'total_price', 'payment_status')
    list_filter = ('room', 'payment_status', 'check_in_date')
    search_fields = ('guest_name', 'guest_email', 'guest_phone')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'price_per_night', 'is_available')
    list_filter = ('room_type', 'is_available')
    search_fields = ('room_number', 'room_type')