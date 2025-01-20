from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Room(models.Model):
    ROOM_TYPES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite/Family'),
    ]

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}" 

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=15)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Ensure no null values
    payment_status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid'),
            ('Cancelled', 'Cancelled'),
        ],
        default='Pending',
    )


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('Gcash', 'Gcash'),
        ('Bank Transfer', 'Bank Transfer'),
    ]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - Amount: {self.amount_paid}"  

@receiver(post_save, sender=Booking)
def update_room_availability(sender, instance, **kwargs):
    instance.room.is_available = False
    instance.room.save()
