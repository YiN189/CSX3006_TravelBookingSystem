# partners/admin.py
'''
from django.contrib import admin
from .models import Partner, Hotel, RoomType, Flight


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'user', 'is_verified', 'created_at']
    list_filter = ['partner_type', 'is_verified', 'created_at']
    search_fields = ['name', 'user__username', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'partner_type', 'is_verified')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'website')
        }),
        ('Additional Details', {
            'fields': ('description', 'logo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'partner', 'star_rating', 'is_active', 'created_at']
    list_filter = ['city', 'star_rating', 'is_active', 'created_at']
    search_fields = ['name', 'city', 'address', 'partner__name']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter hotels by partner if user is partner
        if hasattr(request.user, 'partner_profile'):
            return qs.filter(partner=request.user.partner_profile)
        return qs.none()


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel', 'price_per_night', 'max_occupancy', 'rooms_available', 'is_active']
    list_filter = ['is_active', 'max_occupancy', 'hotel__city']
    search_fields = ['name', 'hotel__name', 'description']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter room types by partner's hotels
        if hasattr(request.user, 'partner_profile'):
            return qs.filter(hotel__partner=request.user.partner_profile)
        return qs.none()


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'origin', 'destination', 'departure_time', 'price', 'seats_available', 'is_active']
    list_filter = ['origin', 'destination', 'is_active', 'departure_time']
    search_fields = ['flight_number', 'origin', 'destination', 'partner__name']
    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter flights by partner
        if hasattr(request.user, 'partner_profile'):
            return qs.filter(partner=request.user.partner_profile)
        return qs.none()
        '''
# partners/admin.py

from django.contrib import admin
from django.db.models import Count, Sum
from django.utils.html import format_html
from .models import Partner, Hotel, RoomType, Flight


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'user_email', 'is_verified', 'hotels_count', 'flights_count', 'created_at']
    list_filter = ['partner_type', 'is_verified', 'created_at']
    search_fields = ['name', 'user__username', 'user__email', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_verified']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'partner_type', 'is_verified')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'website')
        }),
        ('Additional Details', {
            'fields': ('description', 'logo')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'User Email'

    def hotels_count(self, obj):
        count = obj.hotels.count()
        if count > 0:
            return format_html(
                '<a href="/admin/partners/hotel/?partner__id__exact={}">{} Hotels</a>',
                obj.id, count
            )
        return '0 Hotels'

    hotels_count.short_description = 'Hotels'

    def flights_count(self, obj):
        count = obj.flights.count()
        if count > 0:
            return format_html(
                '<a href="/admin/partners/flight/?partner__id__exact={}">{} Flights</a>',
                obj.id, count
            )
        return '0 Flights'

    flights_count.short_description = 'Flights'

    actions = ['verify_partners', 'unverify_partners']

    def verify_partners(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} partners verified.')

    verify_partners.short_description = 'Verify selected partners'

    def unverify_partners(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} partners unverified.')

    unverify_partners.short_description = 'Unverify selected partners'


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_link', 'city', 'star_rating', 'room_types_count', 'is_active', 'created_at']
    list_filter = ['city', 'star_rating', 'is_active', 'created_at', 'partner']
    search_fields = ['name', 'city', 'address', 'partner__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']

    fieldsets = (
        ('Basic Information', {
            'fields': ('partner', 'name', 'city', 'address', 'star_rating')
        }),
        ('Details', {
            'fields': ('description', 'main_image', 'amenities')
        }),
        ('Check-in/out Times', {
            'fields': ('check_in_time', 'check_out_time')
        }),
        ('Contact', {
            'fields': ('email', 'phone')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Partner can only see their own hotels
        if hasattr(request.user, 'partner_profile'):
            return qs.filter(partner=request.user.partner_profile)
        return qs.none()

    def partner_link(self, obj):
        return format_html(
            '<a href="/admin/partners/partner/{}/change/">{}</a>',
            obj.partner.id, obj.partner.name
        )

    partner_link.short_description = 'Partner'

    def room_types_count(self, obj):
        count = obj.room_types.count()
        if count > 0:
            return format_html(
                '<a href="/admin/partners/roomtype/?hotel__id__exact={}">{} Rooms</a>',
                obj.id, count
            )
        return '0 Rooms'

    room_types_count.short_description = 'Room Types'

    actions = ['activate_hotels', 'deactivate_hotels']

    def activate_hotels(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} hotels activated.')

    activate_hotels.short_description = 'Activate selected hotels'

    def deactivate_hotels(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} hotels deactivated.')

    deactivate_hotels.short_description = 'Deactivate selected hotels'


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hotel_link', 'price_per_night', 'max_occupancy', 'rooms_available', 'bookings_count',
                    'is_active']
    list_filter = ['is_active', 'max_occupancy', 'hotel__city', 'hotel__partner']
    search_fields = ['name', 'hotel__name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active', 'rooms_available']

    fieldsets = (
        ('Basic Information', {
            'fields': ('hotel', 'name', 'description')
        }),
        ('Pricing & Capacity', {
            'fields': ('price_per_night', 'max_occupancy', 'rooms_available')
        }),
        ('Room Details', {
            'fields': ('room_size', 'bed_type', 'amenities', 'image')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Partner can only see their own room types
        if hasattr(request.user, 'partner_profile'):
            return qs.filter(hotel__partner=request.user.partner_profile)
        return qs.none()

    def hotel_link(self, obj):
        return format_html(
            '<a href="/admin/partners/hotel/{}/change/">{}</a>',
            obj.hotel.id, obj.hotel.name
        )

    hotel_link.short_description = 'Hotel'

    def bookings_count(self, obj):
        count = obj.bookings.count()
        return f'{count} bookings'

    bookings_count.short_description = 'Total Bookings'


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'partner_link', 'route', 'departure_time', 'price', 'seats_status',
                    'bookings_count', 'is_active']
    list_filter = ['origin', 'destination', 'is_active', 'departure_time', 'class_type', 'partner']
    search_fields = ['flight_number', 'origin', 'destination', 'partner__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_active']
    date_hierarchy = 'departure_time'

    fieldsets = (
        ('Basic Information', {
            'fields': ('partner', 'flight_number', 'aircraft_type', 'class_type')
        }),
        ('Route & Schedule', {
            'fields': ('origin', 'destination', 'departure_time', 'arrival_time')
        }),
        ('Pricing & Capacity', {
            'fields': ('price', 'total_seats', 'seats_available')
        }),
        ('Additional', {
            'fields': ('airline_logo', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Partner can only see their own flights
        if hasattr(request.user, 'partner_profile'):
            return qs.filter(partner=request.user.partner_profile)
        return qs.none()

    def partner_link(self, obj):
        return format_html(
            '<a href="/admin/partners/partner/{}/change/">{}</a>',
            obj.partner.id, obj.partner.name
        )

    partner_link.short_description = 'Partner'

    def route(self, obj):
        return f'{obj.origin} → {obj.destination}'

    route.short_description = 'Route'

    def seats_status(self, obj):
        percentage = (obj.seats_available / obj.total_seats) * 100
        if percentage > 50:
            color = 'green'
        elif percentage > 20:
            color = 'orange'
        else:
            color = 'red'
        return format_html(
            '<span style="color: {};">{} / {} ({}%)</span>',
            color, obj.seats_available, obj.total_seats, int(percentage)
        )

    seats_status.short_description = 'Available Seats'

    def bookings_count(self, obj):
        count = obj.bookings.count()
        return f'{count} bookings'

    bookings_count.short_description = 'Total Bookings'

    actions = ['activate_flights', 'deactivate_flights']

    def activate_flights(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} flights activated.')

    activate_flights.short_description = 'Activate selected flights'

    def deactivate_flights(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} flights deactivated.')

    deactivate_flights.short_description = 'Deactivate selected flights'

