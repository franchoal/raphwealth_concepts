from django.urls import path
from .views import apply_for_loan, loan_success, loan_calculator  
from django.shortcuts import redirect

urlpatterns = [
    path('apply/', apply_for_loan, name='apply_for_loan'),  
    path('success/<int:loan_id>/', loan_success, name='loan_success'),  
    path('calculator/', loan_calculator, name='loan_calculator'),
    # path('home/', lambda request: redirect('home'), name='home'),  # Redirects to home page
]

