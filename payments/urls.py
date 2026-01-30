from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment processing
    path('pay/<uuid:booking_id>/', views.payment_page, name='payment_page'),
    path('success/<uuid:payment_id>/', views.payment_success, name='payment_success'),
    path('failed/<uuid:payment_id>/', views.payment_failed, name='payment_failed'),

    # Payment history
    path('history/', views.payment_history, name='payment_history'),

    # Receipt
    path('receipt/<uuid:payment_id>/', views.payment_receipt, name='payment_receipt'),

    # Refund
    path('refund/<uuid:payment_id>/', views.request_refund, name='request_refund'),

    # Admin statistics
    path('statistics/', views.payment_statistics, name='statistics'),
]
