# partners/admin.py

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
