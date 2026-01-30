from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Payment, PaymentReceipt


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_id_short', 'user', 'booking_link', 'amount',
                    'payment_method', 'status_badge', 'payment_date', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at', 'payment_date']
    search_fields = ['payment_id', 'transaction_id', 'user__email',
                     'booking__booking_id', 'card_holder_name']
    readonly_fields = ['payment_id', 'transaction_id', 'created_at',
                       'updated_at', 'payment_date']

    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'booking', 'user', 'amount', 'status',
                       'transaction_id', 'payment_date')
        }),
        ('Payment Method', {
            'fields': ('payment_method',)
        }),
        ('Card Details', {
            'fields': ('card_type', 'card_last_four', 'card_holder_name'),
            'classes': ('collapse',)
        }),
        ('Bank Transfer Details', {
            'fields': ('bank_name', 'account_number'),
            'classes': ('collapse',)
        }),
        ('PayPal Details', {
            'fields': ('paypal_email',),
            'classes': ('collapse',)
        }),
        ('Additional Information', {
            'fields': ('notes', 'failure_reason', 'created_at', 'updated_at')
        }),
    )

    def payment_id_short(self, obj):
        return str(obj.payment_id)[:8] + '...'

    payment_id_short.short_description = 'Payment ID'

    def booking_link(self, obj):
        url = reverse('admin:bookings_booking_change', args=[obj.booking.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.booking.booking_id)[:8])

    booking_link.short_description = 'Booking'

    def status_badge(self, obj):
        colors = {
            'pending': 'warning',
            'completed': 'success',
            'failed': 'danger',
            'refunded': 'info'
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color,
            obj.get_status_display()
        )

    status_badge.short_description = 'Status'

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Partner admin can only see payments for their properties
        if hasattr(request.user, 'partner_profile'):
            partner = request.user.partner_profile
            qs = qs.filter(
                Q(booking__hotel_detail__room_type__hotel__partner=partner) |
                Q(booking__flight_detail__flight__partner=partner)
            )

        return qs.select_related('user', 'booking')

    actions = ['mark_as_completed', 'mark_as_refunded']

    def mark_as_completed(self, request, queryset):
        count = 0
        for payment in queryset:
            if payment.status == 'pending':
                payment.status = 'completed'
                payment.payment_date = timezone.now()
                payment.booking.status = 'confirmed'
                payment.booking.save()
                payment.save()
                count += 1
        self.message_user(request, f'{count} payment(s) marked as completed.')

    mark_as_completed.short_description = 'Mark selected as completed'

    def mark_as_refunded(self, request, queryset):
        count = 0
        for payment in queryset:
            success, _ = payment.refund_payment()
            if success:
                count += 1
        self.message_user(request, f'{count} payment(s) refunded.')

    mark_as_refunded.short_description = 'Refund selected payments'


@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_id_short', 'payment_link', 'generated_at', 'downloaded_count']
    readonly_fields = ['receipt_id', 'generated_at', 'downloaded_count']
    search_fields = ['receipt_id', 'payment__payment_id']

    def receipt_id_short(self, obj):
        return str(obj.receipt_id)[:8] + '...'

    receipt_id_short.short_description = 'Receipt ID'

    def payment_link(self, obj):
        url = reverse('admin:payments_payment_change', args=[obj.payment.id])
        return format_html('<a href="{}">{}</a>', url, str(obj.payment.payment_id)[:8])

    payment_link.short_description = 'Payment'
