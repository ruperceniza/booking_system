from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Room, Booking, Payment
from .forms import BookingForm, PaymentForm
from django.contrib import messages



def home(request):
    return HttpResponse("OHA Travellers Inn Online Booking System")

def rooms_list(request):
    rooms = Room.objects.all()
    return render(request, 'booking/rooms_list.html', {'rooms':rooms})

def bookings_list(request):
    bookings = Booking.objects.all()
    return render(request, 'booking/bookings_list.html', {'bookings': bookings})

def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            if booking.check_in_date and booking.check_out_date:
                num_nights = (booking.check_out_date - booking.check_in_date).days

                if num_nights > 0:
                    room = booking.room
                    booking.total_price = num_nights * room.price_per_night
                    booking.save()
                    return redirect('process_payment', booking_id=booking.id)
                else:
                    messages.error(request, "Check-out date mustbe after check-in date.")
            else:
                messages.error(request, "Both check-in and check-out dates are required.")
    else:
        form = BookingForm()

    return render(request, 'booking/create_booking.html', {'form': form})

def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.save()

            booking.payment_status = 'Paid'
            booking.save()

            return redirect('bookings_list')
    else:
        form = PaymentForm()
    
    return render(request, 'booking/process_payment.html', {'form': form, 'booking' : booking})