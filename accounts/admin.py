# accounts/admin.py
'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin
    """
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone'),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'role', 'phone'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile Admin
    """
    list_display = ['user', 'city', 'country']
    search_fields = ['user__username', 'user__email', 'city', 'country']
    list_filter = ['country', 'city']
    '''

# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Count
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Enhanced User Admin with statistics
    """
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active', 'bookings_count', 'created_at']
    list_filter = ['role', 'is_staff', 'is_active', 'created_at', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone']
    ordering = ['-created_at']
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'role', 'phone'),
        }),
    )

    def bookings_count(self, obj):
        """Show number of bookings for this user"""
        return obj.bookings.count()

    bookings_count.short_description = 'Total Bookings'

    actions = ['make_customer', 'make_partner', 'activate_users', 'deactivate_users']

    def make_customer(self, request, queryset):
        updated = queryset.update(role='customer')
        self.message_user(request, f'{updated} users changed to Customer role.')

    make_customer.short_description = 'Change role to Customer'

    def make_partner(self, request, queryset):
        updated = queryset.update(role='partner')
        self.message_user(request, f'{updated} users changed to Partner role.')

    make_partner.short_description = 'Change role to Partner'

    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users activated.')

    activate_users.short_description = 'Activate selected users'

    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} users deactivated.')

    deactivate_users.short_description = 'Deactivate selected users'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile Admin
    """
    list_display = ['user', 'city', 'country', 'phone']
    search_fields = ['user__username', 'user__email', 'city', 'country']
    list_filter = ['country', 'city']
    readonly_fields = ['user']

    def phone(self, obj):
        return obj.user.phone

    phone.short_description = 'Phone Number'
