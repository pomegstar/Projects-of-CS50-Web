from django.db import models
from accounts.models import Patient
from hospitals.models import Doctor


class Appointment(models.Model):
    is_complete = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    treatment_date = models.DateField()
    appointment_time = models.DateTimeField(auto_now_add=True)
    serial_number = models.PositiveIntegerField()
    age = models.PositiveIntegerField(null=True)
    problem = models.TextField(null=True)

    def __str__(self):
        return f"Patient: {self.patient.user.username} - Dr: {self.doctor.user.username} on {self.treatment_date}"
