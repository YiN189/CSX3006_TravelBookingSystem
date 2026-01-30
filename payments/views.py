from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum, Count, Q
from bookings.models import Booking
from .models import Payment, PaymentReceipt
from .forms import PaymentForm, RefundForm
from accounts.decorators import customer_required, admin_required
from datetime import timedelta


@login_required
@customer_required
def payment_page(request, booking_id):
    """Payment form page"""
    booking = get_object_or_404(Booking, booking_id=booking_id, user=request.user)

    # Check if payment already exists
    if hasattr(booking, 'payment'):
        if booking.payment.status == 'completed':
            messages.info(request, 'This booking has already been paid.')
            return redirect('payments:payment_success', payment_id=booking.payment.payment_id)
        elif booking.payment.status == 'pending':
            # Allow retry
            payment = booking.payment
        else:
            # Create new payment for failed ones
            payment = None
    else:
        payment = None

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.user = request.user
            payment.amount = booking.total_amount

            # Store card last 4 digits if card payment
            if form.cleaned_data['payment_method'] in ['credit_card', 'debit_card']:
                payment.card_last_four = form.cleaned_data['card_last_four']

            payment.save()

            # Process payment
            success, message = payment.process_payment()

            if success:
                messages.success(request, message)

                # Create receipt
                PaymentReceipt.objects.get_or_create(payment=payment)

                return redirect('payments:payment_success', payment_id=payment.payment_id)
            else:
                messages.error(request, message)
                return redirect('payments:payment_failed', payment_id=payment.payment_id)
    else:
        initial_data = {'payment_method': 'credit_card'}
        form = PaymentForm(instance=payment, initial=initial_data)

    context = {
        'form': form,
        'booking': booking,
        'payment': payment,
    }
    return render(request, 'payments/payment_form.html', context)


@login_required
def payment_success(request, payment_id):
    """Payment success page"""
    payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)

    context = {
        'payment': payment,
        'booking': payment.booking,
    }
    return render(request, 'payments/payment_success.html', context)


@login_required
def payment_failed(request, payment_id):
    """Payment failed page"""
    payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)

    context = {
        'payment': payment,
        'booking': payment.booking,
    }
    return render(request, 'payments/payment_failed.html', context)


@login_required
def payment_history(request):
    """View payment history for current user"""
    payments = Payment.objects.filter(user=request.user).select_related('booking')

    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)

    # Filter by payment method
    method_filter = request.GET.get('method')
    if method_filter:
        payments = payments.filter(payment_method=method_filter)

    context = {
        'payments': payments,
        'status_filter': status_filter,
        'method_filter': method_filter,
    }
    return render(request, 'payments/payment_history.html', context)


@login_required
def payment_receipt(request, payment_id):
    """Generate and display payment receipt"""
    payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)

    if payment.status != 'completed':
        messages.error(request, 'Receipt is only available for completed payments.')
        return redirect('payments:payment_history')

    # Get or create receipt
    receipt, created = PaymentReceipt.objects.get_or_create(payment=payment)
    receipt.increment_download()

    context = {
        'payment': payment,
        'booking': payment.booking,
        'receipt': receipt,
    }
    return render(request, 'payments/receipt.html', context)


@login_required
@customer_required
def request_refund(request, payment_id):
    """Request a refund for a payment"""
    payment = get_object_or_404(Payment, payment_id=payment_id, user=request.user)

    if payment.status != 'completed':
        messages.error(request, 'Only completed payments can be refunded.')
        return redirect('payments:payment_history')

    if request.method == 'POST':
        form = RefundForm(request.POST)
        if form.is_valid():
            success, message = payment.refund_payment()
            if success:
                # Store refund reason in payment notes
                refund_reason = form.cleaned_data['reason']
                payment.notes = f"Refund requested: {refund_reason}\n\n{payment.notes or ''}"
                payment.save()

                messages.success(request, message)
                return redirect('payments:payment_history')
            else:
                messages.error(request, message)
    else:
        form = RefundForm()

    context = {
        'form': form,
        'payment': payment,
        'booking': payment.booking,
    }
    return render(request, 'payments/refund_request.html', context)


@login_required
@admin_required
def payment_statistics(request):
    """Admin dashboard for payment statistics"""
    # Date range filter
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    payments = Payment.objects.filter(created_at__gte=start_date)

    # Overall statistics
    total_revenue = payments.filter(status='completed').aggregate(
        total=Sum('amount'))['total'] or 0

    total_refunded = payments.filter(status='refunded').aggregate(
        total=Sum('amount'))['total'] or 0

    payment_count = payments.count()
    completed_count = payments.filter(status='completed').count()
    failed_count = payments.filter(status='failed').count()
    refunded_count = payments.filter(status='refunded').count()

    # Success rate
    success_rate = (completed_count / payment_count * 100) if payment_count > 0 else 0

    # By payment method
    by_method = payments.values('payment_method').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('-total')

    # By status
    by_status = payments.values('status').annotate(
        count=Count('id'),
        total=Sum('amount')
    )

    # Recent payments
    recent_payments = Payment.objects.select_related('booking', 'user').order_by('-created_at')[:10]

    context = {
        'days': days,
        'total_revenue': total_revenue,
        'total_refunded': total_refunded,
        'payment_count': payment_count,
        'completed_count': completed_count,
        'failed_count': failed_count,
        'refunded_count': refunded_count,
        'success_rate': round(success_rate, 2),
        'by_method': by_method,
        'by_status': by_status,
        'recent_payments': recent_payments,
    }
    return render(request, 'payments/statistics.html', context)
