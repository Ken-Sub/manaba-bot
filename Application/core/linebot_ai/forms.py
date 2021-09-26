from django import forms
from .models import Student

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('manaba_id', 'manaba_password',)

        
