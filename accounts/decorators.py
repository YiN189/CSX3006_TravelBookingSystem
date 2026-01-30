# accounts/decorators.py

from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator to restrict access based on user role
    Usage: @role_required(['admin', 'partner'])
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role in allowed_roles or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                from django.shortcuts import redirect
                from django.urls import reverse
                return redirect(f"{reverse('accounts:login')}?next={request.path}")
        return wrapped_view
    return decorator


def customer_required(view_func):
    """
    Decorator for customer-only views
    """
    return role_required(['customer'])(view_func)


def partner_required(view_func):
    """
    Decorator for partner-only views
    """
    return role_required(['partner'])(view_func)


def admin_required(view_func):
    """
    Decorator for admin-only views
    """
    return role_required(['admin'])(view_func)
