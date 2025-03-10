import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Loan
from .forms import LoanApplicationForm

logger = logging.getLogger(__name__)

@login_required
def apply_for_loan(request):
    """Handles loan applications with face verification, ID upload, and guarantor details."""
    if request.method == "POST":
        logger.info(f"Loan application attempt by {request.user.username}")
        form = LoanApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            face_image = request.FILES.get("face_image")
            id_upload = request.FILES.get("id_upload")

            if not face_image:
                logger.error("No face image provided!")
                messages.error(request, "Face image is required!")
                return render(request, "loans/apply_loan.html", {"form": form})

            logger.info(f"Loan application by {request.user.username} for ₦{form.cleaned_data['loan_amount']}")
            logger.info(f"Guarantor Name: {form.cleaned_data['guarantor_name']}, Phone: {form.cleaned_data['guarantor_phone']}")

            try:
                loan = form.save(commit=False)
                loan.user = request.user
                loan.status = 'pending'  # Default status is pending

                # Assign file uploads
                loan.face_image = face_image
                loan.id_upload = id_upload

                loan.save()
                messages.success(request, "Your loan application has been submitted successfully!")
                logger.info(f"Loan successfully saved for {request.user.username}")
                return redirect("loan_success", loan_id=loan.id)
            
            except Exception as e:
                logger.error(f"Error saving loan application: {e}")
                messages.error(request, "An error occurred while submitting your loan application. Please try again.")
        else:
            logger.warning(f"Form validation failed: {form.errors}")
            messages.error(request, "Please correct the errors below.")

    else:
        form = LoanApplicationForm()

    return render(request, "loans/apply_loan.html", {"form": form})

@login_required
def loan_success(request, loan_id):
    """Displays success page after successful loan application."""
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)
    return render(request, "loans/loan_success.html", {"loan": loan})

@login_required
def loan_list(request):
    """Displays the list of loans applied by the logged-in user."""
    loans = Loan.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "loans/loan_list.html", {"loans": loans})

@login_required
def loan_detail(request, loan_id):
    """Displays details of a specific loan."""
    loan = get_object_or_404(Loan, id=loan_id, user=request.user)
    return render(request, "loans/loan_detail.html", {"loan": loan})

@login_required
def loan_calculator(request):
    """Render loan calculator page."""
    return render(request, "loans/loan_calculator.html")
