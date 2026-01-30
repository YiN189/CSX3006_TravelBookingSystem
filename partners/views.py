# partners/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import partner_required
from .models import Partner, Hotel, RoomType, Flight
from .forms import PartnerProfileForm, HotelForm, RoomTypeForm, FlightForm


@login_required
@partner_required
def partner_dashboard(request):
    """
    Partner dashboard overview
    """
    # Get or create partner profile
    partner, created = Partner.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'contact_email': request.user.email,
        }
    )

    context = {
        'partner': partner,
        'total_hotels': partner.hotels.count(),
        'active_hotels': partner.hotels.filter(is_active=True).count(),
        'total_flights': partner.flights.count(),
        'active_flights': partner.flights.filter(is_active=True).count(),
    }

    return render(request, 'partners/dashboard.html', context)


@login_required
@partner_required
def partner_profile(request):
    """
    Partner profile management
    """
    partner, created = Partner.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.username,
            'contact_email': request.user.email,
        }
    )

    if request.method == 'POST':
        form = PartnerProfileForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, 'Partner profile updated successfully!')
            return redirect('partners:partner_profile')
    else:
        form = PartnerProfileForm(instance=partner)

    return render(request, 'partners/profile.html', {'form': form, 'partner': partner})


# Hotel Management Views
@login_required
@partner_required
def hotel_list(request):
    """
    List all hotels for the current partner
    """
    partner = Partner.objects.get(user=request.user)
    hotels = partner.hotels.all()

    return render(request, 'partners/hotels/list.html', {'hotels': hotels, 'partner': partner})


@login_required
@partner_required
def hotel_create(request):
    """
    Create a new hotel
    """
    partner = Partner.objects.get(user=request.user)

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.partner = partner
            hotel.save()
            messages.success(request, f'Hotel "{hotel.name}" created successfully!')
            return redirect('partners:hotel_list')
    else:
        form = HotelForm()

    return render(request, 'partners/hotels/form.html', {'form': form, 'title': 'Add New Hotel'})


@login_required
@partner_required
def hotel_edit(request, hotel_id):
    """
    Edit an existing hotel
    """
    partner = Partner.objects.get(user=request.user)
    hotel = get_object_or_404(Hotel, id=hotel_id, partner=partner)

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, instance=hotel)
        if form.is_valid():
            form.save()
            messages.success(request, f'Hotel "{hotel.name}" updated successfully!')
            return redirect('partners:hotel_list')
    else:
        form = HotelForm(instance=hotel)

    return render(request, 'partners/hotels/form.html', {
        'form': form,
        'title': f'Edit Hotel: {hotel.name}',
        'hotel': hotel
    })


@login_required
@partner_required
def hotel_delete(request, hotel_id):
    """
    Delete a hotel
    """
    partner = Partner.objects.get(user=request.user)
    hotel = get_object_or_404(Hotel, id=hotel_id, partner=partner)

    if request.method == 'POST':
        hotel_name = hotel.name
        hotel.delete()
        messages.success(request, f'Hotel "{hotel_name}" deleted successfully!')
        return redirect('partners:hotel_list')

    return render(request, 'partners/hotels/delete.html', {'hotel': hotel})


# Room Type Management Views
@login_required
@partner_required
def room_type_list(request, hotel_id):
    """
    List all room types for a specific hotel
    """
    partner = Partner.objects.get(user=request.user)
    hotel = get_object_or_404(Hotel, id=hotel_id, partner=partner)
    room_types = hotel.room_types.all()

    return render(request, 'partners/rooms/list.html', {
        'hotel': hotel,
        'room_types': room_types
    })


@login_required
@partner_required
def room_type_create(request, hotel_id):
    """
    Create a new room type
    """
    partner = Partner.objects.get(user=request.user)
    hotel = get_object_or_404(Hotel, id=hotel_id, partner=partner)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST, request.FILES)
        if form.is_valid():
            room_type = form.save(commit=False)
            room_type.hotel = hotel
            room_type.save()
            messages.success(request, f'Room type "{room_type.name}" created successfully!')
            return redirect('partners:room_type_list', hotel_id=hotel.id)
    else:
        form = RoomTypeForm()

    return render(request, 'partners/rooms/form.html', {
        'form': form,
        'hotel': hotel,
        'title': 'Add New Room Type'
    })


@login_required
@partner_required
def room_type_edit(request, hotel_id, room_id):
    """
    Edit an existing room type
    """
    partner = Partner.objects.get(user=request.user)
    hotel = get_object_or_404(Hotel, id=hotel_id, partner=partner)
    room_type = get_object_or_404(RoomType, id=room_id, hotel=hotel)

    if request.method == 'POST':
        form = RoomTypeForm(request.POST, request.FILES, instance=room_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room type "{room_type.name}" updated successfully!')
            return redirect('partners:room_type_list', hotel_id=hotel.id)
    else:
        form = RoomTypeForm(instance=room_type)

    return render(request, 'partners/rooms/form.html', {
        'form': form,
        'hotel': hotel,
        'title': f'Edit Room Type: {room_type.name}',
        'room_type': room_type
    })


@login_required
@partner_required
def room_type_delete(request, hotel_id, room_id):
    """
    Delete a room type
    """
    partner = Partner.objects.get(user=request.user)
    hotel = get_object_or_404(Hotel, id=hotel_id, partner=partner)
    room_type = get_object_or_404(RoomType, id=room_id, hotel=hotel)

    if request.method == 'POST':
        room_name = room_type.name
        room_type.delete()
        messages.success(request, f'Room type "{room_name}" deleted successfully!')
        return redirect('partners:room_type_list', hotel_id=hotel.id)

    return render(request, 'partners/rooms/delete.html', {
        'hotel': hotel,
        'room_type': room_type
    })


# Flight Management Views
@login_required
@partner_required
def flight_list(request):
    """
    List all flights for the current partner
    """
    partner = Partner.objects.get(user=request.user)
    flights = partner.flights.all()

    return render(request, 'partners/flights/list.html', {'flights': flights, 'partner': partner})


@login_required
@partner_required
def flight_create(request):
    """
    Create a new flight
    """
    partner = Partner.objects.get(user=request.user)

    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.partner = partner
            flight.save()
            messages.success(request, f'Flight "{flight.flight_number}" created successfully!')
            return redirect('partners:flight_list')
    else:
        form = FlightForm()

    return render(request, 'partners/flights/form.html', {'form': form, 'title': 'Add New Flight'})


@login_required
@partner_required
def flight_edit(request, flight_id):
    """
    Edit an existing flight
    """
    partner = Partner.objects.get(user=request.user)
    flight = get_object_or_404(Flight, id=flight_id, partner=partner)

    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES, instance=flight)
        if form.is_valid():
            form.save()
            messages.success(request, f'Flight "{flight.flight_number}" updated successfully!')
            return redirect('partners:flight_list')
    else:
        form = FlightForm(instance=flight)

    return render(request, 'partners/flights/form.html', {
        'form': form,
        'title': f'Edit Flight: {flight.flight_number}',
        'flight': flight
    })


@login_required
@partner_required
def flight_delete(request, flight_id):
    """
    Delete a flight
    """
    partner = Partner.objects.get(user=request.user)
    flight = get_object_or_404(Flight, id=flight_id, partner=partner)

    if request.method == 'POST':
        flight_number = flight.flight_number
        flight.delete()
        messages.success(request, f'Flight "{flight_number}" deleted successfully!')
        return redirect('partners:flight_list')

    return render(request, 'partners/flights/delete.html', {'flight': flight})
