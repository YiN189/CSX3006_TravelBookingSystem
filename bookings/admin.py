# bookings/admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Booking, HotelBookingDetail, FlightBookingDetail


class HotelBookingDetailInline(admin.StackedInline):
    model = HotelBookingDetail
    extra = 0
    readonly_fields = ['hotel', 'room_type', 'check_in_date', 'check_out_date',
                       'number_of_rooms', 'number_of_guests', 'price_per_night', 'number_of_nights']
    can_delete = False


class FlightBookingDetailInline(admin.StackedInline):
    model = FlightBookingDetail
    extra = 0
    readonly_fields = ['flight', 'number_of_passengers', 'price_per_seat',
                       'passenger_title', 'passenger_first_name', 'passenger_last_name',
                       'passenger_dob', 'passenger_passport']
    can_delete = False


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id_short', 'user_link', 'booking_type', 'status_badge',
                    'total_amount', 'payment_status', 'created_at']
    list_filter = ['booking_type', 'status', 'created_at']
    search_fields = ['booking_id', 'user__username', 'user__email']
    readonly_fields = ['booking_id', 'created_at', 'updated_at']
    inlines = [HotelBookingDetailInline, FlightBookingDetailInline]
    date_hierarchy = 'created_at'

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

    def booking_id_short(self, obj):
        return str(obj.booking_id)[:8] + '...'

    booking_id_short.short_description = 'Booking ID'

    def user_link(self, obj):
        return format_html(
            '<a href="/admin/accounts/user/{}/change/">{}</a>',
            obj.user.id, obj.user.username
        )

    user_link.short_description = 'User'

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'green',
            'cancelled': 'red',
            'completed': 'blue'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )

    status_badge.short_description = 'Status'

    def payment_status(self, obj):
        if hasattr(obj, 'payment'):
            if obj.payment.status == 'completed':
                return format_html('<span style="color: green;">✓ Paid</span>')
            elif obj.payment.status == 'pending':
                return format_html('<span style="color: orange;">⏱ Pending</span>')
            elif obj.payment.status == 'failed':
                return format_html('<span style="color: red;">✗ Failed</span>')
            elif obj.payment.status == 'refunded':
                return format_html('<span style="color: blue;">↩ Refunded</span>')
        return format_html('<span style="color: gray;">No Payment</span>')

    payment_status.short_description = 'Payment'

    actions = ['confirm_bookings', 'cancel_bookings', 'complete_bookings']

    def confirm_bookings(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} bookings confirmed.')

    confirm_bookings.short_description = 'Confirm selected bookings'

    def cancel_bookings(self, request, queryset):
        updated = queryset.exclude(status='cancelled').update(status='cancelled')
        self.message_user(request, f'{updated} bookings cancelled.')

    cancel_bookings.short_description = 'Cancel selected bookings'

    def complete_bookings(self, request, queryset):
        updated = queryset.filter(status='confirmed').update(status='completed')
        self.message_user(request, f'{updated} bookings completed.')

    complete_bookings.short_description = 'Mark as completed'


@admin.register(HotelBookingDetail)
class HotelBookingDetailAdmin(admin.ModelAdmin):
    list_display = ['booking_link', 'hotel_link', 'room_type', 'check_in_date',
                    'check_out_date', 'nights', 'rooms', 'guests', 'total_cost']
    list_filter = ['check_in_date', 'hotel__city']
    search_fields = ['booking__booking_id', 'hotel__name', 'room_type__name']
    readonly_fields = ['booking', 'hotel', 'room_type']

    def booking_link(self, obj):
        return format_html(
            '<a href="/admin/bookings/booking/{}/change/">{}</a>',
            obj.booking.id, str(obj.booking.booking_id)[:8]
        )

    booking_link.short_description = 'Booking'

    def hotel_link(self, obj):
        return format_html(
            '<a href="/admin/partners/hotel/{}/change/">{}</a>',
            obj.hotel.id, obj.hotel.name
        )

    hotel_link.short_description = 'Hotel'

    def nights(self, obj):
        return obj.number_of_nights

    nights.short_description = 'Nights'

    def rooms(self, obj):
        return obj.number_of_rooms

    rooms.short_description = 'Rooms'

    def guests(self, obj):
        return obj.number_of_guests

    guests.short_description = 'Guests'

    def total_cost(self, obj):
        return f'${obj.calculate_total():.2f}'

    total_cost.short_description = 'Total'


@admin.register(FlightBookingDetail)
class FlightBookingDetailAdmin(admin.ModelAdmin):
    list_display = ['booking_link', 'flight_link', 'passengers_count', 'passenger_name', 'price_per_seat', 'total_cost']
    list_filter = ['flight__departure_time', 'flight__origin', 'flight__destination']
    search_fields = ['booking__booking_id', 'flight__flight_number', 'passenger_first_name', 'passenger_last_name']
    readonly_fields = ['booking', 'flight']

    fieldsets = (
        ('Booking Info', {
            'fields': ('booking', 'flight', 'number_of_passengers', 'price_per_seat')
        }),
        ('Passenger Info', {
            'fields': ('passenger_title', 'passenger_first_name', 'passenger_last_name',
                       'passenger_dob', 'passenger_passport')
        }),
    )

    def booking_link(self, obj):
        return format_html(
            '<a href="/admin/bookings/booking/{}/change/">{}</a>',
            obj.booking.id, str(obj.booking.booking_id)[:8]
        )

    booking_link.short_description = 'Booking'

    def flight_link(self, obj):
        return format_html(
            '<a href="/admin/partners/flight/{}/change/">{}</a>',
            obj.flight.id, obj.flight.flight_number
        )

    flight_link.short_description = 'Flight'

    def passengers_count(self, obj):
        return obj.number_of_passengers

    passengers_count.short_description = 'Passengers'

    def passenger_name(self, obj):
        if obj.passenger_first_name:
            return f'{obj.passenger_title} {obj.passenger_first_name} {obj.passenger_last_name}'
        return '-'

    passenger_name.short_description = 'Passenger Name'

    def total_cost(self, obj):
        return f'${obj.calculate_total():.2f}'

    total_cost.short_description = 'Total'
