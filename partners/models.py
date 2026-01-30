# partners/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Partner(models.Model):
    """
    Partner model - links to User with role='partner'
    """
    PARTNER_TYPE_CHOICES = [
        ('hotel', 'Hotel Partner'),
        ('flight', 'Flight Partner'),
        ('both', 'Hotel & Flight Partner'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='partner_profile',
        limit_choices_to={'role': 'partner'}
    )

    name = models.CharField(
        max_length=255,
        help_text='Company/Business name'
    )

    partner_type = models.CharField(
        max_length=20,
        choices=PARTNER_TYPE_CHOICES,
        default='both',
        help_text='Type of partner'
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Partner description'
    )

    logo = models.ImageField(
        upload_to='partners/logos/',
        blank=True,
        null=True
    )

    website = models.URLField(
        blank=True,
        null=True
    )

    contact_email = models.EmailField()

    contact_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    is_verified = models.BooleanField(
        default=False,
        help_text='Whether the partner is verified by admin'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_partner_type_display()})"


class Hotel(models.Model):
    """
    Hotel model
    """
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='hotels'
    )

    name = models.CharField(
        max_length=255,
        help_text='Hotel name'
    )

    city = models.CharField(
        max_length=100,
        help_text='City where hotel is located'
    )

    address = models.TextField(
        help_text='Full address'
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Hotel description'
    )

    star_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=3,
        help_text='Star rating (1-5)'
    )

    main_image = models.ImageField(
        upload_to='hotels/',
        blank=True,
        null=True
    )

    amenities = models.TextField(
        blank=True,
        null=True,
        help_text='Hotel amenities (comma-separated)'
    )

    check_in_time = models.TimeField(
        default='14:00:00',
        help_text='Check-in time'
    )

    check_out_time = models.TimeField(
        default='12:00:00',
        help_text='Check-out time'
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether the hotel is active'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.city}"


class RoomType(models.Model):
    """
    Room Type model for hotels
    """
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='room_types'
    )

    name = models.CharField(
        max_length=100,
        help_text='Room type name (e.g., Standard, Deluxe, Suite)'
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='Room description'
    )

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Price per night'
    )

    max_occupancy = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=2,
        help_text='Maximum number of guests'
    )

    rooms_available = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=10,
        help_text='Number of rooms available'
    )

    room_size = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Room size in square meters'
    )

    bed_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Type of bed (e.g., King, Queen, Twin)'
    )

    amenities = models.TextField(
        blank=True,
        null=True,
        help_text='Room amenities (comma-separated)'
    )

    image = models.ImageField(
        upload_to='rooms/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether the room type is available for booking'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Room Type'
        verbose_name_plural = 'Room Types'
        ordering = ['hotel', 'price_per_night']

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"


class Flight(models.Model):
    """
    Flight model
    """
    partner = models.ForeignKey(
        Partner,
        on_delete=models.CASCADE,
        related_name='flights'
    )

    flight_number = models.CharField(
        max_length=20,
        unique=True,
        help_text='Unique flight number'
    )

    origin = models.CharField(
        max_length=100,
        help_text='Departure city/airport'
    )

    destination = models.CharField(
        max_length=100,
        help_text='Arrival city/airport'
    )

    departure_time = models.DateTimeField(
        help_text='Departure date and time'
    )

    arrival_time = models.DateTimeField(
        help_text='Arrival date and time'
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text='Base price per seat'
    )

    seats_available = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=150,
        help_text='Number of seats available'
    )

    total_seats = models.IntegerField(
        validators=[MinValueValidator(1)],
        default=150,
        help_text='Total number of seats'
    )

    aircraft_type = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Type of aircraft'
    )

    airline_logo = models.ImageField(
        upload_to='airlines/',
        blank=True,
        null=True
    )

    class_type = models.CharField(
        max_length=50,
        default='Economy',
        help_text='Class type (Economy, Business, First Class)'
    )

    is_active = models.BooleanField(
        default=True,
        help_text='Whether the flight is available for booking'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Flight'
        verbose_name_plural = 'Flights'
        ordering = ['departure_time']

    def __str__(self):
        return f"{self.flight_number}: {self.origin} → {self.destination}"

    @property
    def duration(self):
        """Calculate flight duration"""
        return self.arrival_time - self.departure_time
