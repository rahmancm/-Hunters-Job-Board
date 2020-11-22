from django import forms  
from .models import JobPosting 
from .models import Application
from .models import Userprofile
from django.contrib.auth.models import User

class EmployeeForm(forms.ModelForm):  
    class Meta:  
        model = JobPosting  
        fields = "__all__"  

class ApplicationForm(forms.ModelForm):  
    class Meta:  
        model = Application  
        fields = ['content','experiance'] 
class UserprofileForm(forms.ModelForm):
    class Meta:
        model=Userprofile   
        fields=['PhoneNumber','address','education','profession','experiance','country','state','profile_pic']     
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model =User        
        fields =['first_name','last_name','username','email']