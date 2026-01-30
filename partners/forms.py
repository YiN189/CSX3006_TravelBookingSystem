# partners/forms.py

from django import forms
from .models import Partner, Hotel, RoomType, Flight

class PartnerProfileForm(forms.ModelForm):
    """
    Form for partner to update their profile
    """
    class Meta:
        model = Partner
        fields = ['name', 'partner_type', 'description', 'logo', 'website', 'contact_email', 'contact_phone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'partner_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class HotelForm(forms.ModelForm):
    """
    Form for creating/updating hotels
    """
    class Meta:
        model = Hotel
        fields = [
            'name', 'city', 'address', 'description', 'star_rating',
            'main_image', 'amenities', 'check_in_time', 'check_out_time',
            'email', 'phone', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'star_rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'amenities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'e.g., WiFi, Pool, Gym, Restaurant, Parking'
            }),
            'check_in_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RoomTypeForm(forms.ModelForm):
    """
    Form for creating/updating room types
    """
    class Meta:
        model = RoomType
        fields = [
            'name', 'description', 'price_per_night', 'max_occupancy',
            'rooms_available', 'room_size', 'bed_type', 'amenities',
            'image', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'max_occupancy': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'rooms_available': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'room_size': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bed_type': forms.TextInput(attrs={'class': 'form-control'}),
            'amenities': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'e.g., TV, Mini Bar, Safe, Bathtub'
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FlightForm(forms.ModelForm):
    """
    Form for creating/updating flights
    """
    class Meta:
        model = Flight
        fields = [
            'flight_number', 'origin', 'destination', 'departure_time',
            'arrival_time', 'price', 'seats_available', 'total_seats',
            'aircraft_type', 'airline_logo', 'class_type', 'is_active'
        ]
        widgets = {
            'flight_number': forms.TextInput(attrs={'class': 'form-control'}),
            'origin': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'departure_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'arrival_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'seats_available': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'total_seats': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'aircraft_type': forms.TextInput(attrs={'class': 'form-control'}),
            'airline_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'class_type': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
