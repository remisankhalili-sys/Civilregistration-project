from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.contrib import messages
from django.db.models import Q
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

# 4. User Dashboard View
class UserDashboardView(LoginRequiredMixin, TemplateView):
    """
    Displays the user dashboard.
    Requires the user to be logged in.
    Shows usage statistics and limits.
    """
    template_name = 'users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current user's profile
        user_profile = self.request.user.profile
        
        # Check usage limits
        is_daily_limited = not user_profile.check_daily_limit()
        is_monthly_limited = not user_profile.check_monthly_limit()
        
        # Get current usage amounts
        daily_used = user_profile.get_daily_usage()
        monthly_used = user_profile.get_monthly_usage()
        
        # Determine effective limits (from AdminConsumptionLimit if available, else default)
        try:
            admin_limits = AdminConsumptionLimit.objects.get(user=self.request.user)
            daily_limit = admin_limits.get_effective_daily_limit()
            monthly_limit = admin_limits.get_effective_monthly_limit()
        except AdminConsumptionLimit.DoesNotExist:
            # Fallback to default limits defined in the profile model
            daily_limit = user_profile.daily_limit
            monthly_limit = user_profile.monthly_limit

        # Update context dictionary with all necessary data
        context.update({
            'user': self.request.user,
            'profile': user_profile,
            'is_daily_limited': is_daily_limited,
            'is_monthly_limited': is_monthly_limited,
            'daily_used': daily_used,
            'daily_limit': daily_limit,
            'monthly_used': monthly_used,
            'monthly_limit': monthly_limit,
        })
        
        return context
    
# 5. Search View
class SearchView(LoginRequiredMixin, ListView):
    """
    Handles search functionality.
    Requires login. Implements pagination and search logging.
    """
    template_name = 'users/search.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        """
        Define the queryset for the list view.
        Checks limits before performing the search.
        """
        query = self.request.GET.get('q', '')
        user_profile = self.request.user.profile

        # --- Check Limits Before Searching ---
        if not user_profile.check_daily_limit():
            messages.error(self.request, "You have reached your daily search limit.")
            return UserProfile.objects.none()
        
        if not user_profile.check_monthly_limit():
            messages.error(self.request, "You have reached your monthly search limit.")
            return UserProfile.objects.none()

        # --- Perform Search ---
        if query:
            start_time = time.time()
            
            # Filter users based on multiple fields
            results = UserProfile.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(national_code__icontains=query) |
                Q(phone_number__icontains=query) |
                Q(address__icontains=query)
            )
            
            end_time = time.time()
            duration = round(end_time - start_time, 4)

            # Log the search activity
            SearchLog.objects.create(
                user=self.request.user,
                query_text=query,
                results_count=results.count(),
                duration=duration
            )

            messages.success(self.request, f"Found {results.count()} results in {duration} seconds.")
            
            # Store temporary data in session for the template
            self.request.session['search_duration'] = duration
            self.request.session['search_query'] = query
            
            return results
        else:
            # If no query, return empty queryset
            return UserProfile.objects.none()

    def get_context_data(self, **kwargs):
        """
        Add search-specific data to the context.
        """
        context = super().get_context_data(**kwargs)
        
        # Retrieve data from session
        context['duration'] = self.request.session.get('search_duration', 0)
        context['query'] = self.request.session.get('search_query', '')
        
        return context

