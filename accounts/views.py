import base64
import uuid
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UserRegistrationForm, LoanApplicationForm
from .models import LoanApplication

# ✅ User Registration
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # ✅ Saves user & hashes password
            login(request, user)  # ✅ Logs user in after registration
            messages.success(request, "Registration successful! Apply for a loan now.")
            return redirect(reverse_lazy("apply_loan"))  
    else:
        form = UserRegistrationForm()
    
    return render(request, "accounts/register.html", {"form": form})

# ✅ User Login
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful! Apply for a loan now.")
            return redirect(reverse_lazy("apply_loan"))
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

# ✅ User Logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect(reverse_lazy("login"))

# ✅ Loan Application - Only for Logged-in Users
@login_required
def apply_for_loan(request):
    if request.method == "POST":
        form = LoanApplicationForm(request.POST, request.FILES)
        
        if form.is_valid():
            # ✅ Handle Face Image (Base64 Decoding)
            face_image_data = request.POST.get("face_image")
            if face_image_data and ";base64," in face_image_data:
                try:
                    format, imgstr = face_image_data.split(";base64,")
                    ext = format.split("/")[-1]
                    valid_extensions = {"png", "jpg", "jpeg"}
                    
                    if ext not in valid_extensions:
                        messages.error(request, "Invalid image format. Only PNG, JPG, and JPEG are allowed.")
                        return render(request, "apply_loan.html", {"form": form})

                    image_data = ContentFile(base64.b64decode(imgstr), name=f"{uuid.uuid4()}.{ext}")
                    form.instance.face_image = image_data  # ✅ Save face image
                except Exception as e:
                    messages.error(request, "Error processing face image. Please try again.")
                    return render(request, "apply_loan.html", {"form": form})

            # ✅ Assign the logged-in user
            form.instance.user = request.user
            
            # ✅ Save loan application
            form.save()
            messages.success(request, "Loan application submitted successfully!")
            return redirect(reverse_lazy("loan_success"))  
    else:
        form = LoanApplicationForm()

    return render(request, "apply_loan.html", {"form": form})
