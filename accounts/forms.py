from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LoanApplication

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        """Ensure the email is unique and normalized."""
        email = self.cleaned_data.get("email").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email.")
        return email


class LoanApplicationForm(forms.ModelForm):
    class Meta:
        model = LoanApplication
        fields = ['full_name', 'phone', 'email', 'home_address', 'face_image', 'id_upload']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'home_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter home address', 'rows': 2}),
        }

    def clean_email(self):
        """Ensure email is unique across LoanApplication and User models."""
        email = self.cleaned_data.get("email").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already registered with a user account.")
        if LoanApplication.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A loan application with this email already exists.")
        return email

    def clean_phone(self):
        """Ensure phone number is unique in LoanApplication."""
        phone = self.cleaned_data.get("phone").strip()
        if LoanApplication.objects.filter(phone=phone).exists():
            raise forms.ValidationError("A loan application with this phone number already exists.")
        return phone
