# bookings/urls.py

from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # Hotel booking
    path('hotels/', views.hotel_search, name='hotel_search'),
    path('hotels/<int:hotel_id>/', views.hotel_detail, name='hotel_detail'),
    path('hotels/book/<int:room_type_id>/', views.hotel_booking_create, name='hotel_booking_create'),

    # Flight booking
    path('flights/', views.flight_search, name='flight_search'),
    path('flights/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('flights/book/<int:flight_id>/', views.flight_booking_create, name='flight_booking_create'),

    # Booking management
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/<uuid:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<uuid:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('cancel/<uuid:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
