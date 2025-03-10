from django.db import models
from django.contrib.auth.models import User

class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loan_applications")
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    home_address = models.TextField()

    face_image = models.ImageField(upload_to="face_images/")
    id_upload = models.ImageField(upload_to="id_uploads/")

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Add this line if missing

    def __str__(self):
        return f"{self.full_name} - {self.status}"

