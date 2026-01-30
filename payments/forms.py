from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    # Card payment fields
    card_number = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234 5678 9012 3456',
            'maxlength': '16'
        })
    )

    cvv = forms.CharField(
        max_length=4,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'CVV',
            'maxlength': '4'
        })
    )

    expiry_month = forms.ChoiceField(
        choices=[(str(i).zfill(2), str(i).zfill(2)) for i in range(1, 13)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    expiry_year = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(2026, 2036)],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Payment
        fields = ['payment_method', 'card_holder_name', 'card_type',
                  'bank_name', 'account_number', 'paypal_email', 'notes']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'card_holder_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'John Doe'
            }),
            'card_type': forms.Select(attrs={'class': 'form-select'}),
            'bank_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bank Name'
            }),
            'account_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Account Number'
            }),
            'paypal_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')

        if payment_method in ['credit_card', 'debit_card']:
            # Validate card fields
            if not cleaned_data.get('card_number'):
                raise forms.ValidationError("Card number is required for card payments")
            if not cleaned_data.get('cvv'):
                raise forms.ValidationError("CVV is required for card payments")
            if not cleaned_data.get('card_holder_name'):
                raise forms.ValidationError("Card holder name is required")

            # Store last 4 digits only
            card_number = cleaned_data.get('card_number', '')
            cleaned_data['card_last_four'] = card_number[-4:] if len(card_number) >= 4 else ''

        elif payment_method == 'bank_transfer':
            if not cleaned_data.get('bank_name'):
                raise forms.ValidationError("Bank name is required for bank transfer")
            if not cleaned_data.get('account_number'):
                raise forms.ValidationError("Account number is required for bank transfer")

        elif payment_method == 'paypal':
            if not cleaned_data.get('paypal_email'):
                raise forms.ValidationError("PayPal email is required for PayPal payments")

        return cleaned_data


class RefundForm(forms.Form):
    reason = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Please provide a reason for the refund...'
        }),
        required=True,
        label='Refund Reason'
    )

    confirm = forms.BooleanField(
        required=True,
        label='I confirm that I want to refund this payment',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
