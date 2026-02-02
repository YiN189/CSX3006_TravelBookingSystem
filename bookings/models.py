# bookings/models.py

from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import User
from partners.models import Hotel, RoomType, Flight
import uuid


class Booking(models.Model):
    """
    Main Booking model - handles both hotel and flight bookings
    """
    BOOKING_TYPE_CHOICES = [
        ('hotel', 'Hotel Booking'),
        ('flight', 'Flight Booking'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    booking_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text='Unique booking ID'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    booking_type = models.CharField(
        max_length=20,
        choices=BOOKING_TYPE_CHOICES,
        help_text='Type of booking'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text='Booking status'
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Total booking amount'
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Additional notes or special requests'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.booking_id} - {self.user.username} ({self.get_booking_type_display()})"

    def is_active(self):
        return self.status in ['pending', 'confirmed']


class HotelBookingDetail(models.Model):
    """
    Hotel-specific booking details
    """
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='hotel_details',
        limit_choices_to={'booking_type': 'hotel'}
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    check_in_date = models.DateField(
        help_text='Check-in date'
    )

    check_out_date = models.DateField(
        help_text='Check-out date'
    )

    number_of_rooms = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        help_text='Number of rooms booked'
    )

    number_of_guests = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        help_text='Total number of guests'
    )

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price per night at time of booking'
    )

    number_of_nights = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text='Number of nights'
    )

    class Meta:
        verbose_name = 'Hotel Booking Detail'
        verbose_name_plural = 'Hotel Booking Details'

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type.name}"

    def calculate_total(self):
        """Calculate total cost for hotel booking"""
        return self.price_per_night * self.number_of_nights * self.number_of_rooms


class FlightBookingDetail(models.Model):
    """
    Flight-specific booking details (includes passenger info)
    """
    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Mrs', 'Mrs.'),
        ('Ms', 'Ms.'),
        ('Dr', 'Dr.'),
    ]
    
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='flight_details',
        limit_choices_to={'booking_type': 'flight'}
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    number_of_passengers = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=1,
        help_text='Number of passengers'
    )

    price_per_seat = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text='Price per seat at time of booking'
    )
    
    # ============================================
    # PASSENGER INFORMATION (moved from Passenger entity)
    # ============================================
    passenger_title = models.CharField(
        max_length=10,
        choices=TITLE_CHOICES,
        default='Mr',
        help_text='Passenger title'
    )
    
    passenger_first_name = models.CharField(
        max_length=100,
        help_text='Passenger first name',
        blank=True,
        null=True
    )
    
    passenger_last_name = models.CharField(
        max_length=100,
        help_text='Passenger last name',
        blank=True,
        null=True
    )
    
    passenger_dob = models.DateField(
        blank=True,
        null=True,
        help_text='Passenger date of birth'
    )
    
    passenger_passport = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Passport number'
    )

    class Meta:
        verbose_name = 'Flight Booking Detail'
        verbose_name_plural = 'Flight Booking Details'

    def __str__(self):
        return f"{self.flight.flight_number} - {self.number_of_passengers} passengers"

    def calculate_total(self):
        """Calculate total cost for flight booking"""
        return self.price_per_seat * self.number_of_passengers
    
    @property
    def passenger_full_name(self):
        """Get passenger full name"""
        return f"{self.passenger_title} {self.passenger_first_name} {self.passenger_last_name}"



class Passenger(models.Model):
    """
    Passenger information for flight bookings
    """
    TITLE_CHOICES = [
        ('Mr', 'Mr.'),
        ('Mrs', 'Mrs.'),
        ('Ms', 'Ms.'),
        ('Dr', 'Dr.'),
    ]

    flight_booking = models.ForeignKey(
        FlightBookingDetail,
        on_delete=models.CASCADE,
        related_name='passengers'
    )

    title = models.CharField(
        max_length=10,
        choices=TITLE_CHOICES,
        default='Mr'
    )

    first_name = models.CharField(
        max_length=100,
        help_text='Passenger first name'
    )

    last_name = models.CharField(
        max_length=100,
        help_text='Passenger last name'
    )

    date_of_birth = models.DateField(
        help_text='Passenger date of birth'
    )

    passport_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Passport number (for international flights)'
    )

    class Meta:
        verbose_name = 'Passenger'
        verbose_name_plural = 'Passengers'

    def __str__(self):
        return f"{self.title} {self.first_name} {self.last_name}"
