from django import forms  
from .models import JobPosting 
class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = JobPosting  
        fields = "__all__"  