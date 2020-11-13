from django import forms  
from .models import JobPosting 
from .models import Application


class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = JobPosting  
        fields = "__all__"  

class ApplicationForm(forms.ModelForm):  
    class Meta:  
        model = Application  
        fields = ['content','experiance'] 