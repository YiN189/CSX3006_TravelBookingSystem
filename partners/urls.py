# partners/urls.py

from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    # Partner dashboard and profile
    path('dashboard/', views.partner_dashboard, name='partner_dashboard'),
    path('profile/', views.partner_profile, name='partner_profile'),

    # Hotel management
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('hotels/create/', views.hotel_create, name='hotel_create'),
    path('hotels/<int:hotel_id>/edit/', views.hotel_edit, name='hotel_edit'),
    path('hotels/<int:hotel_id>/delete/', views.hotel_delete, name='hotel_delete'),

    # Room type management
    path('hotels/<int:hotel_id>/rooms/', views.room_type_list, name='room_type_list'),
    path('hotels/<int:hotel_id>/rooms/create/', views.room_type_create, name='room_type_create'),
    path('hotels/<int:hotel_id>/rooms/<int:room_id>/edit/', views.room_type_edit, name='room_type_edit'),
    path('hotels/<int:hotel_id>/rooms/<int:room_id>/delete/', views.room_type_delete, name='room_type_delete'),

    # Flight management
    path('flights/', views.flight_list, name='flight_list'),
    path('flights/create/', views.flight_create, name='flight_create'),
    path('flights/<int:flight_id>/edit/', views.flight_edit, name='flight_edit'),
    path('flights/<int:flight_id>/delete/', views.flight_delete, name='flight_delete'),
]
