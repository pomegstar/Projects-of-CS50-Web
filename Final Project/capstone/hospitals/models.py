from django.db import models
from accounts.models import User


class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255)
    weeks = models.CharField(max_length=255, null=True)
    fro = models.TimeField(null=True)
    to = models.TimeField(null=True)

    def __str__(self):
        return f"Dr. {self.user.username} ({self.specialization})"
