from django import forms
from django.apps import apps  # Lazy import to prevent circular import issues
import logging

# Setup logging for debugging
logger = logging.getLogger(__name__)

class LoanCalculatorForm(forms.Form):
    """Form for loan calculation input."""
    loan_amount = forms.DecimalField(
        label="Loan Amount",
        min_value=1000,
        max_digits=10,
        decimal_places=2
    )

class LoanApplicationForm(forms.ModelForm):
    """Form for loan application with face verification, ID upload, and guarantor details."""

    face_image = forms.ImageField(
        required=True,
        label="Face Verification (Upload a clear image)"
    )
    id_upload = forms.ImageField(
        required=True,
        label="Upload ID (Passport, Driver’s License, National ID)"
    )
    guarantor_name = forms.CharField(
        required=True,
        label="Guarantor's Full Name",
        max_length=255
    )
    guarantor_occupation = forms.CharField(
        required=True,
        label="Guarantor's Occupation",
        max_length=255
    )
    guarantor_phone = forms.CharField(
        required=True,
        label="Guarantor's Phone Number",
        max_length=15
    )
    guarantor_id = forms.ImageField(
        required=True,
        label="Guarantor's ID Upload (Passport, Driver’s License, National ID)"
    )

    class Meta:
        model = apps.get_model('loans', 'Loan')  # Lazy import to avoid circular import issues
        fields = [
            'loan_amount', 'face_image', 'id_upload',
            'guarantor_name', 'guarantor_occupation', 
            'guarantor_phone', 'guarantor_id'
        ]

    def clean_loan_amount(self):
        """Validate loan amount to ensure it meets the minimum requirement."""
        loan_amount = self.cleaned_data.get("loan_amount")
        if loan_amount and loan_amount < 1000:
            raise forms.ValidationError("Minimum loan amount is ₦1,000.")
        return loan_amount

    def clean_guarantor_phone(self):
        """Ensure the guarantor phone number is valid."""
        phone = self.cleaned_data.get("guarantor_phone")
        if phone and not phone.isdigit():
            raise forms.ValidationError("Guarantor phone number should contain only digits.")
        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError("Guarantor phone number must be between 10-15 digits.")
        return phone

    def clean(self):
        """Ensure all required fields are provided and log any issues."""
        cleaned_data = super().clean()
        face_image = cleaned_data.get("face_image")
        id_upload = cleaned_data.get("id_upload")
        guarantor_id = cleaned_data.get("guarantor_id")

        errors = {}

        if not face_image:
            logger.error("Face image is missing in form submission.")
            errors["face_image"] = "Face verification image is required."

        if not id_upload:
            logger.error("ID upload is missing in form submission.")
            errors["id_upload"] = "ID upload (Passport, Driver’s License, or National ID) is required."

        if not guarantor_id:
            logger.error("Guarantor ID upload is missing.")
            errors["guarantor_id"] = "Guarantor's ID upload is required."

        if errors:
            raise forms.ValidationError(errors)

        logger.info(f"Validated loan application data: {cleaned_data}")
        return cleaned_data
