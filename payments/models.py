from django.db import models
from django.conf import settings
from bookings.models import Booking
import uuid
from django.utils import timezone


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('paypal', 'PayPal'),
        ('cash', 'Cash'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    CARD_TYPE_CHOICES = [
        ('visa', 'Visa'),
        ('mastercard', 'Mastercard'),
        ('amex', 'American Express'),
        ('discover', 'Discover'),
        ('other', 'Other'),
    ]

    # Primary fields
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')

    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Transaction details
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    # Card details (optional, for card payments)
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES, blank=True, null=True)
    card_last_four = models.CharField(max_length=4, blank=True, null=True)
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)

    # Bank transfer details (optional)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=50, blank=True, null=True)

    # PayPal details (optional)
    paypal_email = models.EmailField(blank=True, null=True)

    # Timestamps
    payment_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Additional info
    notes = models.TextField(blank=True, null=True)
    failure_reason = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['payment_method']),
        ]

    def __str__(self):
        return f"Payment {self.payment_id} - {self.booking.booking_id} - {self.status}"

    def save(self, *args, **kwargs):
        # Generate transaction ID if not exists
        if not self.transaction_id:
            self.transaction_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"

        # Set payment date when completed
        if self.status == 'completed' and not self.payment_date:
            self.payment_date = timezone.now()

        super().save(*args, **kwargs)

    def process_payment(self):
        """Mock payment processing"""
        # In a real system, this would integrate with payment gateway
        import random

        # 95% success rate for demo
        if random.random() < 0.95:
            self.status = 'completed'
            self.payment_date = timezone.now()
            self.booking.status = 'confirmed'
            self.booking.save()
            self.save()
            return True, "Payment processed successfully"
        else:
            self.status = 'failed'
            self.failure_reason = "Payment declined by bank (Mock)"
            self.save()
            return False, "Payment failed. Please try again."

    def refund_payment(self):
        """Process refund"""
        if self.status == 'completed':
            self.status = 'refunded'
            self.booking.status = 'cancelled'
            self.booking.save()

            # Restore availability if hotel booking
            if self.booking.booking_type == 'hotel':
                hotel_detail = self.booking.hotel_detail
                hotel_detail.room_type.available_rooms += hotel_detail.number_of_rooms
                hotel_detail.room_type.save()

            # Restore availability if flight booking
            elif self.booking.booking_type == 'flight':
                flight_detail = self.booking.flight_detail
                flight_detail.flight.available_seats += flight_detail.passengers.count()
                flight_detail.flight.save()

            self.save()
            return True, "Payment refunded successfully"
        return False, "Cannot refund this payment"


class PaymentReceipt(models.Model):
    """Model to track receipt generation"""
    receipt_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='receipt')
    generated_at = models.DateTimeField(auto_now_add=True)
    downloaded_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"Receipt {self.receipt_id} for Payment {self.payment.payment_id}"

    def increment_download(self):
        self.downloaded_count += 1
        self.save()
