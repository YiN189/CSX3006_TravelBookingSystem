# bookings/forms.py

from django import forms
from .models import Booking, HotelBookingDetail, FlightBookingDetail
from partners.models import Hotel, RoomType, Flight
from datetime import date, timedelta


class HotelSearchForm(forms.Form):
    """
    Form for searching hotels
    """
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter city name'
        })
    )

    check_in_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()
        })
    )

    check_out_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': (date.today() + timedelta(days=1)).isoformat()
        })
    )

    guests = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )


class HotelBookingForm(forms.ModelForm):
    """
    Form for creating hotel bookings
    """
    check_in_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()
        })
    )

    check_out_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': (date.today() + timedelta(days=1)).isoformat()
        })
    )

    number_of_rooms = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    number_of_guests = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Special requests or notes'
        })
    )

    class Meta:
        model = HotelBookingDetail
        fields = ['check_in_date', 'check_out_date', 'number_of_rooms', 'number_of_guests']

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError('Check-out date must be after check-in date.')

            if check_in < date.today():
                raise forms.ValidationError('Check-in date cannot be in the past.')

        return cleaned_data


class FlightSearchForm(forms.Form):
    """
    Form for searching flights
    """
    origin = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Departure city'
        })
    )

    destination = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Arrival city'
        })
    )

    departure_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': date.today().isoformat()
        })
    )

    passengers = forms.IntegerField(
        min_value=1,
        initial=1,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )


class FlightBookingForm(forms.ModelForm):
    """
    Form for creating flight bookings (includes passenger info)
    """
    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Mrs', 'Mrs.'),
        ('Ms', 'Ms.'),
        ('Dr', 'Dr.'),
    ]

    number_of_passengers = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    # Passenger fields (now part of FlightBookingDetail)
    passenger_title = forms.ChoiceField(
        choices=TITLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    passenger_first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )

    passenger_last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )

    passenger_dob = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    passenger_passport = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Passport Number (optional)'
        })
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Special requests or notes'
        })
    )

    class Meta:
        model = FlightBookingDetail
        fields = ['number_of_passengers', 'passenger_title', 'passenger_first_name',
                  'passenger_last_name', 'passenger_dob', 'passenger_passport']
