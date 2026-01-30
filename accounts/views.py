# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm, UserUpdateForm, UserProfileUpdateForm
from .models import User, UserProfile


def home(request):
    """
    Homepage view
    """
    return render(request, 'home.html')


def register_view(request):
    """
    User registration view
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile automatically
            UserProfile.objects.create(user=user)

            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    User login view
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')

                # Redirect based on role
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard_view(request):
    """
    User dashboard - different content based on role
    """
    context = {
        'user': request.user,
        'role': request.user.role,
    }

    if request.user.is_system_admin():
        # System admin dashboard
        context['total_users'] = User.objects.count()
        context['total_customers'] = User.objects.filter(role='customer').count()
        context['total_partners'] = User.objects.filter(role='partner').count()

    elif request.user.is_partner():
        # Partner dashboard - redirect to partners app
        return redirect('partners:partner_dashboard')

    else:
        # Customer dashboard
        context['message'] = 'Welcome to your dashboard! Browse hotels and flights to start booking.'

    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_view(request):
    """
    User profile view with update functionality
    """
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'accounts/profile.html', context)
