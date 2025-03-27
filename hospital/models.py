from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
    ROLE_CHOICES = [
        ('GM', 'General Manager'),
        ('DR', 'Doctor'),
        ('AS', 'Assistant'),
    ]
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    assistants = models.ManyToManyField('Assistant', related_name='assigned_doctors', blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.specialization})"

class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    # The reverse relationship is handled by the Doctor model

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=20)
    medical_history = models.TextField(blank=True)
    doctors = models.ManyToManyField(Doctor, related_name='patients')
    assistants = models.ManyToManyField(Assistant, related_name='patients', blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class TreatmentRecommendation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    recommendation_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.treatment.name} for {self.patient}"

class TreatmentApplication(models.Model):
    STATUS_CHOICES = [
        ('PE', 'Pending'),
        ('IP', 'In Progress'),
        ('CO', 'Completed'),
    ]
    
    assistant = models.ForeignKey(Assistant, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PE')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.treatment.name} for {self.patient} by {self.assistant}"
    
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
