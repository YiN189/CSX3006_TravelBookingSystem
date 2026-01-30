# bookings/admin.py

from django.contrib import admin
from .models import Booking, HotelBookingDetail, FlightBookingDetail, Passenger


class HotelBookingDetailInline(admin.StackedInline):
    model = HotelBookingDetail
    extra = 0


class FlightBookingDetailInline(admin.StackedInline):
    model = FlightBookingDetail
    extra = 0


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'booking_type', 'status', 'total_amount', 'created_at']
    list_filter = ['booking_type', 'status', 'created_at']
    search_fields = ['booking_id', 'user__username', 'user__email']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    inlines = [HotelBookingDetailInline, FlightBookingDetailInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('booking_id', 'user', 'booking_type', 'status')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Additional', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(HotelBookingDetail)
class HotelBookingDetailAdmin(admin.ModelAdmin):
    list_display = ['booking', 'hotel', 'room_type', 'check_in_date', 'check_out_date', 'number_of_rooms']
    list_filter = ['check_in_date', 'hotel__city']
    search_fields = ['booking__booking_id', 'hotel__name', 'room_type__name']


@admin.register(FlightBookingDetail)
class FlightBookingDetailAdmin(admin.ModelAdmin):
    list_display = ['booking', 'flight', 'number_of_passengers', 'price_per_seat']
    list_filter = ['flight__departure_time']
    search_fields = ['booking__booking_id', 'flight__flight_number']


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['title', 'first_name', 'last_name', 'date_of_birth', 'flight_booking']
    list_filter = ['title']
    search_fields = ['first_name', 'last_name', 'passport_number']

