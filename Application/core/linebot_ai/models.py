from django.db import models
from django.utils import timezone

class Student(models.Model):
    user_id = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=20) 
    manaba_id = models.CharField(max_length=30, blank=True, null=True)
    manaba_password = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.user_id})"
