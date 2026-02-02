# bookings/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from datetime import date, datetime
from accounts.decorators import customer_required
from .models import Booking, HotelBookingDetail, FlightBookingDetail, Passenger
from .forms import (
    HotelSearchForm, HotelBookingForm,
    FlightSearchForm, FlightBookingForm,
    PassengerFormSet
)
from partners.models import Hotel, RoomType, Flight
from utils.db_manager import BookingQueries, HotelQueries


# Hotel Booking Views
def hotel_search(request):
    """
    Search for hotels
    """
    form = HotelSearchForm(request.GET or None)
    hotels = Hotel.objects.filter(is_active=True)

    if form.is_valid():
        city = form.cleaned_data.get('city')
        if city:
            hotels = hotels.filter(city__icontains=city)

    context = {
        'form': form,
        'hotels': hotels,
    }

    return render(request, 'bookings/hotels/search.html', context)


def hotel_detail(request, hotel_id):
    """
    View hotel details and available room types
    """
    hotel = get_object_or_404(Hotel, id=hotel_id, is_active=True)
    room_types = hotel.room_types.filter(is_active=True)

    context = {
        'hotel': hotel,
        'room_types': room_types,
    }

    return render(request, 'bookings/hotels/detail.html', context)


@login_required
@customer_required
def hotel_booking_create(request, room_type_id):
    """
    Create a hotel booking
    """
    room_type = get_object_or_404(RoomType, id=room_type_id, is_active=True)
    hotel = room_type.hotel

    if request.method == 'POST':
        form = HotelBookingForm(request.POST)

        if form.is_valid():
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            number_of_rooms = form.cleaned_data['number_of_rooms']
            number_of_guests = form.cleaned_data['number_of_guests']
            notes = request.POST.get('notes', '')

            # Calculate number of nights
            nights = (check_out_date - check_in_date).days

            # Check availability
            if room_type.rooms_available < number_of_rooms:
                messages.error(request, f'Only {room_type.rooms_available} rooms available.')
                return redirect('bookings:hotel_booking_create', room_type_id=room_type.id)

            # Check max occupancy
            if number_of_guests > (room_type.max_occupancy * number_of_rooms):
                messages.error(request,
                               f'Maximum occupancy exceeded. Each room can accommodate {room_type.max_occupancy} guests.')
                return redirect('bookings:hotel_booking_create', room_type_id=room_type.id)

            # Calculate total
            total_amount = room_type.price_per_night * nights * number_of_rooms

            # Create booking with transaction
            try:
                with transaction.atomic():
                    # Create main booking
                    booking = Booking.objects.create(
                        user=request.user,
                        booking_type='hotel',
                        status='pending',
                        total_amount=total_amount,
                        notes=notes
                    )

                    # Create hotel booking details
                    HotelBookingDetail.objects.create(
                        booking=booking,
                        hotel=hotel,
                        room_type=room_type,
                        check_in_date=check_in_date,
                        check_out_date=check_out_date,
                        number_of_rooms=number_of_rooms,
                        number_of_guests=number_of_guests,
                        price_per_night=room_type.price_per_night,
                        number_of_nights=nights
                    )

                    # Update room availability
                    room_type.rooms_available -= number_of_rooms
                    room_type.save()

                    # NEW: Redirect to payment page instead of booking detail
                    messages.success(request,
                                     'Booking created successfully! Please complete payment to confirm your reservation.')
                    return redirect('payments:payment_page', booking_id=booking.booking_id)

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('bookings:hotel_booking_create', room_type_id=room_type.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HotelBookingForm()

    context = {
        'form': form,
        'room_type': room_type,
        'hotel': hotel,
    }

    return render(request, 'bookings/hotels/booking_form.html', context)


# Flight Booking Views
def flight_search(request):
    """
    Search for flights
    """
    form = FlightSearchForm(request.GET or None)
    flights = Flight.objects.filter(is_active=True, departure_time__gte=datetime.now())

    if form.is_valid():
        origin = form.cleaned_data.get('origin')
        destination = form.cleaned_data.get('destination')
        departure_date = form.cleaned_data.get('departure_date')

        if origin:
            flights = flights.filter(origin__icontains=origin)
        if destination:
            flights = flights.filter(destination__icontains=destination)
        if departure_date:
            flights = flights.filter(departure_time__date=departure_date)

    context = {
        'form': form,
        'flights': flights,
    }

    return render(request, 'bookings/flights/search.html', context)


def flight_detail(request, flight_id):
    """
    View flight details
    """
    flight = get_object_or_404(Flight, id=flight_id, is_active=True)

    context = {
        'flight': flight,
    }

    return render(request, 'bookings/flights/detail.html', context)


@login_required
@customer_required
def flight_booking_create(request, flight_id):
    """
    Create a flight booking
    """
    flight = get_object_or_404(Flight, id=flight_id, is_active=True)

    if request.method == 'POST':
        form = FlightBookingForm(request.POST)
        passenger_formset = PassengerFormSet(request.POST, prefix='passengers')

        if form.is_valid() and passenger_formset.is_valid():
            number_of_passengers = form.cleaned_data['number_of_passengers']
            notes = request.POST.get('notes', '')

            # Validate number of passenger forms matches number_of_passengers
            valid_passengers = [f for f in passenger_formset if
                                f.cleaned_data and not f.cleaned_data.get('DELETE', False)]
            if len(valid_passengers) != number_of_passengers:
                messages.error(request, f'Please provide information for exactly {number_of_passengers} passengers.')
                return render(request, 'bookings/flights/booking_form.html', {
                    'form': form,
                    'passenger_formset': passenger_formset,
                    'flight': flight,
                })

            # Check seat availability
            if flight.seats_available < number_of_passengers:
                messages.error(request, f'Only {flight.seats_available} seats available.')
                return redirect('bookings:flight_booking_create', flight_id=flight.id)

            # Calculate total
            total_amount = flight.price * number_of_passengers

            # Create booking with transaction
            try:
                with transaction.atomic():
                    # Create main booking
                    booking = Booking.objects.create(
                        user=request.user,
                        booking_type='flight',
                        status='pending',
                        total_amount=total_amount,
                        notes=notes
                    )

                    # Create flight booking details
                    flight_booking = FlightBookingDetail.objects.create(
                        booking=booking,
                        flight=flight,
                        number_of_passengers=number_of_passengers,
                        price_per_seat=flight.price
                    )

                    # Create passenger records
                    for passenger_form in valid_passengers:
                        passenger_data = passenger_form.cleaned_data
                        Passenger.objects.create(
                            flight_booking=flight_booking,
                            title=passenger_data['title'],
                            first_name=passenger_data['first_name'],
                            last_name=passenger_data['last_name'],
                            date_of_birth=passenger_data['date_of_birth'],
                            passport_number=passenger_data.get('passport_number', '')
                        )

                    # Update seat availability
                    flight.seats_available -= number_of_passengers
                    flight.save()

                    # NEW: Redirect to payment page instead of booking detail
                    messages.success(request,
                                     'Flight booking created successfully! Please complete payment to confirm your ticket.')
                    return redirect('payments:payment_page', booking_id=booking.booking_id)

            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('bookings:flight_booking_create', flight_id=flight.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FlightBookingForm()
        passenger_formset = PassengerFormSet(prefix='passengers')

    context = {
        'form': form,
        'passenger_formset': passenger_formset,
        'flight': flight,
    }

    return render(request, 'bookings/flights/booking_form.html', context)


# Booking Management Views
@login_required
def my_bookings(request):
    """
    View all bookings for current user
    """
    bookings = Booking.objects.filter(user=request.user).select_related(
        'hotel_details__hotel',
        'hotel_details__room_type',
        'flight_details__flight'
    ).prefetch_related('payment')  # NEW: Add payment prefetch

    context = {
        'bookings': bookings,
    }

    return render(request, 'bookings/my_bookings.html', context)


@login_required
def booking_detail(request, booking_id):
    """
    View booking details
    """
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    # NEW: Check if payment exists
    has_payment = hasattr(booking, 'payment')
    payment_completed = has_payment and booking.payment.status == 'completed'

    context = {
        'booking': booking,
        'has_payment': has_payment,  # NEW
        'payment_completed': payment_completed,  # NEW
    }

    return render(request, 'bookings/booking_detail.html', context)


@login_required
def booking_cancel(request, booking_id):
    """
    Cancel a booking
    """
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    if booking.status in ['cancelled', 'completed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:booking_detail', booking_id=booking.booking_id)


    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Update booking status
                booking.status = 'cancelled'
                booking.save()

                # Restore availability
                if booking.booking_type == 'hotel':
                    hotel_details = booking.hotel_details
                    hotel_details.room_type.rooms_available += hotel_details.number_of_rooms
                    hotel_details.room_type.save()
                elif booking.booking_type == 'flight':
                    flight_details = booking.flight_details
                    flight_details.flight.seats_available += flight_details.number_of_passengers
                    flight_details.flight.save()

                messages.success(request, 'Booking cancelled successfully.')
                return redirect('bookings:my_bookings')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'bookings/booking_cancel.html', {'booking': booking})


@login_required
@customer_required
def cancel_booking(request, booking_id):
    """
    Cancel a booking (simplified version for quick cancel from my_bookings)
    """
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)
    
    # Check if booking can be cancelled
    if booking.status in ['cancelled', 'completed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:booking_detail', booking_id=booking.booking_id)
    
    # Cancel the booking
    booking.status = 'cancelled'
    booking.save()
    
    # Restore availability
    if booking.booking_type == 'hotel':
        hotel_detail = booking.hotel_details
        hotel_detail.room_type.rooms_available += hotel_detail.number_of_rooms
        hotel_detail.room_type.save()
    elif booking.booking_type == 'flight':
        flight_detail = booking.flight_details
        flight_detail.flight.seats_available += flight_detail.passengers.count()
        flight_detail.flight.save()
    
    messages.success(request, 'Booking cancelled successfully.')
    return redirect('bookings:my_bookings')


# ============================================
# Raw SQL Views (Alternative to ORM)
# ============================================

@login_required
def my_bookings_raw_sql(request):
    """
    My bookings using raw SQL instead of ORM
    """
    # Get bookings using raw SQL
    bookings = BookingQueries.get_user_bookings(request.user.id)
    
    # For each booking, get details
    for booking in bookings:
        if booking['booking_type'] == 'hotel':
            booking['details'] = BookingQueries.get_hotel_booking_details(booking['booking_id'])
    
    context = {
        'bookings': bookings
    }
    return render(request, 'bookings/my_bookings.html', context)


def hotel_search_raw_sql(request):
    """
    Hotel search using raw SQL
    """
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Search using raw SQL
    hotels = HotelQueries.search_hotels(city, min_price, max_price)
    
    context = {
        'hotels': hotels,
        'search_city': city,
    }
    return render(request, 'bookings/hotel_search.html', context)
