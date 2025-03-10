import os
from django.db import models
from django.contrib.auth.models import User

def user_upload_path(instance, filename):
    """Generate a file path for user uploads based on their username and loan ID."""
    loan_id = instance.id if instance.id else "new"
    return f"uploads/{instance.user.username}/loan_{loan_id}/{filename}"

class Loan(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=6.0)
    tenure_months = models.IntegerField(default=4)

    # File uploads
    face_image = models.ImageField(upload_to=user_upload_path, null=True, blank=True)
    id_upload = models.ImageField(upload_to=user_upload_path, null=True, blank=True)
    guarantor_id = models.ImageField(upload_to=user_upload_path, null=True, blank=True)

    # Guarantor details with default values to avoid migration errors
    guarantor_name = models.CharField(max_length=255, default="Unknown Guarantor")
    guarantor_occupation = models.CharField(max_length=255, default="Not Provided")
    guarantor_phone = models.CharField(max_length=15, default="0000000000")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Loan #{self.id} | {self.user.username} | ₦{self.loan_amount} ({self.status})"
