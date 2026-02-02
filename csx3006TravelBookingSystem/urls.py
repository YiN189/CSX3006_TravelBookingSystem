# csx3006TravelBookingSystem/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home
from accounts.admin_views import admin_dashboard  # Add this import

# Customize admin site
admin.site.site_header = "Hotel Booking System Administration"
admin.site.site_title = "Hotel Booking Admin"
admin.site.index_title = "Welcome to Hotel Booking System Admin"

urlpatterns = [
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),  # Add this
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('partners/', include('partners.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
