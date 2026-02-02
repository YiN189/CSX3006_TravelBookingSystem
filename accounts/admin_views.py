# accounts/admin_views.py

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from partners.models import Partner, Hotel, Flight
from bookings.models import Booking


@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard with statistics
    """
    # Date ranges
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)

    # User statistics
    total_users = User.objects.count()
    customers = User.objects.filter(role='customer').count()
    partners = User.objects.filter(role='partner').count()
    admins = User.objects.filter(role='admin').count()
    new_users_this_month = User.objects.filter(created_at__gte=last_30_days).count()

    # Partner statistics
    total_partners = Partner.objects.count()
    verified_partners = Partner.objects.filter(is_verified=True).count()
    total_hotels = Hotel.objects.count()
    active_hotels = Hotel.objects.filter(is_active=True).count()
    total_flights = Flight.objects.count()
    active_flights = Flight.objects.filter(is_active=True).count()

    # Booking statistics
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    cancelled_bookings = Booking.objects.filter(status='cancelled').count()
    bookings_this_week = Booking.objects.filter(created_at__gte=last_7_days).count()
    bookings_this_month = Booking.objects.filter(created_at__gte=last_30_days).count()

    # Revenue statistics
    total_revenue = Booking.objects.filter(
        status__in=['confirmed', 'completed']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    revenue_this_month = Booking.objects.filter(
        status__in=['confirmed', 'completed'],
        created_at__gte=last_30_days
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    avg_booking_value = Booking.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0

    # Recent bookings
    recent_bookings = Booking.objects.select_related('user').order_by('-created_at')[:10]

    # Top customers
    top_customers = User.objects.filter(role='customer').annotate(
        booking_count=Count('bookings'),
        total_spent=Sum('bookings__total_amount')
    ).order_by('-total_spent')[:5]

    context = {
        # User stats
        'total_users': total_users,
        'customers': customers,
        'partners': partners,
        'admins': admins,
        'new_users_this_month': new_users_this_month,

        # Partner stats
        'total_partners': total_partners,
        'verified_partners': verified_partners,
        'total_hotels': total_hotels,
        'active_hotels': active_hotels,
        'total_flights': total_flights,
        'active_flights': active_flights,

        # Booking stats
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'bookings_this_week': bookings_this_week,
        'bookings_this_month': bookings_this_month,

        # Revenue stats
        'total_revenue': total_revenue,
        'revenue_this_month': revenue_this_month,
        'avg_booking_value': avg_booking_value,

        # Lists
        'recent_bookings': recent_bookings,
        'top_customers': top_customers,
    }

    return render(request, 'admin/dashboard.html', context)
