from django.db import models
from django.utils import timezone

class Student(models.Model):
    user_id = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=20) 
    manaba_id = models.CharField(max_length=30, blank=True)
    manaba_password = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.name} ({user_id})"

class LineMessage(models.Model):
    student = models.ForeignKey(Student, related_name="to_student", verbose_name="プッシュ先", on_delete=models.SET_NULL, blank=True)
    message = models.TextField(verbose_name="テキスト")
    created_at = models.DateTimeField(verbose_name="作成日", default=timezone.now)

    def __str__(self):
        return f"{self.student} - {self.message[:10]} - {"