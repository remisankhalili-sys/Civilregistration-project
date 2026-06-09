from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class UserRegistrationForm(forms.ModelForm):
    """
    New user registration form with phone number validation.
    """
    # Profile and password fields.
    national_code = forms.CharField(max_length=10, required=True, label="National Code")
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    birth_date = forms.DateField(required=False, label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Check the number format: it must start with +98 and be numbers.
        if not re.match(r'^\+98[0-9]{10}$', phone):
            raise ValidationError("Phone number must be in the format: +989121111111")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

class UserProfileForm(forms.ModelForm):
    """Form for user to edit profile (optional for later steps)."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']