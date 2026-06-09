from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.views.generic import CreateView, TemplateView, ListView
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
import time
# Import local models and forms
from .forms import UserRegistrationForm
from .models import UserProfile, SearchLog, AdminConsumptionLimit

# 1. User Registration View
class RegisterView(CreateView):
    """
    Handles user registration using Django's CreateView.
    Creates the User object and the associated UserProfile simultaneously.
    """
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """
        Override form_valid to handle custom logic before saving the form.
        1. Save the user without committing to DB yet.
        2. Set the password hash.
        3. Create the related UserProfile instance.
        """
        # Create user instance but do not save to database yet
        user = form.save(commit=False) 
        # Hash the password securely
        user.set_password(form.cleaned_data['password']) 
        user.save()

        # Create the related UserProfile object
        UserProfile.objects.create(
            user=user,
            national_code=form.cleaned_data['national_code'],
            phone_number=form.cleaned_data['phone_number'],
            birth_date=form.cleaned_data.get('birth_date'),
            address=form.cleaned_data.get('address')
        )
        # Display success message
        messages.success(self.request, 'Registration successful. Please log in.')
         # Return the standard response for a valid form
        return super().form_valid(form)

# 2. Login View
class LoginView(TemplateView):
    """
    Handles user login.
    Uses TemplateView to render the login page and handle POST requests.
    """
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        """
        Add context data to the template.
        If the user is already logged in, redirect them to the dashboard.
        """
        context = super().get_context_data(**kwargs)
        
        # Redirect authenticated users to dashboard to prevent duplicate logins
        if self.request.user.is_authenticated:
            return redirect('users:dashboard')
            
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for login credentials.
        """
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('users:dashboard')
        else:
            # Authentication failed
            messages.error(request, 'Invalid username or password.')
            # Render the template again with the context (including error messages)
            return self.render_to_response(self.get_context_data()) 

# 3. Logout View
class CustomLogoutView(LogoutView):
    """
    Handles user logout.
    Redirects to the login page after logout.
    """
    next_page = reverse_lazy('users:login')


