from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    contact_number = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.user.username
